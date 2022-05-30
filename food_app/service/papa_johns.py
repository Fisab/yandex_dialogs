import aiohttp
from utils.config import get_config
from furl import furl
from typing import Optional


config = get_config(root='food_app', part='papa_johns')


async def _query(
    url: furl, method: Optional[str] = 'GET', json: Optional[dict] = None
) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.request(method, url.tostr(), json=json) as response:
            return await response.json()


async def init_cart() -> str:
    url = furl(config.url) / '/cart/add'
    json = {
        'city_id': config.city_id,
        'composition': [
            {'good_id': good.id, 'ingredients': [], 'type': 'good'}
            for good in config.goods_to_check
        ],
    }
    response = await _query(url, method='POST', json=json)
    return response.get('unauthorized_token')


async def check_sauce_exists() -> list[int]:
    """
    :return: массив из id отсутствующих товаров в корзине
    """
    unauthorized_token = await init_cart()
    url = furl(config.url) / '/cart/stop-list'
    url.add(
        {
            'city_id': config.city_id,
            'restaurant_id': config.restaurant_id,
            'unauthorized_token': unauthorized_token,
        }
    )
    response = await _query(url)
    return [row.get('good') for row in response]


async def get_delivery_time():
    """
    :return: примерное время доставки
    """
    url = furl(config.url) / '/restaurant/delivery-time'
    url.add(
        {
            'city_id': config.city_id,
            'restaurant_id': config.restaurant_id,
            'address_coordinates': f'[{",".join(config.location)}]',
        }
    )
    response = await _query(url)
    return response.get('delivery_time')
