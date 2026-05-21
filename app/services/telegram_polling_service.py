import asyncio
import os

from dotenv import load_dotenv

from app.services.telegram_recipient_service import (
    get_telegram_updates,
    process_telegram_update,
)


load_dotenv()

TELEGRAM_POLLING_ENABLED = os.getenv("TELEGRAM_POLLING_ENABLED", "true").lower() == "true"
TELEGRAM_POLLING_INTERVAL = int(os.getenv("TELEGRAM_POLLING_INTERVAL", "5"))

_polling_task: asyncio.Task | None = None
_last_update_offset: int | None = None


async def telegram_polling_loop():
    global _last_update_offset

    while True:
        try:
            updates_response = await get_telegram_updates(offset=_last_update_offset)
            updates = updates_response.get("result") or []

            for update in updates:
                update_id = update.get("update_id")

                if update_id is not None:
                    _last_update_offset = max(_last_update_offset or 0, update_id + 1)

                await process_telegram_update(update, send_reply=True)

        except asyncio.CancelledError:
            raise

        except Exception as error:
            print(f"Telegram polling error: {error}")

        await asyncio.sleep(TELEGRAM_POLLING_INTERVAL)


def start_telegram_polling():
    global _polling_task

    if not TELEGRAM_POLLING_ENABLED:
        print("Telegram polling disabled")
        return

    if _polling_task and not _polling_task.done():
        return

    _polling_task = asyncio.create_task(telegram_polling_loop())
    print(f"Telegram polling started, interval={TELEGRAM_POLLING_INTERVAL}s")


async def stop_telegram_polling():
    global _polling_task

    if not _polling_task:
        return

    _polling_task.cancel()

    try:
        await _polling_task
    except asyncio.CancelledError:
        pass

    _polling_task = None
    print("Telegram polling stopped")
