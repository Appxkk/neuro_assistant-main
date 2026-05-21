import os
import json
from datetime import datetime
from urllib.parse import quote

import httpx
from dotenv import load_dotenv
from fastapi import HTTPException


load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


def get_supabase_headers(prefer: str | None = None) -> dict:
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise HTTPException(status_code=500, detail="SUPABASE_URL или SUPABASE_KEY не указаны в .env")

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
    }

    if prefer:
        headers["Prefer"] = prefer

    return headers


def ensure_telegram_token():
    if not TELEGRAM_BOT_TOKEN:
        raise HTTPException(status_code=500, detail="TELEGRAM_BOT_TOKEN не указан в .env")


def normalize_start_payload(text: str) -> str:
    if not text:
        return "client"

    parts = text.strip().split(maxsplit=1)

    if not parts:
        return "client"

    command = parts[0].split("@", 1)[0].lower()

    if command != "/start":
        return ""

    if len(parts) == 1:
        return "client"

    return parts[1].strip() or "client"


def extract_chat_data(update: dict) -> dict | None:
    message = update.get("message")

    if not isinstance(message, dict):
        return None

    text = str(message.get("text") or "").strip()
    payload = normalize_start_payload(text)

    if payload == "":
        return None

    chat = message.get("chat") or {}
    user = message.get("from") or {}
    chat_id = chat.get("id")

    if chat_id is None:
        return None

    return {
        "chat_id": str(chat_id),
        "username": user.get("username") or chat.get("username"),
        "first_name": user.get("first_name") or chat.get("first_name"),
        "last_name": user.get("last_name") or chat.get("last_name"),
        "payload": payload,
    }


async def process_telegram_update(update: dict, send_reply: bool = True) -> dict:
    chat_data = extract_chat_data(update)

    if not chat_data:
        return {
            "status": "ignored",
            "reason": "update_without_start_command",
        }

    payload = chat_data["payload"]

    if payload == "client":
        recipient = await register_client(chat_data)
        reply_text = (
            "Вы зарегистрированы как обычный получатель рассылок. "
            "Теперь вам можно отправлять клиентские уведомления."
        )
        result = {
            "status": "registered",
            "recipient_type": "client",
            "priority": "normal",
            "recipient": recipient,
        }

    elif payload.startswith("employee_"):
        code = payload.removeprefix("employee_").strip().upper()
        result, reply_text = await register_employee_by_code(chat_data, code)

    else:
        reply_text = (
            "Не удалось определить тип входа. "
            "Используйте ссылку для клиента или персональную ссылку сотрудника."
        )
        result = {
            "status": "error",
            "reason": "unknown_start_payload",
            "payload": payload,
        }

    if send_reply:
        await send_telegram_reply(chat_data["chat_id"], reply_text)

    return result


async def register_client(chat_data: dict) -> dict:
    return await upsert_recipient(
        {
            "chat_id": chat_data["chat_id"],
            "username": chat_data.get("username"),
            "first_name": chat_data.get("first_name"),
            "last_name": chat_data.get("last_name"),
            "recipient_type": "client",
            "priority": "normal",
            "employee_id": None,
            "is_active": True,
            "updated_at": datetime.utcnow().isoformat(),
        }
    )


async def register_employee_by_code(chat_data: dict, code: str) -> tuple[dict, str]:
    if not code:
        return (
            {
                "status": "error",
                "reason": "empty_employee_code",
            },
            "Код сотрудника не указан. Используйте персональную ссылку сотрудника.",
        )

    employee = await find_employee_by_telegram_code(code)

    if not employee:
        return (
            {
                "status": "error",
                "reason": "employee_code_not_found",
                "code": code,
            },
            "Код сотрудника не найден. Обратитесь к администратору системы.",
        )

    recipient = await upsert_recipient(
        {
            "chat_id": chat_data["chat_id"],
            "username": chat_data.get("username"),
            "first_name": chat_data.get("first_name"),
            "last_name": chat_data.get("last_name"),
            "recipient_type": "employee",
            "priority": "staff",
            "employee_id": employee["id"],
            "is_active": True,
            "updated_at": datetime.utcnow().isoformat(),
        }
    )

    return (
        {
            "status": "registered",
            "recipient_type": "employee",
            "priority": "staff",
            "employee": employee,
            "recipient": recipient,
        },
        f"Вы зарегистрированы как сотрудник: {employee.get('full_name')}.",
    )


async def find_employee_by_telegram_code(code: str) -> dict | None:
    code = quote(code, safe="")
    url = (
        f"{SUPABASE_URL}/rest/v1/employees"
        f"?select=id,full_name,position,department,telegram_code"
        f"&telegram_code=eq.{code}"
        f"&limit=1"
    )

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(url, headers=get_supabase_headers())

    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    rows = response.json()
    return rows[0] if rows else None


async def upsert_recipient(data: dict) -> dict:
    url = f"{SUPABASE_URL}/rest/v1/telegram_recipients?on_conflict=chat_id"

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(
            url,
            headers=get_supabase_headers("resolution=merge-duplicates,return=representation"),
            json=data,
        )

    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    rows = response.json()
    return rows[0] if rows else data


async def send_telegram_reply(chat_id: str, text: str) -> dict:
    ensure_telegram_token()

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.post(
            url,
            json={
                "chat_id": chat_id,
                "text": text,
            },
        )

    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    data = response.json()

    if not data.get("ok"):
        raise HTTPException(status_code=502, detail=data.get("description") or "Telegram API вернул ошибку")

    return data.get("result") or {}


async def get_telegram_updates(offset: int | None = None) -> dict:
    ensure_telegram_token()

    params = {
        "timeout": 0,
        "allowed_updates": json.dumps(["message"]),
    }

    if offset is not None:
        params["offset"] = offset

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"

    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get(url, params=params)

    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    data = response.json()

    if not data.get("ok"):
        raise HTTPException(status_code=502, detail=data.get("description") or "Telegram API вернул ошибку")

    return data


async def set_telegram_webhook(webhook_url: str) -> dict:
    ensure_telegram_token()

    if not webhook_url.startswith("https://"):
        raise HTTPException(status_code=400, detail="Webhook URL должен начинаться с https://")

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook"

    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.post(
            url,
            json={
                "url": webhook_url,
                "allowed_updates": ["message"],
            },
        )

    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    data = response.json()

    if not data.get("ok"):
        raise HTTPException(status_code=502, detail=data.get("description") or "Telegram API вернул ошибку")

    return data


async def get_telegram_webhook_info() -> dict:
    ensure_telegram_token()

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getWebhookInfo"

    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.get(url)

    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    data = response.json()

    if not data.get("ok"):
        raise HTTPException(status_code=502, detail=data.get("description") or "Telegram API вернул ошибку")

    return data
