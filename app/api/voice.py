from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from pathlib import Path
from uuid import uuid4
import shutil
import traceback

from app.services.whisper_service import transcribe_audio
from app.services.llm_service import interpret_command
from app.services.business_service import (
    execute_business_command,
    save_command_history,
)

from app.services.pending_action_service import parse_pending_action_command
from app.services.ui_command_service import parse_ui_command
from app.services.ui_llm_service import interpret_ui_command_with_ollama


router = APIRouter(prefix="/api/voice", tags=["voice"])

UPLOAD_DIR = Path("static/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


class TextCommandRequest(BaseModel):
    text: str


def make_error_response(
    recognized_text: str,
    result_text: str,
    source: str = "system",
):
    return {
        "recognized_text": recognized_text,
        "intent": "error",
        "parameters": {},
        "source": source,
        "fallback": False,
        "fallback_reason": None,
        "result_text": result_text,
        "data": [],
    }


def process_recognized_text(recognized_text: str):
    """
    Единая обработка команды.
    ВАЖНО:
    1. Сначала команды, которые создают записи в БД.
    2. Потом команды управления интерфейсом.
    3. Потом обычные бизнес-команды: показать продажи, найти заказ и т.д.
    """

    if not recognized_text:
        return make_error_response(
            recognized_text="",
            result_text="Текст команды пустой",
            source="system",
        )

    recognized_text = recognized_text.strip()

    # ---------------------------------------------------------
    # 1. СНАЧАЛА проверяем действия, которые меняют БД
    # create_order / create_employee / create_sale / create_task
    # ---------------------------------------------------------

    try:
        pending_action = parse_pending_action_command(recognized_text)
    except Exception as action_error:
        return make_error_response(
            recognized_text=recognized_text,
            result_text=f"Ошибка парсера действий: {str(action_error)}",
            source="local_action_parser",
        )

    if pending_action:
        intent = pending_action.get("intent", "confirm_action")
        parameters = pending_action.get("parameters", {})
        result_text = pending_action.get("result_text", "")
        result_data = pending_action.get("data", [])

        save_command_history(
            recognized_text=recognized_text,
            intent=intent,
            parameters=parameters,
            result_text=result_text,
            status="Ожидает подтверждения",
        )

        return {
            "recognized_text": recognized_text,
            "intent": intent,
            "parameters": parameters,
            "source": pending_action.get("source", "local_action_parser"),
            "fallback": pending_action.get("fallback", False),
            "fallback_reason": pending_action.get("fallback_reason"),
            "result_text": result_text,
            "data": result_data,
        }

    # ---------------------------------------------------------
    # 2. Потом UI-команды:
    # открыть настройки, сменить тему, сменить язык и т.д.
    # ---------------------------------------------------------

    try:
        ui_command = parse_ui_command(recognized_text)
    except Exception:
        ui_command = None

    if not ui_command:
        try:
            ui_command = interpret_ui_command_with_ollama(recognized_text)
        except Exception as ui_llm_error:
            ui_command = None
            print(f"Ollama UI parser error: {str(ui_llm_error)}")

    if ui_command:
        intent = ui_command.get("intent", "unknown")
        parameters = ui_command.get("parameters", {})
        result_text = ui_command.get("result_text", "")
        result_data = ui_command.get("data", [])

        save_command_history(
            recognized_text=recognized_text,
            intent=intent,
            parameters=parameters,
            result_text=result_text,
            status="Выполнено" if intent != "unknown" else "Не распознано",
        )

        return {
            "recognized_text": recognized_text,
            "intent": intent,
            "parameters": parameters,
            "source": ui_command.get("source", "local_ui_parser"),
            "fallback": ui_command.get("fallback", False),
            "fallback_reason": ui_command.get("fallback_reason"),
            "result_text": result_text,
            "data": result_data,
        }

    # ---------------------------------------------------------
    # 3. Потом обычные бизнес-команды:
    # показать продажи, найти заказ, показать задачи и т.д.
    # ---------------------------------------------------------

    try:
        interpretation = interpret_command(recognized_text)
    except Exception as llm_error:
        return make_error_response(
            recognized_text=recognized_text,
            result_text=f"Ошибка интерпретации: {str(llm_error)}",
            source="llm",
        )

    intent = interpretation.get("intent", "unknown")
    parameters = interpretation.get("parameters", {})
    source = interpretation.get("source", "unknown")
    fallback = interpretation.get("fallback", False)
    fallback_reason = interpretation.get("fallback_reason")

    try:
        business_result = execute_business_command(
            recognized_text=recognized_text,
            intent=intent,
            parameters=parameters,
        )
    except Exception as business_error:
        return make_error_response(
            recognized_text=recognized_text,
            result_text=f"Ошибка выполнения команды: {str(business_error)}",
            source="business_service",
        )

    result_text = business_result.get("result_text", "")
    result_data = business_result.get("data", [])

    save_command_history(
        recognized_text=recognized_text,
        intent=intent,
        parameters=parameters,
        result_text=result_text,
        status="Выполнено" if intent != "unknown" else "Не распознано",
    )

    return {
        "recognized_text": recognized_text,
        "intent": intent,
        "parameters": parameters,
        "source": source,
        "fallback": fallback,
        "fallback_reason": fallback_reason,
        "result_text": result_text,
        "data": result_data,
    }


@router.post("")
async def process_voice(file: UploadFile = File(...)):
    file_extension = Path(file.filename).suffix or ".webm"
    file_name = f"{uuid4()}{file_extension}"
    file_path = UPLOAD_DIR / file_name

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        try:
            recognized_text = transcribe_audio(str(file_path))
        except Exception as whisper_error:
            return {
                "filename": file.filename,
                "saved_as": file_name,
                "recognized_text": "",
                "intent": "error",
                "parameters": {},
                "source": "whisper",
                "fallback": False,
                "fallback_reason": None,
                "result_text": f"Ошибка Whisper: {str(whisper_error)}",
                "data": [],
            }

        if not recognized_text:
            return {
                "filename": file.filename,
                "saved_as": file_name,
                "recognized_text": "",
                "intent": "error",
                "parameters": {},
                "source": "whisper",
                "fallback": False,
                "fallback_reason": None,
                "result_text": "Whisper не смог распознать речь. Попробуйте сказать громче.",
                "data": [],
            }

        result = process_recognized_text(recognized_text)

        return {
            "filename": file.filename,
            "saved_as": file_name,
            **result,
        }

    except Exception as error:
        print(traceback.format_exc())

        return {
            "filename": file.filename,
            "recognized_text": "",
            "intent": "error",
            "parameters": {},
            "source": "system",
            "fallback": False,
            "fallback_reason": None,
            "result_text": f"Общая ошибка обработки: {str(error)}",
            "data": [],
        }

    finally:
        file.file.close()


@router.post("/text")
async def process_text_command(request: TextCommandRequest):
    """
    Обработка текстовой команды.
    Используется для режима ожидания по ключевому слову:
    'Помощник, открой настройки'
    'Помощник, добавь продажу ...'
    """

    try:
        recognized_text = request.text.strip()

        if not recognized_text:
            return make_error_response(
                recognized_text="",
                result_text="Текст команды пустой",
                source="text",
            )

        return process_recognized_text(recognized_text)

    except Exception as error:
        print(traceback.format_exc())

        return {
            "recognized_text": request.text if request else "",
            "intent": "error",
            "parameters": {},
            "source": "system",
            "fallback": False,
            "fallback_reason": None,
            "result_text": f"Общая ошибка обработки текстовой команды: {str(error)}",
            "data": [],
        }