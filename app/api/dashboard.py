from fastapi import APIRouter
from app.supabase_rest import get_rows


router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("")
def get_dashboard():
    orders = get_rows("orders")
    tasks = get_rows("tasks")
    sales = get_rows("sales")
    history = get_rows("command_history", "select=*&order=created_at.desc&limit=5")

    active_tasks = [task for task in tasks if task.get("status") == "Активная"]
    reports_count = [
        item for item in history
        if item.get("intent") and "report" in item.get("intent")
    ]

    total_sales = sum(float(sale.get("total_price") or 0) for sale in sales)

    return {
        "stats": {
            "commands_today": len(history),
            "success_commands": len(history),
            "active_tasks": len(active_tasks),
            "reports_count": len(reports_count),
        },
        "reports": {
            "total_sales": total_sales,
            "orders_count": len(orders),
        },
        "history": [
            {
                "id": item.get("id"),
                "text": item.get("recognized_text"),
                "intent": item.get("intent"),
                "status": item.get("status"),
                "created_at": item.get("created_at"),
            }
            for item in history
        ],
        "tasks": [
            {
                "id": item.get("id"),
                "title": item.get("title"),
                "employee_id": item.get("employee_id"),
                "deadline": item.get("deadline"),
                "priority": item.get("priority"),
                "status": item.get("status"),
            }
            for item in active_tasks[:5]
        ],
    }