import json


UI_CAPABILITIES = {
    "description": "Возможности web-интерфейса нейропомощника",
    "pages": {
        "dashboard": "Главная панель управления",
        "voice": "Раздел голосовых команд",
        "actions": "Раздел ручного запуска действий",
        "orders": "Раздел заказов",
        "tasks": "Раздел задач",
        "reports": "Раздел отчетов",
        "history": "История команд",
        "settings": "Настройки системы"
    },
    "themes": {
        "light": "Светлая тема",
        "dark": "Темная тема"
    },
    "languages": {
        "ru": "Русский интерфейс",
        "en": "Английский интерфейс"
    },
    "nlp_modes": {
        "ollama": "Основной режим обработки через Ollama",
        "local_parser": "Резервный локальный парсер"
    },
    "settings": {
        "detailedOutput": {
            "type": "boolean",
            "description": "Показывать подробный вывод результата"
        },
        "showTechInfo": {
            "type": "boolean",
            "description": "Показывать техническую информацию: источник, intent, параметры"
        },
        "autoRefresh": {
            "type": "boolean",
            "description": "Автоматически обновлять dashboard"
        },
        "saveHistory": {
            "type": "boolean",
            "description": "Сохранять историю команд"
        },
        "confirmActions": {
            "type": "boolean",
            "description": "Запрашивать подтверждение перед изменением данных"
        },
        "voiceActivationMode": {
            "type": "enum",
            "values": ["button", "wake_word"],
            "description": "Режим голосового управления: по кнопке или постоянное ожидание"
        },
        "wakeWord": {
            "type": "string",
            "description": "Ключевое слово для активации ассистента"
        },
        "speechLanguage": {
            "type": "enum",
            "values": ["ru", "en", "auto"],
            "description": "Язык распознавания речи"
        },
        "fontSize": {
            "type": "enum",
            "values": ["small", "normal", "large"],
            "description": "Размер шрифта интерфейса"
        },
        "compactMode": {
            "type": "boolean",
            "description": "Компактный режим интерфейса"
        },
        "animations": {
            "type": "boolean",
            "description": "Анимации интерфейса"
        },
        "refreshInterval": {
            "type": "integer",
            "min": 5,
            "max": 300,
            "description": "Интервал автообновления dashboard в секундах"
        },
        "defaultReportPeriod": {
            "type": "enum",
            "values": ["month", "quarter", "year"],
            "description": "Период отчета по умолчанию"
        },
        "exportFormat": {
            "type": "enum",
            "values": ["pdf", "xlsx", "csv"],
            "description": "Формат экспорта отчетов"
        }
    },
    "allowed_intents": [
        "open_page",
        "change_theme",
        "change_language",
        "change_setting",
        "change_nlp_mode"
    ]
}


def get_ui_capabilities_json() -> str:
    return json.dumps(UI_CAPABILITIES, ensure_ascii=False, indent=2)


def normalize_boolean(value):
    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        value = value.lower().strip()

        if value in ["true", "1", "yes", "да", "включить", "включи", "on"]:
            return True

        if value in ["false", "0", "no", "нет", "выключить", "выключи", "off"]:
            return False

    return None


def validate_ui_action(action: dict) -> dict | None:
    if not isinstance(action, dict):
        return None

    intent = action.get("intent")
    parameters = action.get("parameters") or {}

    if intent not in UI_CAPABILITIES["allowed_intents"]:
        return None

    if intent == "open_page":
        page = parameters.get("page")

        if page not in UI_CAPABILITIES["pages"]:
            return None

    elif intent == "change_theme":
        theme = parameters.get("theme")

        if theme not in UI_CAPABILITIES["themes"]:
            return None

    elif intent == "change_language":
        language = parameters.get("language")

        if language not in UI_CAPABILITIES["languages"]:
            return None

    elif intent == "change_nlp_mode":
        mode = parameters.get("mode")

        if mode not in UI_CAPABILITIES["nlp_modes"]:
            return None

    elif intent == "change_setting":
        setting = parameters.get("setting")

        if setting not in UI_CAPABILITIES["settings"]:
            return None

        setting_config = UI_CAPABILITIES["settings"][setting]
        setting_type = setting_config["type"]
        value = parameters.get("value")

        if setting_type == "boolean":
            normalized_value = normalize_boolean(value)

            if normalized_value is None:
                return None

            parameters["value"] = normalized_value

        elif setting_type == "enum":
            if value not in setting_config["values"]:
                return None

        elif setting_type == "integer":
            try:
                value = int(value)
            except Exception:
                return None

            min_value = setting_config.get("min")
            max_value = setting_config.get("max")

            if min_value is not None and value < min_value:
                return None

            if max_value is not None and value > max_value:
                return None

            parameters["value"] = value

        elif setting_type == "string":
            if value is None or str(value).strip() == "":
                return None

            parameters["value"] = str(value).strip()

    result_text = action.get("result_text") or "Выполняю команду интерфейса"

    return {
        "intent": intent,
        "source": "ollama_ui_parser",
        "fallback": False,
        "fallback_reason": None,
        "result_text": result_text,
        "parameters": parameters,
        "data": []
    }
