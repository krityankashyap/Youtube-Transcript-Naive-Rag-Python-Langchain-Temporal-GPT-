from fastapi import FastAPI
from dotenv import load_dotenv
from app.configs.settings import Setting, get_settings
from app.controllers.health_controller import router as health_router

load_dotenv()

settings= get_settings()

app = FastAPI(
    title= settings.app_name    
)


@app.get("/")
def hello() -> dict[str, str]:
    return {"message": "Hello, World!"}

app.include_router(health_router)

def main() -> None:
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

