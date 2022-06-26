import aiohttp
from furl import furl
from typing import Optional
import logging
from utils.config import get_config
from pixoo_app.service.utils import get_number_from_list
from food_app.service.delivery_club import get_delivery_club_client
import random
import pendulum


_obj = None
logger = logging.getLogger(__name__)
_config = get_config(root='pixoo_app')
done_phrases = ['Готово', 'Сделано', 'Изменила']


def get_pixoo_client() -> 'PixooService':
    global _obj
    if not _obj:
        _obj = PixooService()
    return _obj


class PixooService:
    def __init__(self):
        self._token = _config.token
        self._base_url = _config.url
        self._channels = {
            0: ['часы'],
            1: ['подборка', 'подборку'],
            2: ['эквалайзер'],
            3: ['сохраненки'],
        }

        # TODO: сделать ли общение через http?
        self._delivery_club_client = get_delivery_club_client()

    async def _query(
        self,
        method: str,
        url: furl,
        params: Optional[dict] = None,
        json: Optional[dict] = None,
        headers: Optional[dict] = None,
    ) -> aiohttp.ClientResponse:
        if headers is None:
            headers = {}
        headers['x-token'] = self._token
        async with aiohttp.ClientSession() as session:
            return await session.request(
                method, url.tostr(), params=params, json=json, headers=headers
            )

    async def set_timer(self, minute: int, second: int) -> aiohttp.ClientResponse:
        url = furl(self._base_url) / 'timer'
        json = {'minute': minute, 'second': second}
        return await self._query('POST', url, json=json)

    async def set_channel(self, channel_id: int) -> aiohttp.ClientResponse:
        url = furl(self._base_url) / 'channel'
        url.args['channel_id'] = channel_id
        return await self._query('POST', url)

    async def set_brightness(self, brightness: int) -> aiohttp.ClientResponse:
        url = furl(self._base_url) / 'brightness'
        url.args['brightness'] = brightness
        return await self._query('POST', url)

    async def set_clock(self, clock_id: Optional[int] = None) -> aiohttp.ClientResponse:
        url = furl(self._base_url) / 'clock'
        if clock_id:
            url.args['clock_id'] = clock_id
        return await self._query('POST', url)

    async def get_answer(self, tokens: list[str]):
        if 'заказ' in tokens:
            order = await self._delivery_club_client.get_last_order(active=True)
            if order:
                if pendulum.parse(order.delivery.time) < pendulum.now():
                    return (
                        f'Заказ из {order.basket.vendor.name} {order.status.name.short},'
                        f'но уже должен был быть доставлен, время получать промокод'
                    )
                delivery_time = pendulum.parse(order.delivery.time) - pendulum.now()
                await self.set_timer(delivery_time.in_minutes(), 0)
                return (
                    f'Заказ из {order.basket.vendor.name} {order.status.name.short}, '
                    f'примерное время доставки {delivery_time.in_words(locale="ru")}'
                )
            return 'Активных заказов нету'
        elif 'яркость' in tokens:
            brightness = get_number_from_list(tokens)
            if not brightness:
                return 'На какой уровень яркости вы хотите установить?'
            await self.set_brightness(brightness)
            return random.choice(done_phrases)
        elif 'канал' in tokens:
            for channel_id, channel_names in self._channels.items():
                for channel_name in channel_names:
                    if channel_name in tokens:
                        await self.set_channel(channel_id)
                        return random.choice(done_phrases)
        elif 'таймер' in tokens:
            minute = get_number_from_list(tokens)
            if not minute:
                return 'На какое время вы хотите установить?'
            await self.set_timer(minute, 0)
            return random.choice(done_phrases)

        return 'Не поняла о чем вы'
