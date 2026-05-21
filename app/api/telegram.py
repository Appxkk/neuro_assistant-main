from fastapi import APIRouter, Body, Query

from app.services.telegram_recipient_service import (
    get_telegram_webhook_info,
    get_telegram_updates,
    process_telegram_update,
    set_telegram_webhook,
)


router = APIRouter(prefix="/api/telegram", tags=["telegram"])


@router.post("/webhook")
async def telegram_webhook(update: dict = Body(...)):
    result = await process_telegram_update(update, send_reply=True)

    return {
        "ok": True,
        "result": result,
    }


@router.post("/poll-updates")
async def poll_telegram_updates(offset: int | None = Query(default=None)):
    updates_response = await get_telegram_updates(offset=offset)
    updates = updates_response.get("result") or []
    processed = []
    next_offset = offset

    for update in updates:
        update_id = update.get("update_id")

        if update_id is not None:
            next_offset = max(next_offset or 0, update_id + 1)

        processed.append(await process_telegram_update(update, send_reply=True))

    return {
        "ok": True,
        "processed_count": len(processed),
        "next_offset": next_offset,
        "results": processed,
    }


@router.post("/set-webhook")
async def configure_telegram_webhook(webhook_url: str = Body(..., embed=True)):
    result = await set_telegram_webhook(webhook_url)

    return {
        "ok": True,
        "result": result,
    }


@router.get("/webhook-info")
async def telegram_webhook_info():
    return await get_telegram_webhook_info()
