
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="Mediscript AI",
    description="Intelligent Realtime Prescription Generation",
    version="1.0.0",
)

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)

templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)


@app.get("/")
async def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"title": "Mediscript AI"},
    )


@app.get("/login")
async def doctor_login(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"title": "Doctor Login | Mediscript AI"},
    )


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "application": "Mediscript AI",
    }
