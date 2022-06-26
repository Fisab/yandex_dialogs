from fastapi import APIRouter
from super_app.models.internal import Status

router = APIRouter()


@router.get('/health', tags=['internal'], response_model=Status)
async def health():
    return Status(status='ok')
