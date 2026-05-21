import json
import os
import re
from typing import Any

import httpx
from dotenv import load_dotenv

from app.services.ui_capabilities import (
    get_ui_capabilities_json,
    validate_ui_action,
)


load_dotenv()


OPENROUTER_CHAT_URL = "https://openrouter.ai/api/v1/chat/completions"

CLOUD_LLM_PROVIDER = os.getenv("CLOUD_LLM_PROVIDER", "openrouter").lower().strip()
CLOUD_LLM_API_KEY = os.getenv("CLOUD_LLM_API_KEY", "")
CLOUD_LLM_MODEL = os.getenv("CLOUD_LLM_MODEL", "openrouter/free")
CLOUD_LLM_REFERER = os.getenv("CLOUD_LLM_HTTP_REFERER", "https://neuro-assistant.local")
CLOUD_LLM_TITLE = os.getenv("CLOUD_LLM_TITLE", "Neuro Assistant")


def env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)

    if value is None:
        return default

    return value.lower().strip() in {"1", "true", "yes", "y", "on", "да"}


def env_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except Exception:
        return default


def cloud_llm_enabled() -> bool:
    return (
        env_bool("CLOUD_LLM_ENABLED", False)
        and CLOUD_LLM_PROVIDER == "openrouter"
        and bool(CLOUD_LLM_API_KEY.strip())
    )


def cloud_llm_timeout() -> int:
    return env_int("CLOUD_LLM_TIMEOUT", 12)


def empty_business_parameters() -> dict[str, Any]:
    return {
        "period": None,
        "order_id": None,
        "employee": None,
        "task_title": None,
        "customer": None,
        "status": None,
    }


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


def call_openrouter_chat(messages: list[dict[str, str]], temperature: float = 0.1) -> str | None:
    if not cloud_llm_enabled():
        return None

    headers = {
        "Authorization": f"Bearer {CLOUD_LLM_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": CLOUD_LLM_REFERER,
        "X-Title": CLOUD_LLM_TITLE,
    }

    payload = {
        "model": CLOUD_LLM_MODEL,
        "messages": messages,
        "temperature": temperature,
    }

    try:
        with httpx.Client(timeout=cloud_llm_timeout()) as client:
            response = client.post(
                OPENROUTER_CHAT_URL,
                headers=headers,
                json=payload,
            )

        response.raise_for_status()
        data = response.json()
        choices = data.get("choices") or []

        if not choices:
            return None

        return (choices[0].get("message", {}).get("content") or "").strip()

    except Exception as error:
        print(f"OpenRouter request error: {error}")
        return None


def normalize_business_response(parsed: dict | None, fallback_reason: str) -> dict[str, Any]:
    allowed_intents = {
        "show_sales",
        "find_order",
        "create_task",
        "show_active_tasks",
        "show_overdue_tasks",
        "warehouse_report",
        "unknown",
    }

    if not isinstance(parsed, dict):
        parsed = {}

    intent = parsed.get("intent")

    if intent not in allowed_intents:
        intent = "unknown"
        fallback_reason = "unknown_command"
    elif intent == "unknown":
        fallback_reason = "unknown_command"

    parameters = empty_business_parameters()

    if isinstance(parsed.get("parameters"), dict):
        parameters.update(parsed["parameters"])

    if intent == "unknown":
        parameters = empty_business_parameters()

    return {
        "intent": intent,
        "parameters": parameters,
        "source": "openrouter",
        "fallback": True,
        "fallback_reason": fallback_reason,
    }


def interpret_command_with_cloud(
    user_text: str,
    fallback_reason: str = "local_parser_and_ollama_unavailable",
) -> dict[str, Any] | None:
    if not user_text or not cloud_llm_enabled():
        return None

    system_prompt = """
Ты NLP-модуль русскоязычного веб-приложения нейропомощника для бизнес-процессов.

Твоя задача — преобразовать команду пользователя в строгий JSON для backend.
Не придумывай новые функции, intent или поля. Если команда не относится к списку возможностей, верни unknown.

Доступные бизнес-intent:
- show_sales: показать продажи или выручку.
- find_order: найти или показать заказ по номеру.
- create_task: создать задачу сотруднику.
- show_active_tasks: показать активные задачи.
- show_overdue_tasks: показать просроченные задачи.
- warehouse_report: сформировать складской отчет или показать остатки.
- unknown: команда не распознана.

Формат ответа строго JSON без markdown:
{
  "intent": "show_sales | find_order | create_task | show_active_tasks | show_overdue_tasks | warehouse_report | unknown",
  "parameters": {
    "period": null,
    "order_id": null,
    "employee": null,
    "task_title": null,
    "customer": null,
    "status": null
  }
}

Правила:
- Периоды возвращай на английском: january, february, march, april, may, june, july, august, september, october, november, december, current_month, all.
- Номер заказа записывай числом в order_id.
- Фамилию или имя сотрудника записывай в employee.
- Название задачи записывай в task_title.
- Статусы задач возвращай на русском: Активная, Просрочена.
- Команды добавления заказа, сотрудника, продажи и рассылки обрабатываются другим локальным модулем. Если такая команда дошла сюда и ты не уверен, верни unknown.
"""

    content = call_openrouter_chat(
        [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text},
        ],
        temperature=0.0,
    )

    if not content:
        return None

    parsed = extract_json(content)

    if parsed is None:
        return normalize_business_response(
            {"intent": "unknown", "parameters": {}},
            "unknown_command",
        )

    return normalize_business_response(parsed, fallback_reason)


def interpret_ui_command_with_cloud(
    user_text: str,
    fallback_reason: str = "local_ui_parser_and_ollama_unavailable",
) -> dict | None:
    if not user_text or not cloud_llm_enabled():
        return None

    system_prompt = f"""
Ты модуль управления web-интерфейсом нейропомощника.

Определи, является ли текст командой управления сайтом. Используй только эти возможности:
{get_ui_capabilities_json()}

Правила:
1. Не выдумывай действий, которых нет в списке.
2. Если команда относится к бизнес-данным, заказам, продажам, задачам или отчетам как к данным — верни unknown.
3. Если команда управляет страницей, темой, языком, настройкой или NLP-режимом — верни JSON.
4. Отвечай только JSON без пояснений.

Формат известной UI-команды:
{{
  "intent": "open_page | change_theme | change_language | change_setting | change_nlp_mode",
  "parameters": {{}},
  "result_text": "краткое действие на русском языке"
}}

Формат неизвестной команды:
{{
  "intent": "unknown",
  "parameters": {{}},
  "result_text": "Команда не относится к управлению интерфейсом"
}}
"""

    content = call_openrouter_chat(
        [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text},
        ],
        temperature=0.0,
    )

    parsed = extract_json(content or "")

    if not parsed or parsed.get("intent") == "unknown":
        return None

    action = validate_ui_action(parsed)

    if not action:
        return None

    action["source"] = "openrouter_ui_parser"
    action["fallback"] = True
    action["fallback_reason"] = fallback_reason

    return action


def ask_help_with_cloud(question: str, wake_word_placeholder: str) -> dict | None:
    if not question or not cloud_llm_enabled():
        return None

    system_prompt = f"""
Ты справочный помощник веб-приложения нейропомощника.
Отвечай только по уже реализованному функционалу сайта. Не придумывай команды и интеграции.
Если пользователь спрашивает, как выполнить действие, дай точную голосовую команду.
В командах всегда используй шаблон ключевого слова: {wake_word_placeholder}
Не заменяй {wake_word_placeholder} на конкретное слово: frontend сам подставит актуальное ключевое слово.

Реализованные функции:
- Навигация: открыть главную, голосовые команды, действия, заказы, задачи, отчеты, историю, настройки.
- Настройки: тема, язык, размер шрифта, режим голосового управления, NLP-режим.
- Создание через окно подтверждения: заказ, сотрудник, продажа, задача, Telegram-рассылка.
- В окне подтверждения можно менять поля голосом и сказать "добавить" или "отмена".
- Просмотр: заказ, продажи, активные задачи, просроченные задачи, складской отчет.
- График продаж по sales.
- Скачать PDF по последнему результату.
- Очистить историю команд.
- Справочный чат.

Отвечай кратко, понятно, на русском языке.
"""

    answer = call_openrouter_chat(
        [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
        temperature=0.2,
    )

    if not answer:
        return None

    return {
        "answer": answer.strip(),
        "source": "openrouter_help",
        "fallback": True,
    }
