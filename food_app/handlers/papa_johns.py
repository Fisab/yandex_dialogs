from fastapi import APIRouter

from food_app.service import papa_johns

router = APIRouter()


@router.get('/sauce_exists', tags=['main'])
async def check_sauce_exists():
    return {'exists': await papa_johns.check_sauce_exists()}


@router.get('/delivery_time', tags=['main'])
async def delivery_time():
    return {'delivery_time': await papa_johns.get_delivery_time()}
