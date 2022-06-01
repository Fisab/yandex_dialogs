from fastapi import APIRouter
from food_app.models.internal import Status

router = APIRouter()


@router.get('/health', tags=['internal'], response_model=Status)
async def health():
    return Status(status='ok')
