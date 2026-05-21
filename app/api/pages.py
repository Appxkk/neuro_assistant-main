from fastapi import APIRouter
from app.supabase_rest import get_rows


router = APIRouter(prefix="/api/pages", tags=["pages"])


@router.get("/orders")
def get_orders_page():
    orders = get_rows("orders", "select=*&order=id.asc")
    return {"orders": orders}


@router.get("/tasks")
def get_tasks_page():
    tasks = get_rows("tasks", "select=*&order=id.asc")
    return {"tasks": tasks}


@router.get("/reports")
def get_reports_page():
    sales = get_rows("sales", "select=*&order=sale_date.asc")
    orders = get_rows("orders", "select=*")
    tasks = get_rows("tasks", "select=*")

    total_sales = sum(float(item.get("total_price") or 0) for item in sales)
    total_quantity = sum(int(item.get("quantity") or 0) for item in sales)
    average_sale = total_sales / len(sales) if sales else 0

    return {
        "summary": {
            "total_sales": total_sales,
            "total_quantity": total_quantity,
            "average_sale": average_sale,
            "orders_count": len(orders),
            "tasks_count": len(tasks),
        },
        "sales": sales,
    }


@router.get("/history")
def get_history_page():
    history = get_rows(
        "command_history",
        "select=*&order=created_at.desc&limit=30"
    )

    return {"history": history}