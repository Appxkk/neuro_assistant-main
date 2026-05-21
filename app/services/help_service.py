import os
import httpx
from dotenv import load_dotenv


load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:1.5b")


WAKE_WORD_PLACEHOLDER = "{wake_word}"


def normalize_text(text: str) -> str:
    if not text:
        return ""

    return text.lower().strip().replace("ё", "е")


def make_help_response(answer: str, source: str = "local_help_parser"):
    return {
        "answer": answer,
        "source": source,
        "fallback": source != "local_help_parser",
    }


def get_all_commands_answer() -> str:
    return f"""Вот основные команды ассистента:

1. Добавить заказ:
«{WAKE_WORD_PLACEHOLDER}, добавь заказ клиента Ромашка на сумму 25000»

2. Добавить сотрудника или менеджера:
«{WAKE_WORD_PLACEHOLDER}, добавь сотрудника Иванов Иван должность Менеджер отдел Продажи»

3. Добавить продажу:
«{WAKE_WORD_PLACEHOLDER}, добавь продажу по заказу 1 товар Мышь Logitech количество 2 на сумму 5000»

4. Создать задачу:
«{WAKE_WORD_PLACEHOLDER}, создай задачу подготовить отчёт описание Сделать отчёт за месяц исполнитель 1 приоритет высокий»

5. Построить график:
«{WAKE_WORD_PLACEHOLDER}, построи график»

6. Скачать PDF:
«{WAKE_WORD_PLACEHOLDER}, скачай PDF»

7. Очистить историю:
«{WAKE_WORD_PLACEHOLDER}, очисти историю»

8. Навигация:
«{WAKE_WORD_PLACEHOLDER}, открой настройки»
«{WAKE_WORD_PLACEHOLDER}, открой заказы»
«{WAKE_WORD_PLACEHOLDER}, открой задачи»
«{WAKE_WORD_PLACEHOLDER}, открой отчёты»
«{WAKE_WORD_PLACEHOLDER}, открой историю»

9. Управление интерфейсом:
«{WAKE_WORD_PLACEHOLDER}, включи тёмную тему»
«{WAKE_WORD_PLACEHOLDER}, включи светлую тему»
«{WAKE_WORD_PLACEHOLDER}, переведи сайт на английский»
«{WAKE_WORD_PLACEHOLDER}, переведи сайт на русский»"""


def get_local_help_answer(question: str) -> dict | None:
    normalized = normalize_text(question)

    if not normalized:
        return make_help_response(
            "Введите вопрос, например: «Как добавить заказ?»"
        )

    # ---------------------------------------------------------
    # Все команды
    # ---------------------------------------------------------

    if (
        "все команд" in normalized
        or "какие команд" in normalized
        or "список команд" in normalized
        or "что ты умеешь" in normalized
        or "что умеет" in normalized
        or "доступные команд" in normalized
    ):
        return make_help_response(get_all_commands_answer())

    # ---------------------------------------------------------
    # Добавление заказа
    # ---------------------------------------------------------

    if (
        "заказ" in normalized
        and (
            "добав" in normalized
            or "созд" in normalized
            or "оформ" in normalized
            or "как" in normalized
        )
    ):
        return make_help_response(
            f"""Чтобы добавить заказ, скажите:

«{WAKE_WORD_PLACEHOLDER}, добавь заказ клиента Ромашка на сумму 25000»

После этого откроется окно подтверждения. В нём можно изменить данные голосом:

«{WAKE_WORD_PLACEHOLDER}, клиент ООО Альфа»
«{WAKE_WORD_PLACEHOLDER}, сумма 50000»
«{WAKE_WORD_PLACEHOLDER}, статус в обработке»
«{WAKE_WORD_PLACEHOLDER}, менеджер Иванов»

Чтобы сохранить запись, скажите:
«{WAKE_WORD_PLACEHOLDER}, добавить»

Чтобы отменить:
«{WAKE_WORD_PLACEHOLDER}, отмена»"""
        )

    # ---------------------------------------------------------
    # Добавление менеджера
    # ---------------------------------------------------------

    if (
        "менеджер" in normalized
        and (
            "добав" in normalized
            or "созд" in normalized
            or "как" in normalized
            or "нов" in normalized
        )
    ):
        return make_help_response(
            f"""Менеджер добавляется через таблицу сотрудников.

Скажите:

«{WAKE_WORD_PLACEHOLDER}, добавь сотрудника Иванов Иван должность Менеджер отдел Продажи»

После открытия окна подтверждения можно изменить поля:

«{WAKE_WORD_PLACEHOLDER}, ФИО Петров Пётр»
«{WAKE_WORD_PLACEHOLDER}, должность Менеджер»
«{WAKE_WORD_PLACEHOLDER}, отдел Продажи»

Для сохранения скажите:
«{WAKE_WORD_PLACEHOLDER}, добавить»

Для отмены:
«{WAKE_WORD_PLACEHOLDER}, отмена»"""
        )

    # ---------------------------------------------------------
    # Добавление сотрудника
    # ---------------------------------------------------------

    if (
        "сотрудник" in normalized
        and (
            "добав" in normalized
            or "созд" in normalized
            or "как" in normalized
            or "нов" in normalized
        )
    ):
        return make_help_response(
            f"""Чтобы добавить сотрудника, скажите:

«{WAKE_WORD_PLACEHOLDER}, добавь сотрудника Сергеев Сергей должность Аналитик отдел Отчёты»

После открытия окна можно изменить данные:

«{WAKE_WORD_PLACEHOLDER}, ФИО Петров Пётр»
«{WAKE_WORD_PLACEHOLDER}, должность Аналитик»
«{WAKE_WORD_PLACEHOLDER}, отдел Отчёты»

Для сохранения:
«{WAKE_WORD_PLACEHOLDER}, добавить»

Для отмены:
«{WAKE_WORD_PLACEHOLDER}, отмена»"""
        )

    # ---------------------------------------------------------
    # Добавление продажи
    # ---------------------------------------------------------

    if (
        "продаж" in normalized
        and (
            "добав" in normalized
            or "созд" in normalized
            or "как" in normalized
            or "нов" in normalized
        )
    ):
        return make_help_response(
            f"""Чтобы добавить продажу, скажите:

«{WAKE_WORD_PLACEHOLDER}, добавь продажу по заказу 1 товар Мышь Logitech количество 2 на сумму 5000»

После открытия окна можно изменить поля:

«{WAKE_WORD_PLACEHOLDER}, заказ 3»
«{WAKE_WORD_PLACEHOLDER}, товар Монитор Samsung»
«{WAKE_WORD_PLACEHOLDER}, количество 4»
«{WAKE_WORD_PLACEHOLDER}, количество четыре»
«{WAKE_WORD_PLACEHOLDER}, сумма 120000»
«{WAKE_WORD_PLACEHOLDER}, дата сегодня»
«{WAKE_WORD_PLACEHOLDER}, дата завтра»

Для сохранения:
«{WAKE_WORD_PLACEHOLDER}, добавить»

Для отмены:
«{WAKE_WORD_PLACEHOLDER}, отмена»"""
        )

    # ---------------------------------------------------------
    # Создание задачи
    # ---------------------------------------------------------

    if (
        "задач" in normalized
        and (
            "добав" in normalized
            or "созд" in normalized
            or "как" in normalized
            or "нов" in normalized
        )
    ):
        return make_help_response(
            f"""Чтобы создать задачу, скажите:

«{WAKE_WORD_PLACEHOLDER}, создай задачу подготовить отчёт описание Сделать отчёт за месяц исполнитель 1 приоритет высокий»

После открытия окна можно изменить данные:

«{WAKE_WORD_PLACEHOLDER}, название Позвонить клиенту»
«{WAKE_WORD_PLACEHOLDER}, описание Уточнить оплату»
«{WAKE_WORD_PLACEHOLDER}, исполнитель Сидоров»
«{WAKE_WORD_PLACEHOLDER}, статус активная»
«{WAKE_WORD_PLACEHOLDER}, статус завершена»
«{WAKE_WORD_PLACEHOLDER}, приоритет высокий»
«{WAKE_WORD_PLACEHOLDER}, приоритет низкий»
«{WAKE_WORD_PLACEHOLDER}, срок завтра»

Для сохранения:
«{WAKE_WORD_PLACEHOLDER}, добавить»

Для отмены:
«{WAKE_WORD_PLACEHOLDER}, отмена»"""
        )

    # ---------------------------------------------------------
    # Изменение полей в окне подтверждения
    # ---------------------------------------------------------

    if (
        "измен" in normalized
        and (
            "пол" in normalized
            or "данн" in normalized
            or "окн" in normalized
            or "подтвержд" in normalized
        )
    ):
        return make_help_response(
            f"""Когда открыто окно подтверждения, поля можно менять голосом.

Для заказа:
«{WAKE_WORD_PLACEHOLDER}, клиент ООО Альфа»
«{WAKE_WORD_PLACEHOLDER}, сумма 50000»
«{WAKE_WORD_PLACEHOLDER}, статус в обработке»
«{WAKE_WORD_PLACEHOLDER}, менеджер Иванов»

Для сотрудника:
«{WAKE_WORD_PLACEHOLDER}, ФИО Петров Пётр»
«{WAKE_WORD_PLACEHOLDER}, должность Аналитик»
«{WAKE_WORD_PLACEHOLDER}, отдел Отчёты»

Для продажи:
«{WAKE_WORD_PLACEHOLDER}, заказ 3»
«{WAKE_WORD_PLACEHOLDER}, товар Монитор Samsung»
«{WAKE_WORD_PLACEHOLDER}, количество 4»
«{WAKE_WORD_PLACEHOLDER}, сумма 120000»
«{WAKE_WORD_PLACEHOLDER}, дата завтра»

Для задачи:
«{WAKE_WORD_PLACEHOLDER}, название Позвонить клиенту»
«{WAKE_WORD_PLACEHOLDER}, описание Уточнить оплату»
«{WAKE_WORD_PLACEHOLDER}, исполнитель Сидоров»
«{WAKE_WORD_PLACEHOLDER}, статус завершена»
«{WAKE_WORD_PLACEHOLDER}, приоритет низкий»
«{WAKE_WORD_PLACEHOLDER}, срок завтра»"""
        )

    # ---------------------------------------------------------
    # Подтверждение и отмена
    # ---------------------------------------------------------

    if (
        "подтверд" in normalized
        or "сохран" in normalized
        or "добавить" in normalized
        or "отмен" in normalized
    ):
        return make_help_response(
            f"""В окне подтверждения можно управлять действием голосом.

Чтобы сохранить запись:
«{WAKE_WORD_PLACEHOLDER}, добавить»

Также подходят команды:
«{WAKE_WORD_PLACEHOLDER}, подтвердить»
«{WAKE_WORD_PLACEHOLDER}, сохранить»

Чтобы отменить:
«{WAKE_WORD_PLACEHOLDER}, отмена»
«{WAKE_WORD_PLACEHOLDER}, не добавлять»"""
        )

    # ---------------------------------------------------------
    # График
    # ---------------------------------------------------------

    if "график" in normalized or "диаграм" in normalized:
        return make_help_response(
            f"""Чтобы построить график продаж, скажите:

«{WAKE_WORD_PLACEHOLDER}, построи график»

Или нажмите кнопку «Построить график» в блоке результата.

График строится по данным таблицы sales и показывает товары с суммами продаж."""
        )

    # ---------------------------------------------------------
    # PDF
    # ---------------------------------------------------------

    if "pdf" in normalized or "пдф" in normalized:
        return make_help_response(
            f"""Чтобы скачать PDF, сначала выполните любую команду, например:

«{WAKE_WORD_PLACEHOLDER}, покажи продажи за март»

После появления результата скажите:

«{WAKE_WORD_PLACEHOLDER}, скачай PDF»

Или нажмите кнопку «Скачать PDF»."""
        )

    # ---------------------------------------------------------
    # История
    # ---------------------------------------------------------

    if "истори" in normalized and (
        "очист" in normalized
        or "удал" in normalized
        or "стер" in normalized
        or "сотри" in normalized
    ):
        return make_help_response(
            f"""Чтобы очистить историю команд, скажите:

«{WAKE_WORD_PLACEHOLDER}, очисти историю»

Также можно нажать кнопку «Очистить» в блоке последних команд.

После очистки список команд удаляется и на сайте, и в базе данных."""
        )

    if "истори" in normalized:
        return make_help_response(
            f"""История команд показывает последние запросы, которые обработал ассистент.

Чтобы открыть историю, скажите:
«{WAKE_WORD_PLACEHOLDER}, открой историю»

Чтобы очистить историю:
«{WAKE_WORD_PLACEHOLDER}, очисти историю»"""
        )

    # ---------------------------------------------------------
    # Тема
    # ---------------------------------------------------------

    if "тем" in normalized or "светл" in normalized or "темн" in normalized:
        return make_help_response(
            f"""Для изменения темы используйте команды:

«{WAKE_WORD_PLACEHOLDER}, включи тёмную тему»
«{WAKE_WORD_PLACEHOLDER}, включи светлую тему»

Тему также можно изменить вручную в настройках сайта."""
        )

    # ---------------------------------------------------------
    # Язык
    # ---------------------------------------------------------

    if "язык" in normalized or "английск" in normalized or "русск" in normalized:
        return make_help_response(
            f"""Для смены языка интерфейса используйте команды:

«{WAKE_WORD_PLACEHOLDER}, переведи сайт на английский»
«{WAKE_WORD_PLACEHOLDER}, переведи сайт на русский»

Также язык можно изменить в настройках сайта."""
        )

    # ---------------------------------------------------------
    # Режим ожидания / ключевое слово
    # ---------------------------------------------------------

    if (
        "ожидан" in normalized
        or "постоян" in normalized
        or "ключев" in normalized
        or "слово" in normalized
        or "активац" in normalized
    ):
        return make_help_response(
            f"""На сайте есть два режима голосового управления:

1. По кнопке — вы нажимаете микрофон и говорите команду.
2. Постоянное ожидание — сайт ждёт ключевое слово.

Ключевое слово можно изменить в настройках. Подсказки в этом чате автоматически используют то слово, которое выбрано в настройках.

Команды:

«{WAKE_WORD_PLACEHOLDER}, включи режим постоянного ожидания»
«{WAKE_WORD_PLACEHOLDER}, переключи управление по кнопке»

Если режим ожидания иногда перезапускается — это нормально для браузерного распознавания речи."""
        )

    # ---------------------------------------------------------
    # NLP режим
    # ---------------------------------------------------------

    if (
        "ollama" in normalized
        or "оллама" in normalized
        or "local" in normalized
        or "локальн" in normalized
        or "запасн" in normalized
        or "основн" in normalized
        or "nlp" in normalized
    ):
        return make_help_response(
            f"""В системе есть два режима обработки команд:

1. Основной режим — Ollama.
2. Запасной режим — Local parser.

Команды:

«{WAKE_WORD_PLACEHOLDER}, включи основной режим»
«{WAKE_WORD_PLACEHOLDER}, включи запасной режим»

Если Ollama долго отвечает или нагружает компьютер, лучше использовать запасной режим."""
        )

    # ---------------------------------------------------------
    # Навигация
    # ---------------------------------------------------------

    if (
        "настройк" in normalized
        or "открыть" in normalized
        or "открой" in normalized
        or "перейти" in normalized
        or "перейди" in normalized
        or "страниц" in normalized
        or "вкладк" in normalized
    ):
        return make_help_response(
            f"""Примеры навигации по сайту:

«{WAKE_WORD_PLACEHOLDER}, открой главную»
«{WAKE_WORD_PLACEHOLDER}, открой настройки»
«{WAKE_WORD_PLACEHOLDER}, открой заказы»
«{WAKE_WORD_PLACEHOLDER}, открой задачи»
«{WAKE_WORD_PLACEHOLDER}, открой отчёты»
«{WAKE_WORD_PLACEHOLDER}, открой историю»

Ассистент автоматически переключит нужную вкладку."""
        )

    return None


def get_default_help_answer() -> dict:
    return make_help_response(
        f"""Я не смог точно определить вопрос.

Можно спросить, например:

«Как добавить заказ?»
«Как добавить менеджера?»
«Как создать задачу?»
«Как добавить продажу?»
«Как построить график?»
«Как скачать PDF?»
«Какие команды доступны?»

Примеры команд будут показаны с актуальным ключевым словом из настроек, например:
«{WAKE_WORD_PLACEHOLDER}, открой настройки»""",
        source="fallback_help",
    )


def ask_ollama_help(question: str) -> dict | None:
    system_prompt = f"""
Ты справочный помощник веб-сайта нейропомощника.
Отвечай только по функционалу этого сайта.
Не придумывай функций, которых нет.
Если пользователь спрашивает, как выполнить действие, дай точную голосовую команду.
В командах всегда используй шаблон ключевого слова: {WAKE_WORD_PLACEHOLDER}
Не заменяй {WAKE_WORD_PLACEHOLDER} на другое слово. Frontend сам подставит актуальное ключевое слово из настроек.

Функции сайта:

1. Добавить заказ:
«{WAKE_WORD_PLACEHOLDER}, добавь заказ клиента Ромашка на сумму 25000»

Поля заказа можно менять:
«{WAKE_WORD_PLACEHOLDER}, клиент ООО Альфа»
«{WAKE_WORD_PLACEHOLDER}, сумма 50000»
«{WAKE_WORD_PLACEHOLDER}, статус в обработке»
«{WAKE_WORD_PLACEHOLDER}, менеджер Иванов»

2. Добавить сотрудника/менеджера:
«{WAKE_WORD_PLACEHOLDER}, добавь сотрудника Иванов Иван должность Менеджер отдел Продажи»

Поля сотрудника можно менять:
«{WAKE_WORD_PLACEHOLDER}, ФИО Петров Пётр»
«{WAKE_WORD_PLACEHOLDER}, должность Аналитик»
«{WAKE_WORD_PLACEHOLDER}, отдел Отчёты»

3. Добавить продажу:
«{WAKE_WORD_PLACEHOLDER}, добавь продажу по заказу 1 товар Мышь Logitech количество 2 на сумму 5000»

Поля продажи можно менять:
«{WAKE_WORD_PLACEHOLDER}, заказ 3»
«{WAKE_WORD_PLACEHOLDER}, товар Монитор Samsung»
«{WAKE_WORD_PLACEHOLDER}, количество 4»
«{WAKE_WORD_PLACEHOLDER}, сумма 120000»
«{WAKE_WORD_PLACEHOLDER}, дата завтра»

4. Создать задачу:
«{WAKE_WORD_PLACEHOLDER}, создай задачу подготовить отчёт описание Сделать отчёт за месяц исполнитель 1 приоритет высокий»

Поля задачи можно менять:
«{WAKE_WORD_PLACEHOLDER}, название Позвонить клиенту»
«{WAKE_WORD_PLACEHOLDER}, описание Уточнить оплату»
«{WAKE_WORD_PLACEHOLDER}, исполнитель Сидоров»
«{WAKE_WORD_PLACEHOLDER}, статус завершена»
«{WAKE_WORD_PLACEHOLDER}, приоритет низкий»
«{WAKE_WORD_PLACEHOLDER}, срок завтра»

5. Подтвердить действие:
«{WAKE_WORD_PLACEHOLDER}, добавить»

6. Отменить действие:
«{WAKE_WORD_PLACEHOLDER}, отмена»

7. Построить график:
«{WAKE_WORD_PLACEHOLDER}, построи график»

8. Скачать PDF:
«{WAKE_WORD_PLACEHOLDER}, скачай PDF»

9. Очистить историю:
«{WAKE_WORD_PLACEHOLDER}, очисти историю»

10. Навигация:
«{WAKE_WORD_PLACEHOLDER}, открой настройки»
«{WAKE_WORD_PLACEHOLDER}, открой заказы»
«{WAKE_WORD_PLACEHOLDER}, открой задачи»
«{WAKE_WORD_PLACEHOLDER}, открой отчёты»
«{WAKE_WORD_PLACEHOLDER}, открой историю»

11. Тема:
«{WAKE_WORD_PLACEHOLDER}, включи тёмную тему»
«{WAKE_WORD_PLACEHOLDER}, включи светлую тему»

12. Язык:
«{WAKE_WORD_PLACEHOLDER}, переведи сайт на английский»
«{WAKE_WORD_PLACEHOLDER}, переведи сайт на русский»

Отвечай кратко, понятно, на русском языке.
"""

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": f"{system_prompt}\n\nВопрос пользователя: {question}\n\nОтвет:",
        "stream": False,
        "options": {
            "temperature": 0.2,
            "num_predict": 350,
        },
    }

    try:
        with httpx.Client(timeout=8) as client:
            response = client.post(
                f"{OLLAMA_URL}/api/generate",
                json=payload,
            )

        if response.status_code >= 400:
            return None

        data = response.json()
        answer = (data.get("response") or "").strip()

        if not answer:
            return None

        return make_help_response(answer, source="ollama_help")

    except Exception:
        return None


def get_help_answer(question: str) -> dict:
    local_answer = get_local_help_answer(question)

    if local_answer:
        return local_answer

    ollama_answer = ask_ollama_help(question)

    if ollama_answer:
        return ollama_answer

    return get_default_help_answer()