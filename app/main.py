from fastapi import FastAPI
from dotenv import load_dotenv
from app.configs.settings import Setting, get_settings
from app.controllers.health_controller import router as health_router
from app.utils import configure_logging, get_logger
from app.controllers import document_controller

load_dotenv()

configure_logging()
logger = get_logger(__name__)

settings= get_settings()

app = FastAPI(
    title= settings.app_name
)
logger.info("Starting %s", settings.app_name)


@app.get("/")
def hello() -> dict[str, str]:
    return {"message": "Hello, World!"}

app.include_router(health_router)
app.include_router(document_controller.router)

def main() -> None:
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

