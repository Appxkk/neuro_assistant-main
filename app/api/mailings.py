import json

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.services.mailing_service import send_mailing_with_uploads


router = APIRouter(prefix="/api/mailings", tags=["mailings"])


@router.post("/send")
async def send_mailing(
    channels: str = Form(...),
    target: str = Form("test"),
    message: str = Form(""),
    files: list[UploadFile] | None = File(None),
):
    try:
        parsed_channels = json.loads(channels)
    except json.JSONDecodeError:
        parsed_channels = [item.strip() for item in channels.split(",") if item.strip()]

    if not isinstance(parsed_channels, list):
        raise HTTPException(status_code=400, detail="Некорректный список каналов")

    return await send_mailing_with_uploads(
        {
            "channels": parsed_channels,
            "target": target,
            "message": message,
        },
        files,
    )
