from fastapi import APIRouter, status
from app.logger import get_logger

router = APIRouter(tags=["default"])

logger = get_logger("reviews")


@router.get("/", status_code=status.HTTP_200_OK)
async def get_default():
    return "ok"
