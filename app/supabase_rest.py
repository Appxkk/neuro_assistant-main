import os
import requests
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL или SUPABASE_KEY не указаны в .env")

BASE_REST_URL = f"{SUPABASE_URL}/rest/v1"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
}


def get_rows(table: str, query: str = "select=*"):
    response = requests.get(
        f"{BASE_REST_URL}/{table}?{query}",
        headers=HEADERS,
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def insert_row(table: str, data: dict):
    response = requests.post(
        f"{BASE_REST_URL}/{table}",
        headers={**HEADERS, "Prefer": "return=representation"},
        json=data,
        timeout=10,
    )
    response.raise_for_status()
    return response.json()