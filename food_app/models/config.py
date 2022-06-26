from pydantic import BaseModel


class Goods2Check(BaseModel):
    name: str
    tokens: list[str]


class TTLInfo(BaseModel):
    unauthorized_token: int
    goods_check: int
    delivery_time: int


class PapaJohns(BaseModel):
    url: str
    ttl: TTLInfo
    goods_to_check: dict[int, Goods2Check]
    restaurant_id: int
    city_id: int
    location: list[str]


class SuperApp(BaseModel):
    root_path: str


class DeliveryClub(BaseModel):
    url: str
    refresh_token: str
    token: str
    secret: str


class FoodApp(BaseModel):
    papa_johns: PapaJohns
    delivery_club: DeliveryClub


class PixooApp(BaseModel):
    token: str
    url: str


class Config(BaseModel):
    food_app: FoodApp
    super_app: SuperApp
    pixoo_app: PixooApp
