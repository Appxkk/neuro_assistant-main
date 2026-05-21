from app.supabase_rest import get_rows, insert_row


def execute_business_command(
    recognized_text: str,
    intent: str,
    parameters: dict
) -> dict:
    """
    Выполняет бизнес-действие по intent и parameters.
    """

    if intent == "find_order":
        return find_order(parameters)

    if intent == "show_sales":
        return show_sales(parameters)

    if intent == "show_active_tasks":
        return show_tasks_by_status("Активная")

    if intent == "show_overdue_tasks":
        return show_tasks_by_status("Просрочена")

    if intent == "create_task":
        return create_task(parameters)

    if intent == "warehouse_report":
        return warehouse_report()

    return {
        "result_text": "Команда не распознана или пока не поддерживается",
        "data": []
    }


def find_order(parameters: dict) -> dict:
    order_id = parameters.get("order_id")

    if not order_id:
        return {
            "result_text": "Не указан номер заказа",
            "data": []
        }

    orders = get_rows("orders", f"select=*&id=eq.{order_id}")

    if not orders:
        return {
            "result_text": f"Заказ №{order_id} не найден",
            "data": []
        }

    order = orders[0]

    return {
        "result_text": (
            f"Заказ №{order.get('id')} найден. "
            f"Клиент: {order.get('customer_name')}. "
            f"Сумма: {order.get('amount')} ₽. "
            f"Статус: {order.get('status')}."
        ),
        "data": orders
    }


def show_sales(parameters: dict) -> dict:
    period = parameters.get("period")

    query = "select=*"

    if period == "march":
        query = "select=*&sale_date=gte.2026-03-01&sale_date=lte.2026-03-31"
    elif period == "april":
        query = "select=*&sale_date=gte.2026-04-01&sale_date=lte.2026-04-30"

    sales = get_rows("sales", query)

    total_sales = sum(float(item.get("total_price") or 0) for item in sales)
    total_quantity = sum(int(item.get("quantity") or 0) for item in sales)

    return {
        "result_text": (
            f"Продажи за выбранный период: {total_sales:.0f} ₽. "
            f"Количество проданных товаров: {total_quantity}."
        ),
        "data": sales
    }


def show_tasks_by_status(status: str) -> dict:
    tasks = get_rows("tasks", f"select=*&status=eq.{status}")

    return {
        "result_text": f"Найдено задач со статусом «{status}»: {len(tasks)}",
        "data": tasks
    }


def create_task(parameters: dict) -> dict:
    employee_name = parameters.get("employee")
    task_title = parameters.get("task_title") or "Новая задача"

    if not employee_name:
        return {
            "result_text": "Не указан сотрудник для создания задачи",
            "data": []
        }

    employees = get_rows(
        "employees",
        f"select=*&full_name=ilike.*{employee_name}*"
    )

    employee_id = employees[0]["id"] if employees else None

    new_task = {
        "title": task_title,
        "description": "Задача создана голосовым помощником",
        "employee_id": employee_id,
        "status": "Активная",
        "priority": "Средний",
        "deadline": None
    }

    created_task = insert_row("tasks", new_task)

    return {
        "result_text": f"Задача создана: {task_title}",
        "data": created_task
    }


def warehouse_report() -> dict:
    sales = get_rows("sales", "select=*")

    products = {}

    for item in sales:
        product_name = item.get("product_name")
        quantity = int(item.get("quantity") or 0)

        if product_name not in products:
            products[product_name] = 0

        products[product_name] += quantity

    report = [
        {
            "product_name": product,
            "sold_quantity": quantity
        }
        for product, quantity in products.items()
    ]

    return {
        "result_text": f"Сформирован складской отчёт по {len(report)} товарам",
        "data": report
    }


def save_command_history(
    recognized_text: str,
    intent: str,
    parameters: dict,
    result_text: str,
    status: str = "Выполнено"
):
    insert_row(
        "command_history",
        {
            "recognized_text": recognized_text,
            "intent": intent,
            "parameters": parameters,
            "result_text": result_text,
            "status": status
        }
    )