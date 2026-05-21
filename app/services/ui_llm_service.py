import json
import os
import re

import httpx

from app.services.ui_capabilities import (
    get_ui_capabilities_json,
    validate_ui_action
)


OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")
OLLAMA_UI_MODEL = os.getenv("OLLAMA_UI_MODEL", os.getenv("OLLAMA_MODEL", "qwen2.5:1.5b"))
OLLAMA_ENABLED = os.getenv("OLLAMA_ENABLED", "true").lower().strip() in {
    "1",
    "true",
    "yes",
    "on",
    "да",
}
try:
    OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "8"))
except Exception:
    OLLAMA_TIMEOUT = 8


def extract_json(text: str) -> dict | None:
    if not text:
        return None

    text = text.strip()

    try:
        return json.loads(text)
    except Exception:
        pass

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        return None

    try:
        return json.loads(match.group(0))
    except Exception:
        return None


def is_ollama_available() -> bool:
    if not OLLAMA_ENABLED or not OLLAMA_URL:
        return False

    try:
        with httpx.Client(timeout=OLLAMA_TIMEOUT) as client:
            response = client.get(f"{OLLAMA_URL}/api/tags")

        return response.status_code < 400
    except Exception:
        return False


def interpret_ui_command_with_ollama(user_text: str) -> dict | None:
    """
    Пытается понять неизвестную UI-команду через Ollama.
    Ollama получает список возможностей сайта и может вернуть только разрешенное действие.
    """

    if not user_text or not is_ollama_available():
        return None

    system_prompt = f"""
Ты являешься модулем управления web-интерфейсом.

Тебе нужно определить, является ли команда пользователя командой управления сайтом.

Ты знаешь только эти возможности сайта:
{get_ui_capabilities_json()}

Правила:
1. Не выдумывай действий, которых нет в списке возможностей.
2. Если команда относится к заказам, продажам, задачам или отчетам как к бизнес-данным — верни unknown.
3. Если команда управляет интерфейсом, настройками, темой, языком, страницами или режимами — верни JSON.
4. Отвечай только JSON без пояснений.

Формат ответа для известной UI-команды:
{{
  "intent": "open_page | change_theme | change_language | change_setting | change_nlp_mode",
  "parameters": {{}},
  "result_text": "краткое действие на русском языке"
}}

Формат ответа, если команда не относится к UI:
{{
  "intent": "unknown",
  "parameters": {{}},
  "result_text": "Команда не относится к управлению интерфейсом"
}}

Примеры:
Пользователь: "сделай шрифт крупнее"
Ответ:
{{
  "intent": "change_setting",
  "parameters": {{
    "setting": "fontSize",
    "value": "large"
  }},
  "result_text": "Увеличиваю размер шрифта"
}}

Пользователь: "сделай сайт компактнее"
Ответ:
{{
  "intent": "change_setting",
  "parameters": {{
    "setting": "compactMode",
    "value": true
  }},
  "result_text": "Включаю компактный режим"
}}

Пользователь: "открой раздел с заказами"
Ответ:
{{
  "intent": "open_page",
  "parameters": {{
    "page": "orders"
  }},
  "result_text": "Открываю раздел заказов"
}}

Пользователь: "покажи заказ 152"
Ответ:
{{
  "intent": "unknown",
  "parameters": {{}},
  "result_text": "Команда не относится к управлению интерфейсом"
}}
"""

    payload = {
        "model": OLLAMA_UI_MODEL,
        "stream": False,
        "format": "json",
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_text
            }
        ]
    }

    try:
        with httpx.Client(timeout=OLLAMA_TIMEOUT) as client:
            response = client.post(f"{OLLAMA_URL}/api/chat", json=payload)
            response.raise_for_status()

        data = response.json()
        content = data.get("message", {}).get("content", "")

        parsed = extract_json(content)

        if not parsed:
            return None

        if parsed.get("intent") == "unknown":
            return None

        return validate_ui_action(parsed)

    except Exception as error:
        print(f"Ollama UI parser error: {error}")
        return None
