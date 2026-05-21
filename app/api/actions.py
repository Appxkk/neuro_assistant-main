import os
from datetime import datetime

import httpx
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from app.services.mailing_service import send_mailing
from app.services.auth_service import (
    ACTION_PERMISSIONS,
    get_current_user_from_request,
    normalize_access_level,
    prepare_employee_auth,
    require_permission,
)


load_dotenv()

router = APIRouter(prefix="/api/actions", tags=["actions"])


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


class ConfirmActionRequest(BaseModel):
    action: str
    payload: dict


def get_supabase_headers():
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise HTTPException(
            status_code=500,
            detail="SUPABASE_URL или SUPABASE_KEY не указаны в .env"
        )

    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }


@router.get("/employees")
def get_employees():
    url = (
        f"{SUPABASE_URL}/rest/v1/employees"
        "?select=id,full_name,position,department,access_level"
        "&order=id.asc"
    )

    try:
        with httpx.Client(timeout=10) as client:
            response = client.get(
                url,
                headers=get_supabase_headers()
            )

        if response.status_code >= 400:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.text
            )

        rows = response.json()

        return {
            "employees": [
                {
                    "id": row["id"],
                    "name": row["full_name"],
                    "position": row.get("position"),
                    "department": row.get("department"),
                    "access_level": row.get("access_level"),
                }
                for row in rows
            ]
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка загрузки сотрудников: {str(error)}"
        )


@router.get("/managers")
def get_managers():
    url = (
        f"{SUPABASE_URL}/rest/v1/employees"
        "?select=id,full_name,position,department"
        "&position=eq.Менеджер"
        "&order=id.asc"
    )

    try:
        with httpx.Client(timeout=10) as client:
            response = client.get(
                url,
                headers=get_supabase_headers()
            )

        if response.status_code >= 400:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.text
            )

        rows = response.json()

        return {
            "managers": [
                {
                    "id": row["id"],
                    "name": row["full_name"],
                    "position": row.get("position"),
                    "department": row.get("department"),
                }
                for row in rows
            ]
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка загрузки менеджеров: {str(error)}"
        )


@router.get("/orders")
def get_orders():
    url = (
        f"{SUPABASE_URL}/rest/v1/orders"
        "?select=id,customer_name,amount,status,manager_id,created_at"
        "&order=id.asc"
    )

    try:
        with httpx.Client(timeout=10) as client:
            response = client.get(
                url,
                headers=get_supabase_headers()
            )

        if response.status_code >= 400:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.text
            )

        rows = response.json()

        return {
            "orders": [
                {
                    "id": row["id"],
                    "customer_name": row.get("customer_name"),
                    "amount": row.get("amount"),
                    "status": row.get("status"),
                    "manager_id": row.get("manager_id"),
                    "created_at": row.get("created_at"),
                }
                for row in rows
            ]
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка загрузки заказов: {str(error)}"
        )


@router.post("/confirm")
def confirm_action(body: ConfirmActionRequest, request: Request):
    user = get_current_user_from_request(request)
    required_permission = ACTION_PERMISSIONS.get(body.action)

    if required_permission:
        require_permission(user, required_permission)

    if body.action == "create_order":
        return create_order(body.payload)

    if body.action == "create_employee":
        return create_employee(body.payload)

    if body.action == "create_sale":
        return create_sale(body.payload)

    if body.action == "create_task":
        return create_task(body.payload)

    if body.action == "send_mailing":
        return send_mailing(body.payload)

    raise HTTPException(
        status_code=400,
        detail=f"Неизвестное действие: {body.action}"
    )


def create_order(payload: dict):
    customer_name = payload.get("customer_name")
    amount = payload.get("amount")
    status = payload.get("status", "Новый")
    manager_id = payload.get("manager_id")

    if not customer_name:
        raise HTTPException(status_code=400, detail="Не указан клиент")

    if amount is None:
        raise HTTPException(status_code=400, detail="Не указана сумма заказа")

    if manager_id is None:
        raise HTTPException(status_code=400, detail="Не выбран менеджер")

    try:
        amount = float(amount)
    except ValueError:
        raise HTTPException(status_code=400, detail="Некорректная сумма заказа")

    try:
        manager_id = int(manager_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Некорректный manager_id")

    order_data = {
        "customer_name": customer_name,
        "amount": amount,
        "status": status,
        "manager_id": manager_id,
        "created_at": datetime.utcnow().isoformat(),
    }

    url = f"{SUPABASE_URL}/rest/v1/orders"

    try:
        with httpx.Client(timeout=10) as client:
            response = client.post(
                url,
                headers=get_supabase_headers(),
                json=order_data,
            )

        if response.status_code >= 400:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.text
            )

        created_rows = response.json()

        return {
            "status": "success",
            "result_text": "Заказ успешно добавлен в базу данных",
            "data": created_rows,
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка добавления заказа: {str(error)}"
        )


def create_employee(payload: dict):
    full_name = payload.get("full_name")
    position = payload.get("position")
    department = payload.get("department")
    access_level = normalize_access_level(payload.get("access_level"))

    if not full_name:
        raise HTTPException(status_code=400, detail="Не указано ФИО сотрудника")

    if not position:
        raise HTTPException(status_code=400, detail="Не указана должность")

    if not department:
        raise HTTPException(status_code=400, detail="Не указан отдел")

    employee_data = {
        "full_name": full_name,
        "position": position,
        "department": department,
        "access_level": access_level,
        "created_at": datetime.utcnow().isoformat(),
    }

    url = f"{SUPABASE_URL}/rest/v1/employees"

    try:
        with httpx.Client(timeout=10) as client:
            response = client.post(
                url,
                headers=get_supabase_headers(),
                json=employee_data,
            )

        if response.status_code >= 400:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.text
            )

        created_rows = response.json()

        if created_rows:
            credentials = prepare_employee_auth(int(created_rows[0]["id"]))
            created_rows[0]["initial_username"] = credentials["username"]
            created_rows[0]["initial_password"] = credentials["password"]
            created_rows[0]["must_change_password"] = True

        return {
            "status": "success",
            "result_text": (
                "Сотрудник успешно добавлен. "
                f"Первичный логин: {created_rows[0].get('initial_username') if created_rows else '—'}. "
                f"Первичный пароль: {created_rows[0].get('initial_password') if created_rows else '—'}"
            ),
            "data": created_rows,
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка добавления сотрудника: {str(error)}"
        )


def create_sale(payload: dict):
    order_id = payload.get("order_id")
    product_name = payload.get("product_name")
    quantity = payload.get("quantity")
    total_price = payload.get("total_price")
    sale_date = payload.get("sale_date")

    if order_id is None:
        raise HTTPException(status_code=400, detail="Не выбран заказ")

    if not product_name:
        raise HTTPException(status_code=400, detail="Не указан товар")

    if quantity is None:
        raise HTTPException(status_code=400, detail="Не указано количество")

    if total_price is None:
        raise HTTPException(status_code=400, detail="Не указана сумма продажи")

    if not sale_date:
        raise HTTPException(status_code=400, detail="Не указана дата продажи")

    try:
        order_id = int(order_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Некорректный order_id")

    try:
        quantity = int(quantity)
    except ValueError:
        raise HTTPException(status_code=400, detail="Некорректное количество")

    try:
        total_price = float(total_price)
    except ValueError:
        raise HTTPException(status_code=400, detail="Некорректная сумма продажи")

    sale_data = {
        "order_id": order_id,
        "product_name": product_name,
        "quantity": quantity,
        "total_price": total_price,
        "sale_date": sale_date,
    }

    url = f"{SUPABASE_URL}/rest/v1/sales"

    try:
        with httpx.Client(timeout=10) as client:
            response = client.post(
                url,
                headers=get_supabase_headers(),
                json=sale_data,
            )

        if response.status_code >= 400:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.text
            )

        created_rows = response.json()

        return {
            "status": "success",
            "result_text": "Продажа успешно добавлена в базу данных",
            "data": created_rows,
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка добавления продажи: {str(error)}"
        )


def create_task(payload: dict):
    title = payload.get("title")
    description = payload.get("description", "")
    employee_id = payload.get("employee_id")
    status = payload.get("status", "Активная")
    priority = payload.get("priority", "Средний")
    deadline = payload.get("deadline")

    if not title:
        raise HTTPException(status_code=400, detail="Не указано название задачи")

    if employee_id is None:
        raise HTTPException(status_code=400, detail="Не выбран исполнитель")

    if not deadline:
        raise HTTPException(status_code=400, detail="Не указан срок задачи")

    try:
        employee_id = int(employee_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Некорректный employee_id")

    task_data = {
        "title": title,
        "description": description,
        "employee_id": employee_id,
        "status": status,
        "priority": priority,
        "deadline": deadline,
        "created_at": datetime.utcnow().isoformat(),
    }

    url = f"{SUPABASE_URL}/rest/v1/tasks"

    try:
        with httpx.Client(timeout=10) as client:
            response = client.post(
                url,
                headers=get_supabase_headers(),
                json=task_data,
            )

        if response.status_code >= 400:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.text
            )

        created_rows = response.json()

        return {
            "status": "success",
            "result_text": "Задача успешно добавлена в базу данных",
            "data": created_rows,
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка добавления задачи: {str(error)}"
        )
