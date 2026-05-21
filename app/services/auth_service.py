import hashlib
import os
import secrets
from datetime import datetime
from typing import Any
from urllib.parse import quote

import requests
from dotenv import load_dotenv
from fastapi import HTTPException, Request
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from werkzeug.security import check_password_hash, generate_password_hash


load_dotenv()


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BASE_REST_URL = f"{SUPABASE_URL}/rest/v1" if SUPABASE_URL else ""

AUTH_ENABLED = os.getenv("AUTH_ENABLED", "true").lower().strip() in {
    "1",
    "true",
    "yes",
    "on",
    "да",
}
AUTH_COOKIE_NAME = os.getenv("AUTH_COOKIE_NAME", "neuro_assistant_session")
AUTH_SECRET_KEY = os.getenv("AUTH_SECRET_KEY") or os.getenv("SUPABASE_KEY") or "dev-secret"
AUTH_SESSION_MAX_AGE = int(os.getenv("AUTH_SESSION_MAX_AGE", "86400"))
AUTH_COOKIE_SECURE = os.getenv("AUTH_COOKIE_SECURE", "false").lower().strip() in {
    "1",
    "true",
    "yes",
    "on",
    "да",
}

ACCESS_LEVELS = {"low", "medium", "high"}

PERMISSIONS_BY_LEVEL = {
    "low": {
        "view_dashboard",
        "view_orders",
        "view_tasks",
        "view_reports",
        "use_voice",
        "use_help",
        "download_pdf",
    },
    "medium": {
        "view_dashboard",
        "view_orders",
        "view_tasks",
        "view_reports",
        "view_history",
        "use_voice",
        "use_help",
        "download_pdf",
        "use_actions",
        "create_records",
    },
    "high": {
        "view_dashboard",
        "view_orders",
        "view_tasks",
        "view_reports",
        "view_history",
        "use_voice",
        "use_help",
        "download_pdf",
        "use_actions",
        "create_records",
        "manage_history",
        "manage_settings",
        "manage_employees",
        "send_mailing",
        "admin",
    },
}

ACTION_PERMISSIONS = {
    "create_order": "create_records",
    "create_sale": "create_records",
    "create_task": "create_records",
    "create_employee": "manage_employees",
    "send_mailing": "send_mailing",
}

serializer = URLSafeTimedSerializer(AUTH_SECRET_KEY, salt="neuro-assistant-auth")


def get_supabase_headers(prefer_return: bool = False) -> dict[str, str]:
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise HTTPException(
            status_code=500,
            detail="SUPABASE_URL или SUPABASE_KEY не указаны в .env",
        )

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
    }

    if prefer_return:
        headers["Prefer"] = "return=representation"

    return headers


def normalize_access_level(access_level: str | None) -> str:
    value = (access_level or "low").lower().strip()
    return value if value in ACCESS_LEVELS else "low"


def get_permissions(access_level: str | None) -> list[str]:
    return sorted(PERMISSIONS_BY_LEVEL.get(normalize_access_level(access_level), set()))


def has_permission(user: dict | None, permission: str | None) -> bool:
    if not permission:
        return True

    if not AUTH_ENABLED:
        return True

    if not user:
        return False

    return permission in PERMISSIONS_BY_LEVEL.get(
        normalize_access_level(user.get("access_level")),
        set(),
    )


def require_permission(user: dict | None, permission: str):
    if not has_permission(user, permission):
        raise HTTPException(
            status_code=403,
            detail="Недостаточно прав для выполнения действия",
        )


def get_required_permission(path: str, method: str) -> str | None:
    if path.startswith("/api/dashboard"):
        return "view_dashboard"

    if path.startswith("/api/pages/orders"):
        return "view_orders"

    if path.startswith("/api/pages/tasks"):
        return "view_tasks"

    if path.startswith("/api/pages/reports"):
        return "view_reports"

    if path.startswith("/api/pages/history"):
        return "view_history"

    if path.startswith("/api/history/clear"):
        return "manage_history"

    if path.startswith("/api/settings"):
        return "manage_settings"

    if path.startswith("/api/actions"):
        return "use_actions"

    if path.startswith("/api/mailings"):
        return "send_mailing"

    if path.startswith("/api/telegram"):
        return "admin"

    if path.startswith("/api/voice"):
        return "use_voice"

    if path.startswith("/api/pdf"):
        return "download_pdf"

    if path.startswith("/api/help"):
        return "use_help"

    return None


def hash_password(password: str) -> str:
    return generate_password_hash(password)


def hash_password_sha256(password: str) -> str:
    digest = hashlib.sha256(password.encode("utf-8")).hexdigest()
    return f"sha256${digest}"


def verify_password(password: str, stored_hash: str | None) -> bool:
    if not stored_hash:
        return False

    if stored_hash.startswith("sha256$"):
        return hash_password_sha256(password) == stored_hash

    return check_password_hash(stored_hash, password)


def generate_initial_credentials(employee_id: int) -> tuple[str, str]:
    username = f"employee_{employee_id}"
    password = f"NA-{secrets.token_hex(3).upper()}"
    return username, password


def find_employee_by_username(username: str) -> dict | None:
    safe_username = quote(username.strip(), safe="")
    url = (
        f"{BASE_REST_URL}/employees"
        f"?select=id,full_name,position,department,username,password_hash,access_level,must_change_password"
        f"&username=eq.{safe_username}"
        f"&limit=1"
    )

    response = requests.get(
        url,
        headers=get_supabase_headers(),
        timeout=10,
    )
    response.raise_for_status()
    rows = response.json()
    return rows[0] if rows else None


def update_employee_auth(employee_id: int, data: dict) -> list[dict]:
    payload = {
        **data,
        "updated_at": datetime.utcnow().isoformat(),
    }

    response = requests.patch(
        f"{BASE_REST_URL}/employees?id=eq.{employee_id}",
        headers=get_supabase_headers(prefer_return=True),
        json=payload,
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def prepare_employee_auth(employee_id: int) -> dict[str, str]:
    username, password = generate_initial_credentials(employee_id)

    update_employee_auth(
        employee_id,
        {
            "username": username,
            "password_hash": hash_password(password),
            "must_change_password": True,
        },
    )

    return {
        "username": username,
        "password": password,
    }


def make_session_payload(employee: dict) -> dict[str, Any]:
    access_level = normalize_access_level(employee.get("access_level"))

    return {
        "id": employee.get("id"),
        "full_name": employee.get("full_name"),
        "position": employee.get("position"),
        "department": employee.get("department"),
        "username": employee.get("username"),
        "access_level": access_level,
        "must_change_password": bool(employee.get("must_change_password")),
        "permissions": get_permissions(access_level),
    }


def create_session_token(employee: dict) -> str:
    return serializer.dumps(make_session_payload(employee))


def decode_session_token(token: str | None) -> dict | None:
    if not token:
        return None

    try:
        payload = serializer.loads(token, max_age=AUTH_SESSION_MAX_AGE)
    except (BadSignature, SignatureExpired):
        return None

    if not isinstance(payload, dict):
        return None

    payload["access_level"] = normalize_access_level(payload.get("access_level"))
    payload["permissions"] = get_permissions(payload.get("access_level"))

    return payload


def get_current_user_from_request(request: Request) -> dict | None:
    if not AUTH_ENABLED:
        return {
            "id": 0,
            "full_name": "Auth disabled",
            "username": "auth_disabled",
            "access_level": "high",
            "must_change_password": False,
            "permissions": get_permissions("high"),
        }

    return decode_session_token(request.cookies.get(AUTH_COOKIE_NAME))
