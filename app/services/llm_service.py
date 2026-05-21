import os
import re
import json
import requests
from typing import Any
from dotenv import load_dotenv

from app.services.cloud_llm_service import interpret_command_with_cloud

load_dotenv()


LLM_PROVIDER = os.getenv("LLM_PROVIDER", "hybrid").lower().strip()
LOCAL_PARSER_ENABLED = os.getenv("LOCAL_PARSER_ENABLED", "true").lower().strip() in {
    "1",
    "true",
    "yes",
    "on",
    "да",
}
OLLAMA_ENABLED = os.getenv("OLLAMA_ENABLED", "true").lower().strip() in {
    "1",
    "true",
    "yes",
    "on",
    "да",
}
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:1.5b")
try:
    OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "8"))
except Exception:
    OLLAMA_TIMEOUT = 8


def interpret_command(user_text: str) -> dict[str, Any]:
    """
    Главная функция интерпретации команды:
    Local parser -> Ollama -> OpenRouter -> fallback.
    """

    fallback_reasons: list[str] = []

    if LOCAL_PARSER_ENABLED:
        try:
            local_result = interpret_with_local_parser(user_text)

            if local_result.get("intent") != "unknown":
                return local_result

            fallback_reasons.append("local_parser_unknown")
        except Exception as error:
            fallback_reasons.append(f"local_parser_error: {error}")

    if OLLAMA_ENABLED and OLLAMA_URL and is_ollama_available():
        try:
            ollama_result = interpret_with_ollama(user_text)

            if ollama_result.get("intent") != "unknown":
                if fallback_reasons:
                    ollama_result["fallback"] = True
                    ollama_result["fallback_reason"] = "local_parser_unknown"

                return ollama_result

            fallback_reasons.append("ollama_unknown")
        except Exception as error:
            fallback_reasons.append(f"ollama_error: {error}")
    else:
        fallback_reasons.append("ollama_unavailable")

    cloud_reason = "local_parser_and_ollama_unavailable"

    if "ollama_unknown" in fallback_reasons:
        cloud_reason = "local_parser_and_ollama_unknown"

    cloud_result = interpret_command_with_cloud(
        user_text,
        fallback_reason=cloud_reason,
    )

    if cloud_result:
        return cloud_result

    return {
        "intent": "unknown",
        "parameters": empty_parameters(),
        "source": "hybrid_fallback",
        "fallback": True,
        "fallback_reason": "; ".join(fallback_reasons) or "all_llm_unavailable",
    }


def is_ollama_available() -> bool:
    if not OLLAMA_ENABLED or not OLLAMA_URL:
        return False

    try:
        response = requests.get(
            f"{OLLAMA_URL}/api/tags",
            timeout=OLLAMA_TIMEOUT,
        )
        return response.status_code < 400
    except Exception:
        return False


def empty_parameters() -> dict[str, Any]:
    return {
        "period": None,
        "order_id": None,
        "employee": None,
        "task_title": None,
        "customer": None,
        "status": None
    }


def interpret_with_local_parser(user_text: str) -> dict[str, Any]:
    """
    Резервный локальный NLP-парсер.
    Работает без интернета, OpenAI и Ollama.
    """

    text = user_text.lower().strip()
    parameters = empty_parameters()

    order_match = re.search(
        r"(?:заказ|заказа|заказ номер|номер заказа)\s*(\d+)",
        text
    )

    if order_match and any(word in text for word in ["покажи", "найди", "открой", "посмотри"]):
        parameters["order_id"] = int(order_match.group(1))
        return {
            "intent": "find_order",
            "parameters": parameters,
            "source": "local_parser"
        }

    if "продаж" in text or "выручк" in text:
        if "январ" in text:
            parameters["period"] = "january"
        elif "феврал" in text:
            parameters["period"] = "february"
        elif "март" in text:
            parameters["period"] = "march"
        elif "апрел" in text:
            parameters["period"] = "april"
        elif "май" in text:
            parameters["period"] = "may"
        elif "июн" in text:
            parameters["period"] = "june"
        elif "июл" in text:
            parameters["period"] = "july"
        elif "август" in text:
            parameters["period"] = "august"
        elif "сентябр" in text:
            parameters["period"] = "september"
        elif "октябр" in text:
            parameters["period"] = "october"
        elif "ноябр" in text:
            parameters["period"] = "november"
        elif "декабр" in text:
            parameters["period"] = "december"
        elif "месяц" in text:
            parameters["period"] = "current_month"
        else:
            parameters["period"] = "all"

        return {
            "intent": "show_sales",
            "parameters": parameters,
            "source": "local_parser"
        }

    if "актив" in text and "задач" in text:
        parameters["status"] = "Активная"
        return {
            "intent": "show_active_tasks",
            "parameters": parameters,
            "source": "local_parser"
        }

    if "просроч" in text and "задач" in text:
        parameters["status"] = "Просрочена"
        return {
            "intent": "show_overdue_tasks",
            "parameters": parameters,
            "source": "local_parser"
        }

    create_words = ["создай", "добавь", "поставь", "назначь"]

    if any(word in text for word in create_words) and "задач" in text:
        employee_match = re.search(
            r"(?:менеджеру|сотруднику)?\s*(иванову|петрову|сидорову|[а-яё]+ову|[а-яё]+еву|[а-яё]+ину)",
            text
        )

        if employee_match:
            raw_employee = employee_match.group(1)
            employee = normalize_employee_name(raw_employee)

            task_title = text

            for word in create_words:
                task_title = task_title.replace(word, "")

            task_title = task_title.replace("задачу", "")
            task_title = task_title.replace("менеджеру", "")
            task_title = task_title.replace("сотруднику", "")
            task_title = task_title.replace(raw_employee, "")
            task_title = task_title.strip()

            parameters["employee"] = employee
            parameters["task_title"] = task_title.capitalize() if task_title else "Новая задача"

            return {
                "intent": "create_task",
                "parameters": parameters,
                "source": "local_parser"
            }

    if "склад" in text or "остат" in text:
        return {
            "intent": "warehouse_report",
            "parameters": parameters,
            "source": "local_parser"
        }

    return {
        "intent": "unknown",
        "parameters": parameters,
        "source": "local_parser"
    }


def normalize_employee_name(name: str) -> str:
    """
    Упрощённая нормализация ФИО из дательного падежа.
    """

    mapping = {
        "иванову": "Иванов",
        "петрову": "Петров",
        "сидорову": "Сидоров",
    }

    if name in mapping:
        return mapping[name]

    if name.endswith("ову") or name.endswith("еву") or name.endswith("ину"):
        return name[:-1].capitalize()

    return name.capitalize()


def interpret_with_ollama(user_text: str) -> dict[str, Any]:
    """
    Интерпретация команды через локальную LLM Ollama.
    Ollama должен быть запущен локально.
    """

    prompt = f"""
Ты NLP-модуль русскоязычного бизнес-помощника.

Твоя задача — преобразовать пользовательский запрос в JSON.

Верни строго JSON без markdown и без пояснений.

Доступные intent:
- show_sales
- find_order
- create_task
- show_active_tasks
- show_overdue_tasks
- warehouse_report
- unknown

Формат ответа:
{{
  "intent": "find_order",
  "parameters": {{
    "period": null,
    "order_id": 152,
    "employee": null,
    "task_title": null,
    "customer": null,
    "status": null
  }}
}}

Правила:
- Если пользователь просит найти или показать заказ, intent = find_order.
- Если пользователь просит продажи или выручку, intent = show_sales.
- Если пользователь просит создать, добавить, поставить или назначить задачу, intent = create_task.
- Если пользователь просит активные задачи, intent = show_active_tasks.
- Если пользователь просит просроченные задачи, intent = show_overdue_tasks.
- Если пользователь просит склад или остатки, intent = warehouse_report.
- Если номер заказа есть в тексте, запиши его в order_id.
- Если есть сотрудник, запиши фамилию в employee.
- Если есть текст задачи, запиши его в task_title.
- Периоды возвращай на английском: march, april, current_month, all.
- Статусы возвращай на русском: Активная, Просрочена, В обработке.

Запрос пользователя:
{user_text}
"""

    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "format": "json"
        },
        timeout=OLLAMA_TIMEOUT
    )

    response.raise_for_status()

    data = response.json()
    raw_response = data.get("response", "")

    parsed = json.loads(raw_response)

    if "intent" not in parsed:
        parsed["intent"] = "unknown"

    if "parameters" not in parsed:
        parsed["parameters"] = empty_parameters()

    # На всякий случай дополняем отсутствующие параметры
    default_params = empty_parameters()
    default_params.update(parsed.get("parameters", {}))
    parsed["parameters"] = default_params

    parsed["source"] = "ollama"

    return parsed
