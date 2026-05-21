from fastapi import APIRouter, HTTPException, Request, Response
from pydantic import BaseModel

from app.services.auth_service import (
    AUTH_COOKIE_NAME,
    AUTH_COOKIE_SECURE,
    AUTH_SESSION_MAX_AGE,
    create_session_token,
    find_employee_by_username,
    get_current_user_from_request,
    hash_password,
    make_session_payload,
    normalize_access_level,
    require_permission,
    update_employee_auth,
    verify_password,
)


router = APIRouter(prefix="/api/auth", tags=["auth"])


class LoginRequest(BaseModel):
    username: str
    password: str


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str


class ChangeCredentialsRequest(BaseModel):
    current_password: str
    new_username: str | None = None
    new_password: str | None = None


class AccessLevelRequest(BaseModel):
    access_level: str


def set_auth_cookie(response: Response, token: str):
    response.set_cookie(
        key=AUTH_COOKIE_NAME,
        value=token,
        max_age=AUTH_SESSION_MAX_AGE,
        httponly=True,
        secure=AUTH_COOKIE_SECURE,
        samesite="lax",
    )


@router.post("/login")
def login(data: LoginRequest, response: Response):
    username = data.username.strip()

    if not username or not data.password:
        raise HTTPException(status_code=400, detail="Введите логин и пароль")

    employee = find_employee_by_username(username)

    if not employee or not verify_password(data.password, employee.get("password_hash")):
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    token = create_session_token(employee)
    set_auth_cookie(response, token)

    return {
        "status": "success",
        "user": make_session_payload(employee),
    }


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(AUTH_COOKIE_NAME)
    return {"status": "success"}


@router.get("/me")
def me(request: Request):
    user = get_current_user_from_request(request)

    if not user:
        raise HTTPException(status_code=401, detail="Требуется авторизация")

    return {"user": user}


@router.post("/change-password")
def change_password(data: ChangePasswordRequest, request: Request, response: Response):
    return change_credentials(
        ChangeCredentialsRequest(
            current_password=data.current_password,
            new_password=data.new_password,
        ),
        request,
        response,
    )


@router.post("/change-credentials")
def change_credentials(data: ChangeCredentialsRequest, request: Request, response: Response):
    user = get_current_user_from_request(request)

    if not user:
        raise HTTPException(status_code=401, detail="Требуется авторизация")

    employee = find_employee_by_username(user.get("username", ""))

    if not employee or not verify_password(data.current_password, employee.get("password_hash")):
        raise HTTPException(status_code=400, detail="Текущий пароль указан неверно")

    update_data = {}

    new_username = (data.new_username or "").strip()
    new_password = data.new_password or ""

    if new_username and new_username != employee.get("username"):
        if len(new_username) < 3:
            raise HTTPException(
                status_code=400,
                detail="Новый логин должен быть не короче 3 символов",
            )

        existing_employee = find_employee_by_username(new_username)

        if existing_employee and int(existing_employee["id"]) != int(employee["id"]):
            raise HTTPException(
                status_code=400,
                detail="Такой логин уже используется",
            )

        update_data["username"] = new_username

    if new_password:
        if len(new_password.strip()) < 6:
            raise HTTPException(
                status_code=400,
                detail="Новый пароль должен быть не короче 6 символов",
            )

        update_data["password_hash"] = hash_password(new_password)
        update_data["must_change_password"] = False

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="Укажите новый логин или новый пароль",
        )

    updated_rows = update_employee_auth(
        int(employee["id"]),
        update_data,
    )

    updated_employee = updated_rows[0] if updated_rows else {
        **employee,
        **update_data,
        "must_change_password": False,
    }

    token = create_session_token(updated_employee)
    set_auth_cookie(response, token)

    return {
        "status": "success",
        "message": "Учётные данные обновлены",
        "user": make_session_payload(updated_employee),
    }


@router.post("/employees/{employee_id}/access-level")
def update_access_level(employee_id: int, data: AccessLevelRequest, request: Request):
    user = get_current_user_from_request(request)
    require_permission(user, "manage_employees")

    access_level = normalize_access_level(data.access_level)
    updated_rows = update_employee_auth(
        employee_id,
        {
            "access_level": access_level,
        },
    )

    return {
        "status": "success",
        "employee": updated_rows[0] if updated_rows else None,
    }
