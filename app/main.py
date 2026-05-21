from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.dashboard import router as dashboard_router
from app.api.voice import router as voice_router
from app.api.settings import router as settings_router
from app.api.pages import router as pages_router
from app.api.pdf import router as pdf_router
from app.supabase_rest import get_rows
from app.api.actions import router as actions_router
from app.api.history import router as history_router
from app.api.help import router as help_router
from app.api.mailings import router as mailings_router
from app.api.telegram import router as telegram_router
from app.api.auth import router as auth_router
from app.services.auth_service import (
    AUTH_ENABLED,
    get_current_user_from_request,
    get_required_permission,
    has_permission,
)
from app.services.telegram_polling_service import (
    start_telegram_polling,
    stop_telegram_polling,
)

app = FastAPI(title="Neuro Assistant")

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

app.include_router(dashboard_router)
app.include_router(voice_router)
app.include_router(settings_router)
app.include_router(pages_router)
app.include_router(pdf_router)
app.include_router(actions_router)
app.include_router(history_router)
app.include_router(help_router)
app.include_router(mailings_router)
app.include_router(telegram_router)
app.include_router(auth_router)


PUBLIC_PATHS = {
    "/login",
    "/health",
    "/favicon.ico",
    "/api/auth/login",
}

PUBLIC_PREFIXES = (
    "/static/",
)


@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    if not AUTH_ENABLED:
        return await call_next(request)

    path = request.url.path

    if path in PUBLIC_PATHS or path.startswith(PUBLIC_PREFIXES):
        return await call_next(request)

    user = get_current_user_from_request(request)

    if not user:
        if path.startswith("/api/") or path in {"/docs", "/openapi.json", "/redoc"}:
            return JSONResponse(
                status_code=401,
                content={"detail": "Требуется авторизация"},
            )

        return RedirectResponse(url="/login", status_code=303)

    request.state.user = user

    required_permission = get_required_permission(path, request.method)

    if required_permission and not has_permission(user, required_permission):
        return JSONResponse(
            status_code=403,
            content={"detail": "Недостаточно прав для выполнения действия"},
        )

    return await call_next(request)


@app.on_event("startup")
async def startup_event():
    start_telegram_polling()


@app.on_event("shutdown")
async def shutdown_event():
    await stop_telegram_polling()


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "user": getattr(request.state, "user", None),
        },
    )


@app.get("/login")
def login_page(request: Request):
    if get_current_user_from_request(request):
        return RedirectResponse(url="/", status_code=303)

    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/db-test")
def db_test():
    employees = get_rows("employees", "select=*&limit=1")
    return {
        "database": "connected via supabase rest",
        "test_rows": employees,
    }
