import os
import json

import httpx
from dotenv import load_dotenv
from fastapi import HTTPException, UploadFile


load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_DEFAULT_CHAT_ID = os.getenv("TELEGRAM_DEFAULT_CHAT_ID")
TELEGRAM_PHOTO_TYPES = {"image/jpeg", "image/png", "image/webp"}
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


def send_mailing(payload: dict) -> dict:
    channels = payload.get("channels") or []
    message = str(payload.get("message") or "").strip()
    target = payload.get("target") or "test"

    if "telegram" not in channels:
        raise HTTPException(status_code=400, detail="Выберите Telegram для отправки рассылки")

    if not message:
        raise HTTPException(status_code=400, detail="Введите текст рассылки")

    telegram_result = send_telegram_message(message, TELEGRAM_DEFAULT_CHAT_ID)

    return {
        "status": "success",
        "result_text": "Рассылка отправлена в Telegram",
        "data": [
            {
                "channel": "telegram",
                "target": target,
                "chat_id": str(TELEGRAM_DEFAULT_CHAT_ID),
                "message_id": telegram_result.get("message_id"),
                "text": message,
            }
        ],
    }


async def send_mailing_with_uploads(payload: dict, uploads: list[UploadFile] | None = None) -> dict:
    channels = payload.get("channels") or []
    message = str(payload.get("message") or "").strip()
    target = payload.get("target") or "test"
    uploaded_files = await read_upload_files(uploads or [])
    photos = [file for file in uploaded_files if file["content_type"] in TELEGRAM_PHOTO_TYPES]
    documents = [file for file in uploaded_files if file["content_type"] not in TELEGRAM_PHOTO_TYPES]

    if "telegram" not in channels:
        raise HTTPException(status_code=400, detail="Выберите Telegram для отправки рассылки")

    if not message and not uploaded_files:
        raise HTTPException(status_code=400, detail="Введите текст рассылки или прикрепите файл")

    recipients = await get_mailing_recipients(target)

    if not recipients:
        raise HTTPException(status_code=400, detail="Получатели для выбранной аудитории не найдены")

    results = []

    for recipient in recipients:
        chat_id = recipient["chat_id"]

        if photos:
            photo_results = await send_telegram_photo_group(chat_id, photos, message)
            for item in photo_results:
                item.update(make_recipient_result_meta(target, recipient))
            results.extend(photo_results)
        elif message:
            text_result = await send_telegram_message_async(message, chat_id)
            results.append(
                {
                    "channel": "telegram",
                    "type": "text",
                    "target": target,
                    "recipient_type": recipient.get("recipient_type"),
                    "recipient_id": recipient.get("id"),
                    "chat_id": str(chat_id),
                    "message_id": text_result.get("message_id"),
                    "text": message,
                }
            )

        for document in documents:
            file_result = await send_telegram_document(chat_id, document)
            file_result.update(make_recipient_result_meta(target, recipient))
            results.append(file_result)

    attachments_count = len(uploaded_files)

    if attachments_count:
        result_text = (
            f"Рассылка отправлена в Telegram. "
            f"Получателей: {len(recipients)}. Вложений: {attachments_count}"
        )
    else:
        result_text = f"Рассылка отправлена в Telegram. Получателей: {len(recipients)}"

    return {
        "status": "success",
        "result_text": result_text,
        "data": results,
    }


def make_recipient_result_meta(target: str, recipient: dict) -> dict:
    return {
        "target": target,
        "recipient_type": recipient.get("recipient_type"),
        "recipient_id": recipient.get("id"),
    }


async def get_mailing_recipients(target: str) -> list[dict]:
    if target == "test":
        if not TELEGRAM_DEFAULT_CHAT_ID:
            raise HTTPException(status_code=500, detail="TELEGRAM_DEFAULT_CHAT_ID не указан в .env")

        return [
            {
                "id": None,
                "chat_id": str(TELEGRAM_DEFAULT_CHAT_ID),
                "recipient_type": "test",
                "priority": "test",
            }
        ]

    if target not in {"employees", "clients", "all"}:
        raise HTTPException(status_code=400, detail=f"Неизвестная аудитория рассылки: {target}")

    if not SUPABASE_URL or not SUPABASE_KEY:
        raise HTTPException(status_code=500, detail="SUPABASE_URL или SUPABASE_KEY не указаны в .env")

    query = (
        "select=id,chat_id,username,first_name,last_name,recipient_type,priority"
        "&is_active=eq.true"
        "&order=id.asc"
    )

    if target == "employees":
        query += "&recipient_type=eq.employee"

    if target == "clients":
        query += "&recipient_type=eq.client"

    url = f"{SUPABASE_URL}/rest/v1/telegram_recipients?{query}"

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(
            url,
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Content-Type": "application/json",
            },
        )

    if response.status_code >= 400:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()


async def read_upload_files(uploads: list[UploadFile]) -> list[dict]:
    files = []

    for upload in uploads:
        if not upload or not upload.filename:
            continue

        content = await upload.read()

        if not content:
            raise HTTPException(status_code=400, detail=f"Файл пустой: {upload.filename}")

        files.append(
            {
                "filename": upload.filename,
                "content": content,
                "content_type": upload.content_type or "application/octet-stream",
                "size": len(content),
            }
        )

    return files


def send_telegram_message(message: str, chat_id: str | None = None) -> dict:
    ensure_telegram_config()
    chat_id = chat_id or TELEGRAM_DEFAULT_CHAT_ID

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    try:
        with httpx.Client(timeout=15) as client:
            response = client.post(
                url,
                json={
                    "chat_id": chat_id,
                    "text": message,
                },
            )

        data = parse_telegram_response(response)
        return data.get("result") or {}

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка отправки Telegram-сообщения: {str(error)}",
        )


async def send_telegram_message_async(message: str, chat_id: str) -> dict:
    ensure_telegram_config()

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.post(
                url,
                json={
                    "chat_id": chat_id,
                    "text": message,
                },
            )

        data = parse_telegram_response(response)
        return data.get("result") or {}

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка отправки Telegram-сообщения: {str(error)}",
        )


async def send_telegram_photo_group(chat_id: str, photos: list[dict], caption: str = "") -> list[dict]:
    ensure_telegram_config()

    if len(photos) == 1:
        result = await send_telegram_photo(chat_id, photos[0], caption)
        return [result]

    media = []
    multipart_files = {}

    for index, photo in enumerate(photos[:10]):
        field_name = f"photo_{index}"
        item = {
            "type": "photo",
            "media": f"attach://{field_name}",
        }

        if index == 0 and caption:
            item["caption"] = caption

        media.append(item)
        multipart_files[field_name] = (
            photo["filename"],
            photo["content"],
            photo["content_type"],
        )

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMediaGroup"

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                url,
                data={
                    "chat_id": chat_id,
                    "media": json.dumps(media, ensure_ascii=False),
                },
                files=multipart_files,
            )

        data = parse_telegram_response(response)
        messages = data.get("result") or []

        return [
            {
                "channel": "telegram",
                "type": "photo_group",
                "chat_id": str(chat_id),
                "message_id": message.get("message_id"),
                "filename": photos[index]["filename"],
                "content_type": photos[index]["content_type"],
                "size": photos[index]["size"],
            }
            for index, message in enumerate(messages)
        ]

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка отправки альбома в Telegram: {str(error)}",
        )


async def send_telegram_photo(chat_id: str, photo: dict, caption: str = "") -> dict:
    ensure_telegram_config()

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                url,
                data={
                    "chat_id": chat_id,
                    "caption": caption,
                },
                files={
                    "photo": (
                        photo["filename"],
                        photo["content"],
                        photo["content_type"],
                    )
                },
            )

        data = parse_telegram_response(response)
        result = data.get("result") or {}

        return {
            "channel": "telegram",
            "type": "photo",
            "chat_id": str(chat_id),
            "message_id": result.get("message_id"),
            "filename": photo["filename"],
            "content_type": photo["content_type"],
            "size": photo["size"],
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка отправки фото в Telegram: {str(error)}",
        )


async def send_telegram_document(chat_id: str, document: dict) -> dict:
    ensure_telegram_config()

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                url,
                data={"chat_id": chat_id},
                files={
                    "document": (
                        document["filename"],
                        document["content"],
                        document["content_type"],
                    )
                },
            )

        data = parse_telegram_response(response)
        result = data.get("result") or {}

        return {
            "channel": "telegram",
            "type": "document",
            "chat_id": str(chat_id),
            "message_id": result.get("message_id"),
            "filename": document["filename"],
            "content_type": document["content_type"],
            "size": document["size"],
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка отправки документа в Telegram: {str(error)}",
        )


def ensure_telegram_config():
    if not TELEGRAM_BOT_TOKEN:
        raise HTTPException(status_code=500, detail="TELEGRAM_BOT_TOKEN не указан в .env")

    if not TELEGRAM_DEFAULT_CHAT_ID:
        raise HTTPException(status_code=500, detail="TELEGRAM_DEFAULT_CHAT_ID не указан в .env")


def parse_telegram_response(response: httpx.Response) -> dict:
    if response.status_code >= 400:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text,
        )

    data = response.json()

    if not data.get("ok"):
        raise HTTPException(
            status_code=502,
            detail=data.get("description") or "Telegram API вернул ошибку",
        )

    return data
