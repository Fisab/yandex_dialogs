from pydantic import BaseModel


class Goods2Check(BaseModel):
    name: str
    tokens: list[str]


class PapaJohns(BaseModel):
    url: str
    ttl_unauthorized_token: int
    goods_to_check: dict[int, Goods2Check]
    restaurant_id: int
    city_id: int
    location: list[str]


class SuperApp(BaseModel):
    root_path: str


class PapaJohnsRoot(BaseModel):
    papa_johns: PapaJohns


class Config(BaseModel):
    food_app: PapaJohnsRoot
    super_app: SuperApp
