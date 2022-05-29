from fastapi import APIRouter
from food_app.service.config import get_config
from food_app.models.config import Config

router = APIRouter()


@router.get('/config', tags=['internal'], response_model=Config)
async def config():
    return get_config()
