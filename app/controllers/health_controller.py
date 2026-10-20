from app.schemas.api import HealthResponse
from app.utils import get_logger
from datetime import datetime
from fastapi import APIRouter

logger = get_logger(__name__)

router= APIRouter(
    prefix="/health",
    tags=["Health Check"]
)

@router.get("/", response_model=HealthResponse, summary="Health Check Endpoint")
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    logger.debug("Health check requested")
    return HealthResponse(
        status="Ok/Healthy",
        timestamp=datetime.now()
    )