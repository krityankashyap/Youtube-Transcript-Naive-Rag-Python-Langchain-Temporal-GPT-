from app.schemas.api import HealthResponse
from datetime import datetime
from fastapi import APIRouter

router= APIRouter(
    prefix="/health",
    tags=["Health Check"]
)

@router.get("/", response_model=HealthResponse, summary="Health Check Endpoint")
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(
        status="Ok/Healthy",
        timestamp=datetime.now()
    )