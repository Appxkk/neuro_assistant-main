import re
from datetime import datetime, timedelta


def normalize_text(text: str) -> str:
    return text.lower().strip().replace("ё", "е")


def parse_amount(text: str) -> int | None:
    """
    Достаёт сумму из текста:
    - 15000
    - 15 000
    - 15.000
    - 15,000
    - на сумму 15000
    """

    patterns = [
        r"(?:на\s+сумму|сумма|стоимостью|стоимость|на)\s+([0-9][0-9\s\.,]{0,30})",
        r"([0-9][0-9\s\.,]{2,30})",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if not match:
            continue

        raw_amount = match.group(1)
        digits_only = re.sub(r"\D", "", raw_amount)

        if not digits_only:
            continue

        try:
            return int(digits_only)
        except ValueError:
            continue

    return None


def parse_number_after_keywords(text: str, keywords: list[str]) -> int | None:
    keywords_pattern = "|".join(keywords)

    match = re.search(
        rf"(?:{keywords_pattern})\s+([0-9]+)",
        text,
        re.IGNORECASE,
    )

    if not match:
        return None

    try:
        return int(match.group(1))
    except ValueError:
        return None


def parse_customer_name(text: str) -> str:
    customer_match = re.search(
        r"(?:клиента|клиенту|для клиента)\s+(.+?)(?:\s+на\s+сумму|\s+сумма|\s+стоимостью|\s+стоимость|\s+на\s+[0-9]|$)",
        text,
        re.IGNORECASE,
    )

    if customer_match:
        customer_name = customer_match.group(1).strip()
    else:
        customer_name = "Неизвестный клиент"

    customer_name = re.sub(r"[^а-яА-Яa-zA-Z0-9\s\-]", "", customer_name)
    customer_name = re.sub(r"\s+", " ", customer_name).strip()

    if not customer_name:
        customer_name = "Неизвестный клиент"

    return customer_name.title()


def parse_create_order_command(text: str) -> dict | None:
    """
    Команды:
    - добавь заказ клиента Иванов на сумму 15000
    - создай заказ для клиента Альфа на сумму 25000
    """

    if not text:
        return None

    normalized = normalize_text(text)

    if not (
        ("добав" in normalized or "созда" in normalized)
        and "заказ" in normalized
    ):
        return None

    # Чтобы команда "добавь продажу по заказу 1" не считалась созданием заказа
    if "продаж" in normalized:
        return None

    amount = parse_amount(normalized)

    if amount is None:
        return None

    customer_name = parse_customer_name(normalized)

    return {
        "intent": "confirm_action",
        "source": "local_action_parser",
        "fallback": False,
        "fallback_reason": None,
        "result_text": "Требуется подтверждение добавления заказа",
        "parameters": {
            "action": "create_order",
            "payload": {
                "customer_name": customer_name,
                "amount": amount,
                "status": "Новый",
            },
        },
        "data": [],
    }


def parse_employee_name(text: str) -> str | None:
    """
    Достаёт ФИО сотрудника:
    - добавь сотрудника Сергеев Сергей должность Менеджер отдел Продажи
    """

    match = re.search(
        r"(?:сотрудника|работника)\s+(.+?)(?:\s+должность|\s+на должность|\s+отдел|$)",
        text,
        re.IGNORECASE,
    )

    if not match:
        return None

    full_name = match.group(1).strip()
    full_name = re.sub(r"[^а-яА-Яa-zA-Z\s\-]", "", full_name)
    full_name = re.sub(r"\s+", " ", full_name).strip()

    if not full_name:
        return None

    return full_name.title()


def parse_position(text: str) -> str:
    match = re.search(
        r"(?:должность|на должность)\s+(.+?)(?:\s+отдел|$)",
        text,
        re.IGNORECASE,
    )

    if not match:
        return "Менеджер"

    position = match.group(1).strip()
    position = re.sub(r"[^а-яА-Яa-zA-Z\s\-]", "", position)
    position = re.sub(r"\s+", " ", position).strip()

    return position.title() if position else "Менеджер"


def parse_department(text: str) -> str:
    match = re.search(
        r"(?:отдел|департамент)\s+(.+?)$",
        text,
        re.IGNORECASE,
    )

    if not match:
        return "Продажи"

    department = match.group(1).strip()
    department = re.sub(r"[^а-яА-Яa-zA-Z\s\-]", "", department)
    department = re.sub(r"\s+", " ", department).strip()

    return department.title() if department else "Продажи"


def parse_create_employee_command(text: str) -> dict | None:
    """
    Команды:
    - добавь сотрудника Сергеев Сергей должность Менеджер отдел Продажи
    - создай сотрудника Иванов Иван
    """

    if not text:
        return None

    normalized = normalize_text(text)

    if not (
        ("добав" in normalized or "созда" in normalized)
        and ("сотрудник" in normalized or "работник" in normalized)
    ):
        return None

    full_name = parse_employee_name(text)

    if not full_name:
        return None

    position = parse_position(text)
    department = parse_department(text)

    return {
        "intent": "confirm_action",
        "source": "local_action_parser",
        "fallback": False,
        "fallback_reason": None,
        "result_text": "Требуется подтверждение добавления сотрудника",
        "parameters": {
            "action": "create_employee",
            "payload": {
                "full_name": full_name,
                "position": position,
                "department": department,
            },
        },
        "data": [],
    }


def parse_product_name(text: str) -> str:
    """
    Достаёт товар:
    - товар Клавиатура Logitech количество 2
    - продукт Ноутбук Lenovo количество 3
    - продажу Клавиатура Logitech количество 2
    """

    match = re.search(
        r"(?:товар|продукт)\s+(.+?)(?:\s+количество|\s+кол-во|\s+[0-9]+\s*(?:штук|штуки|шт)|\s+на\s+сумму|\s+сумма|$)",
        text,
        re.IGNORECASE,
    )

    if not match:
        match = re.search(
            r"продаж[ауи]?\s+(.+?)(?:\s+по\s+заказу|\s+количество|\s+кол-во|\s+[0-9]+\s*(?:штук|штуки|шт)|\s+на\s+сумму|\s+сумма|$)",
            text,
            re.IGNORECASE,
        )

    if match:
        product_name = match.group(1).strip()
    else:
        product_name = "Новый товар"

    product_name = re.sub(r"[^а-яА-Яa-zA-Z0-9\s\-]", "", product_name)
    product_name = re.sub(r"\s+", " ", product_name).strip()

    return product_name.title() if product_name else "Новый товар"


def parse_quantity(text: str) -> int:
    match = re.search(
        r"(?:количество|кол-во)\s+([0-9]+)",
        text,
        re.IGNORECASE,
    )

    if not match:
        match = re.search(
            r"([0-9]+)\s+(?:штук|штуки|шт)",
            text,
            re.IGNORECASE,
        )

    if not match:
        return 1

    try:
        return int(match.group(1))
    except ValueError:
        return 1


def parse_order_id(text: str) -> int | None:
    return parse_number_after_keywords(text, ["заказу", "заказ", "order"])


def parse_create_sale_command(text: str) -> dict | None:
    """
    Команды:
    - добавь продажу по заказу 6 товар Клавиатура Logitech количество 2 на сумму 9000
    - создай продажу товар Ноутбук Lenovo количество 1 сумма 50000
    """

    if not text:
        return None

    normalized = normalize_text(text)

    if not (
        ("добав" in normalized or "созда" in normalized)
        and "продаж" in normalized
    ):
        return None

    product_name = parse_product_name(text)
    quantity = parse_quantity(normalized)
    total_price = parse_amount(normalized)
    order_id = parse_order_id(normalized)

    if total_price is None:
        total_price = 0

    return {
        "intent": "confirm_action",
        "source": "local_action_parser",
        "fallback": False,
        "fallback_reason": None,
        "result_text": "Требуется подтверждение добавления продажи",
        "parameters": {
            "action": "create_sale",
            "payload": {
                "order_id": order_id,
                "product_name": product_name,
                "quantity": quantity,
                "total_price": total_price,
                "sale_date": datetime.utcnow().date().isoformat(),
            },
        },
        "data": [],
    }


def parse_deadline(text: str) -> str:
    normalized = normalize_text(text)

    now = datetime.utcnow()

    if "сегодня" in normalized:
        return now.isoformat()

    if "завтра" in normalized:
        return (now + timedelta(days=1)).isoformat()

    if "послезавтра" in normalized:
        return (now + timedelta(days=2)).isoformat()

    date_match = re.search(
        r"(\d{4}-\d{2}-\d{2})",
        text,
        re.IGNORECASE,
    )

    if date_match:
        try:
            return datetime.fromisoformat(date_match.group(1)).isoformat()
        except ValueError:
            pass

    return (now + timedelta(days=1)).isoformat()


def parse_priority(text: str) -> str:
    normalized = normalize_text(text)

    if "высок" in normalized:
        return "Высокий"

    if "низк" in normalized:
        return "Низкий"

    return "Средний"


def parse_task_title(text: str) -> str | None:
    """
    Достаёт название задачи:
    - создай задачу подготовить отчет
    - добавь задачу связаться с клиентом описание ...
    """

    match = re.search(
        r"(?:создай|создать|добавь|добавить)\s+задачу\s+(.+?)(?:\s+описание|\s+исполнитель|\s+сотрудник|\s+приоритет|\s+срок|\s+до\s+завтра|$)",
        text,
        re.IGNORECASE,
    )

    if not match:
        return None

    title = match.group(1).strip()
    title = re.sub(r"\s+", " ", title).strip()

    if not title:
        return None

    return title[0].upper() + title[1:]


def parse_task_description(text: str) -> str:
    match = re.search(
        r"описание\s+(.+?)(?:\s+исполнитель|\s+сотрудник|\s+приоритет|\s+срок|$)",
        text,
        re.IGNORECASE,
    )

    if not match:
        return ""

    description = match.group(1).strip()
    description = re.sub(r"\s+", " ", description).strip()

    return description


def parse_employee_id_from_task(text: str) -> int | None:
    return parse_number_after_keywords(text, ["исполнитель", "сотрудник", "работник"])


def parse_create_task_command(text: str) -> dict | None:
    """
    Команды:
    - создай задачу подготовить отчет
    - создай задачу связаться с клиентом описание Уточнить оплату исполнитель 1 приоритет высокий
    """

    if not text:
        return None

    normalized = normalize_text(text)

    if not (
        ("добав" in normalized or "созда" in normalized)
        and "задач" in normalized
    ):
        return None

    title = parse_task_title(text)

    if not title:
        return None

    description = parse_task_description(text)
    employee_id = parse_employee_id_from_task(normalized)
    priority = parse_priority(normalized)
    deadline = parse_deadline(normalized)

    return {
        "intent": "confirm_action",
        "source": "local_action_parser",
        "fallback": False,
        "fallback_reason": None,
        "result_text": "Требуется подтверждение создания задачи",
        "parameters": {
            "action": "create_task",
            "payload": {
                "title": title,
                "description": description,
                "employee_id": employee_id,
                "status": "Активная",
                "priority": priority,
                "deadline": deadline,
            },
        },
        "data": [],
    }


def parse_send_mailing_command(text: str) -> dict | None:
    """
    Команды:
    - сделай рассылку
    - надо сделать рассылку
    - подготовь рассылку в телеграм
    """

    if not text:
        return None

    normalized = normalize_text(text)

    if "рассыл" not in normalized:
        return None

    if not any(
        word in normalized
        for word in ["сдел", "созда", "подготов", "отправ", "надо", "нужно"]
    ):
        return None

    channels = []

    if "телеграм" in normalized or "telegram" in normalized or "тг" in normalized:
        channels.append("telegram")

    return {
        "intent": "confirm_action",
        "source": "local_action_parser",
        "fallback": False,
        "fallback_reason": None,
        "result_text": "Требуется подтверждение отправки рассылки",
        "parameters": {
            "action": "send_mailing",
            "payload": {
                "channels": channels,
                "message": "",
            },
        },
        "data": [],
    }


def parse_pending_action_command(text: str) -> dict | None:
    """
    Общий парсер действий, которые меняют БД.
    """

    parsers = [
        parse_create_order_command,
        parse_create_employee_command,
        parse_create_sale_command,
        parse_create_task_command,
        parse_send_mailing_command,
    ]

    for parser in parsers:
        result = parser(text)

        if result:
            return result

    return None
