import aiohttp
from utils.config import get_config
from furl import furl
from typing import Optional
from asyncache import cached
from cachetools import TTLCache


_obj = None
_config = get_config(root='food_app', part='papa_johns')


def papa_johns() -> 'PapaJohns':
    global _obj
    if not _obj:
        _obj = PapaJohns()
    return _obj


class PapaJohns:
    def __init__(self):
        self.config = _config

    @staticmethod
    async def _query(
        url: furl, method: Optional[str] = 'GET', json: Optional[dict] = None
    ) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url.tostr(), json=json) as response:
                return await response.json()

    @cached(TTLCache(maxsize=128, ttl=_config.ttl.unauthorized_token))
    async def init_cart(self) -> str:
        url = furl(self.config.url) / '/cart/add'
        json = {
            'city_id': self.config.city_id,
            'composition': [
                {'good_id': good_id, 'ingredients': [], 'type': 'good'}
                for good_id in self.config.goods_to_check
            ],
        }
        response = await self._query(url, method='POST', json=json)
        return response.get('unauthorized_token')

    async def get_goods_out_of_stock(self) -> list[int]:
        """
        :return: массив из id отсутствующих товаров в корзине
        """
        unauthorized_token = await self.init_cart()
        url = furl(self.config.url) / '/cart/stop-list'
        url.add(
            {
                'city_id': self.config.city_id,
                'restaurant_id': self.config.restaurant_id,
                'unauthorized_token': unauthorized_token,
            }
        )
        response = await self._query(url)
        return [row.get('good') for row in response]

    @cached(TTLCache(maxsize=128, ttl=_config.ttl.goods_check))
    async def check_goods_in_stock(self, good_id: int) -> bool:
        goods_out_of_stock = await self.get_goods_out_of_stock()
        return good_id not in goods_out_of_stock

    @cached(TTLCache(maxsize=128, ttl=_config.ttl.delivery_time))
    async def get_delivery_time(self) -> str:
        """
        :return: примерное время доставки
        """
        url = furl(self.config.url) / '/restaurant/delivery-time'
        url.add(
            {
                'city_id': self.config.city_id,
                'restaurant_id': self.config.restaurant_id,
                'address_coordinates': f'[{",".join(self.config.location)}]',
            }
        )
        response = await self._query(url)
        return response.get('delivery_time')

    def check_question_about_good(self, tokens: list[str]) -> Optional[int]:
        for good_id in self.config.goods_to_check:
            good = self.config.goods_to_check[good_id]
            for good_token in good.tokens:
                if good_token in tokens:
                    return good_id

    async def get_answer(self, tokens: list[str]) -> str:
        good_id = self.check_question_about_good(tokens)

        if good_id:
            good_in_stock = await self.check_goods_in_stock(good_id)
            return {True: 'Товар в наличии', False: 'Товар отсутствует'}.get(
                good_in_stock
            )

        delivery_time = await self.get_delivery_time()
        return f'Время доставки {delivery_time}'
