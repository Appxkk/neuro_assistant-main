import os

import httpx
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException


load_dotenv()

router = APIRouter(prefix="/api/history", tags=["history"])

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


def get_supabase_headers():
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise HTTPException(
            status_code=500,
            detail="SUPABASE_URL или SUPABASE_KEY не указаны в .env",
        )

    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }


@router.delete("/clear")
def clear_history():
    """
    Полностью очищает историю команд.
    Таблица истории должна называться command_history.
    """

    url = f"{SUPABASE_URL}/rest/v1/command_history?id=gt.0"

    try:
        with httpx.Client(timeout=10) as client:
            response = client.delete(
                url,
                headers=get_supabase_headers(),
            )

        if response.status_code >= 400:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.text,
            )

        return {
            "status": "success",
            "result_text": "История команд очищена",
            "data": response.json() if response.text else [],
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка очистки истории: {str(error)}",
        )