def normalize_text(text: str) -> str:
    if not text:
        return ""

    return text.lower().strip().replace("ё", "е")


def make_ui_response(
    intent: str,
    result_text: str,
    parameters: dict | None = None,
):
    return {
        "intent": intent,
        "source": "local_ui_parser",
        "fallback": False,
        "fallback_reason": None,
        "result_text": result_text,
        "parameters": parameters or {},
        "data": [],
    }


def parse_ui_command(text: str) -> dict | None:
    """
    Локальный парсер команд управления интерфейсом.

    Важно:
    команды очистки истории стоят выше команды открытия истории,
    чтобы фраза "очисти историю" не воспринималась как "открой историю".
    """

    normalized = normalize_text(text)

    if not normalized:
        return None

    # ---------------------------------------------------------
    # Очистка истории команд
    # ВАЖНО: этот блок должен быть выше перехода на страницу "История"
    # ---------------------------------------------------------

    if (
        (
            "очист" in normalized
            or "удали" in normalized
            or "удалить" in normalized
            or "стер" in normalized
            or "сотри" in normalized
            or "убери" in normalized
        )
        and (
            "истори" in normalized
            or "последние команд" in normalized
            or "команд" in normalized
        )
    ):
        return make_ui_response(
            intent="clear_history",
            result_text="Очищаю историю команд",
        )

    # ---------------------------------------------------------
    # Навигация по страницам
    # ---------------------------------------------------------

    if (
        "главн" in normalized
        or "дашборд" in normalized
        or "dashboard" in normalized
        or "панель" in normalized
        or "открой главную" in normalized
        or "перейди на главную" in normalized
    ):
        return make_ui_response(
            intent="open_page",
            result_text="Открываю главную страницу",
            parameters={"page": "dashboard"},
        )

    if (
        "голосов" in normalized
        or "голосовые команд" in normalized
        or "voice" in normalized
        or "команды" in normalized and "голос" in normalized
    ):
        return make_ui_response(
            intent="open_page",
            result_text="Открываю раздел голосовых команд",
            parameters={"page": "voice"},
        )

    if (
        "действ" in normalized
        and (
            "открой" in normalized
            or "перейди" in normalized
            or "покажи страницу" in normalized
            or "раздел" in normalized
        )
    ):
        return make_ui_response(
            intent="open_page",
            result_text="Открываю раздел действий",
            parameters={"page": "actions"},
        )

    if (
        "заказ" in normalized
        and (
            "открой" in normalized
            or "перейди" in normalized
            or "покажи страницу" in normalized
            or "раздел" in normalized
        )
    ):
        return make_ui_response(
            intent="open_page",
            result_text="Открываю заказы",
            parameters={"page": "orders"},
        )

    if (
        "задач" in normalized
        and (
            "открой" in normalized
            or "перейди" in normalized
            or "покажи страницу" in normalized
            or "раздел" in normalized
        )
    ):
        return make_ui_response(
            intent="open_page",
            result_text="Открываю задачи",
            parameters={"page": "tasks"},
        )

    if (
        "отчет" in normalized
        and (
            "открой" in normalized
            or "перейди" in normalized
            or "покажи страницу" in normalized
            or "раздел" in normalized
        )
    ):
        return make_ui_response(
            intent="open_page",
            result_text="Открываю отчёты",
            parameters={"page": "reports"},
        )

    if (
        "истори" in normalized
        and (
            "открой" in normalized
            or "перейди" in normalized
            or "покажи" in normalized
            or "раздел" in normalized
        )
    ):
        return make_ui_response(
            intent="open_page",
            result_text="Открываю историю",
            parameters={"page": "history"},
        )

    if (
        "настройк" in normalized
        or "settings" in normalized
        or "параметр" in normalized
    ):
        return make_ui_response(
            intent="open_page",
            result_text="Открываю настройки",
            parameters={"page": "settings"},
        )

    # ---------------------------------------------------------
    # Тема интерфейса
    # ---------------------------------------------------------

    if (
        "темн" in normalized
        or "темная" in normalized
        or "темную" in normalized
        or "dark" in normalized
    ):
        return make_ui_response(
            intent="change_theme",
            result_text="Включаю тёмную тему",
            parameters={"theme": "dark"},
        )

    if (
        "светл" in normalized
        or "светлая" in normalized
        or "светлую" in normalized
        or "light" in normalized
    ):
        return make_ui_response(
            intent="change_theme",
            result_text="Включаю светлую тему",
            parameters={"theme": "light"},
        )

    # ---------------------------------------------------------
    # Язык интерфейса
    # ---------------------------------------------------------

    if (
        "английск" in normalized
        or "english" in normalized
        or "на английский" in normalized
        or "переведи сайт на английский" in normalized
    ):
        return make_ui_response(
            intent="change_language",
            result_text="Переключаю интерфейс на английский язык",
            parameters={"language": "en"},
        )

    if (
        "русск" in normalized
        or "russian" in normalized
        or "на русский" in normalized
        or "переведи сайт на русский" in normalized
    ):
        return make_ui_response(
            intent="change_language",
            result_text="Переключаю интерфейс на русский язык",
            parameters={"language": "ru"},
        )

    # ---------------------------------------------------------
    # NLP режим
    # ---------------------------------------------------------

    if (
        "ollama" in normalized
        or "оллама" in normalized
        or "основной режим" in normalized
        or "включи основной" in normalized
    ):
        return make_ui_response(
            intent="change_nlp_mode",
            result_text="Переключаю NLP на Ollama",
            parameters={"mode": "ollama"},
        )

    if (
        "local" in normalized
        or "локальный" in normalized
        or "локальныи" in normalized
        or "запасной режим" in normalized
        or "резервный режим" in normalized
        or "резервныи режим" in normalized
    ):
        return make_ui_response(
            intent="change_nlp_mode",
            result_text="Переключаю NLP на Local parser",
            parameters={"mode": "local_parser"},
        )

    # ---------------------------------------------------------
    # Режим голосовой активации
    # ---------------------------------------------------------

    if (
        ("постоян" in normalized or "ожидан" in normalized)
        and (
            "включ" in normalized
            or "активиру" in normalized
            or "запусти" in normalized
            or "сделай" in normalized
        )
    ):
        return make_ui_response(
            intent="change_setting",
            result_text="Включаю режим постоянного ожидания",
            parameters={
                "setting": "voiceActivationMode",
                "value": "wake_word",
            },
        )

    if (
        ("по кнопк" in normalized or "кнопк" in normalized)
        and (
            "включ" in normalized
            or "переключ" in normalized
            or "сделай" in normalized
        )
    ):
        return make_ui_response(
            intent="change_setting",
            result_text="Переключаю голосовое управление на режим по кнопке",
            parameters={
                "setting": "voiceActivationMode",
                "value": "button",
            },
        )

    if (
        ("ожидан" in normalized or "постоян" in normalized)
        and (
            "выключ" in normalized
            or "отключ" in normalized
            or "останов" in normalized
        )
    ):
        return make_ui_response(
            intent="change_setting",
            result_text="Выключаю режим постоянного ожидания",
            parameters={
                "setting": "voiceActivationMode",
                "value": "button",
            },
        )

    # ---------------------------------------------------------
    # Подробный вывод
    # ---------------------------------------------------------

    if (
        "подробн" in normalized
        and (
            "включ" in normalized
            or "показыв" in normalized
            or "сделай" in normalized
        )
    ):
        return make_ui_response(
            intent="change_setting",
            result_text="Включаю подробный вывод",
            parameters={
                "setting": "detailedOutput",
                "value": True,
            },
        )

    if (
        "подробн" in normalized
        and (
            "выключ" in normalized
            or "отключ" in normalized
            or "убери" in normalized
        )
    ):
        return make_ui_response(
            intent="change_setting",
            result_text="Отключаю подробный вывод",
            parameters={
                "setting": "detailedOutput",
                "value": False,
            },
        )

    # ---------------------------------------------------------
    # Техническая информация
    # ---------------------------------------------------------

    if (
        ("техническ" in normalized or "технич" in normalized)
        and (
            "включ" in normalized
            or "показыв" in normalized
            or "сделай" in normalized
        )
    ):
        return make_ui_response(
            intent="change_setting",
            result_text="Включаю отображение технической информации",
            parameters={
                "setting": "showTechInfo",
                "value": True,
            },
        )

    if (
        ("техническ" in normalized or "технич" in normalized)
        and (
            "выключ" in normalized
            or "отключ" in normalized
            or "убери" in normalized
            or "скрой" in normalized
        )
    ):
        return make_ui_response(
            intent="change_setting",
            result_text="Отключаю отображение технической информации",
            parameters={
                "setting": "showTechInfo",
                "value": False,
            },
        )

    # ---------------------------------------------------------
    # Автообновление dashboard
    # ---------------------------------------------------------

    if (
        "автообнов" in normalized
        and (
            "включ" in normalized
            or "активиру" in normalized
            or "сделай" in normalized
        )
    ):
        return make_ui_response(
            intent="change_setting",
            result_text="Включаю автообновление dashboard",
            parameters={
                "setting": "autoRefresh",
                "value": True,
            },
        )

    if (
        "автообнов" in normalized
        and (
            "выключ" in normalized
            or "отключ" in normalized
            or "убери" in normalized
        )
    ):
        return make_ui_response(
            intent="change_setting",
            result_text="Отключаю автообновление dashboard",
            parameters={
                "setting": "autoRefresh",
                "value": False,
            },
        )

    # ---------------------------------------------------------
    # Подтверждение действий
    # ---------------------------------------------------------

    if (
        "подтвержд" in normalized
        and (
            "включ" in normalized
            or "активиру" in normalized
            or "сделай" in normalized
        )
    ):
        return make_ui_response(
            intent="change_setting",
            result_text="Включаю подтверждение действий",
            parameters={
                "setting": "confirmActions",
                "value": True,
            },
        )

    if (
        "подтвержд" in normalized
        and (
            "выключ" in normalized
            or "отключ" in normalized
            or "убери" in normalized
        )
    ):
        return make_ui_response(
            intent="change_setting",
            result_text="Отключаю подтверждение действий",
            parameters={
                "setting": "confirmActions",
                "value": False,
            },
        )

    # ---------------------------------------------------------
    # Размер шрифта
    # ---------------------------------------------------------

    if (
        ("шрифт" in normalized or "текст" in normalized)
        and (
            "крупнее" in normalized
            or "больше" in normalized
            or "увелич" in normalized
            or "large" in normalized
            or "bigger" in normalized
        )
    ):
        return make_ui_response(
            intent="change_setting",
            result_text="Увеличиваю размер шрифта",
            parameters={
                "setting": "fontSize",
                "value": "large",
            },
        )

    if (
        ("шрифт" in normalized or "текст" in normalized)
        and (
            "меньше" in normalized
            or "уменьш" in normalized
            or "small" in normalized
            or "smaller" in normalized
        )
    ):
        return make_ui_response(
            intent="change_setting",
            result_text="Уменьшаю размер шрифта",
            parameters={
                "setting": "fontSize",
                "value": "small",
            },
        )

    if (
        ("шрифт" in normalized or "текст" in normalized)
        and (
            "обычный" in normalized
            or "нормальный" in normalized
            or "стандартный" in normalized
            or "normal" in normalized
        )
    ):
        return make_ui_response(
            intent="change_setting",
            result_text="Возвращаю стандартный размер шрифта",
            parameters={
                "setting": "fontSize",
                "value": "normal",
            },
        )

    # ---------------------------------------------------------
    # Компактный режим
    # ---------------------------------------------------------

    if (
        "компакт" in normalized
        and (
            "включ" in normalized
            or "сделай" in normalized
            or "enable" in normalized
        )
    ):
        return make_ui_response(
            intent="change_setting",
            result_text="Включаю компактный режим",
            parameters={
                "setting": "compactMode",
                "value": True,
            },
        )

    if (
        "компакт" in normalized
        and (
            "выключ" in normalized
            or "отключ" in normalized
            or "disable" in normalized
        )
    ):
        return make_ui_response(
            intent="change_setting",
            result_text="Выключаю компактный режим",
            parameters={
                "setting": "compactMode",
                "value": False,
            },
        )

    # ---------------------------------------------------------
    # Анимации
    # ---------------------------------------------------------

    if (
        "анимац" in normalized
        and (
            "выключ" in normalized
            or "отключ" in normalized
            or "disable" in normalized
        )
    ):
        return make_ui_response(
            intent="change_setting",
            result_text="Отключаю анимации интерфейса",
            parameters={
                "setting": "animations",
                "value": False,
            },
        )

    if (
        "анимац" in normalized
        and (
            "включ" in normalized
            or "enable" in normalized
        )
    ):
        return make_ui_response(
            intent="change_setting",
            result_text="Включаю анимации интерфейса",
            parameters={
                "setting": "animations",
                "value": True,
            },
        )

    # ---------------------------------------------------------
    # Период отчёта по умолчанию
    # ---------------------------------------------------------

    if (
        ("период отчет" in normalized or "период отчета" in normalized)
        and "месяц" in normalized
    ):
        return make_ui_response(
            intent="change_setting",
            result_text="Устанавливаю период отчета по умолчанию за месяц",
            parameters={
                "setting": "defaultReportPeriod",
                "value": "month",
            },
        )

    if (
        ("период отчет" in normalized or "период отчета" in normalized)
        and ("квартал" in normalized or "quarter" in normalized)
    ):
        return make_ui_response(
            intent="change_setting",
            result_text="Устанавливаю период отчета по умолчанию за квартал",
            parameters={
                "setting": "defaultReportPeriod",
                "value": "quarter",
            },
        )

    if (
        ("период отчет" in normalized or "период отчета" in normalized)
        and ("год" in normalized or "year" in normalized)
    ):
        return make_ui_response(
            intent="change_setting",
            result_text="Устанавливаю период отчета по умолчанию за год",
            parameters={
                "setting": "defaultReportPeriod",
                "value": "year",
            },
        )
        # ---------------------------------------------------------
    # Скачать PDF
    # ---------------------------------------------------------

    if (
        ("скачай" in normalized or "скачать" in normalized or "загрузи" in normalized or "download" in normalized)
        and ("pdf" in normalized or "пдф" in normalized or "пдф файл" in normalized)
    ):
        return make_ui_response(
            intent="download_pdf",
            result_text="Скачиваю PDF-отчёт",
            parameters={},
        )
        # ---------------------------------------------------------
    # Построить график
    # ---------------------------------------------------------

    if (
        ("построй" in normalized or "построи" in normalized or "создай" in normalized or "сформируй" in normalized)
        and ("график" in normalized or "диаграм" in normalized or "chart" in normalized)
    ):
        return make_ui_response(
            intent="build_chart",
            result_text="Строю график продаж",
            parameters={},
        )
        # ---------------------------------------------------------
    # Открыть справочный чат
    # ---------------------------------------------------------

    if (
        ("помощ" in normalized or "справк" in normalized or "help" in normalized)
        and (
            "открой" in normalized
            or "покажи" in normalized
            or "открыть" in normalized
            or "нужна" in normalized
        )
    ):
        return make_ui_response(
            intent="open_help",
            result_text="Открываю справочный чат",
            parameters={},
        )

    # ---------------------------------------------------------
    # Вопрос в справочный чат
    # ---------------------------------------------------------

    if (
        normalized.startswith("как ")
        or normalized.startswith("что ")
        or normalized.startswith("какие ")
        or normalized.startswith("зачем ")
        or normalized.startswith("почему ")
        or "как добавить" in normalized
        or "как создать" in normalized
        or "как скачать" in normalized
        or "как построить" in normalized
        or "какие команды" in normalized
    ):
        return make_ui_response(
            intent="help_question",
            result_text="Открываю справочный чат и ищу подсказку",
            parameters={
                "question": text,
            },
        )

    return None
