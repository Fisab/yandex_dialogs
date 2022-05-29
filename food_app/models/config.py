from pydantic import BaseModel


class Goods2Check(BaseModel):
    name: str
    id: int


class PapaJohns(BaseModel):
    url: str
    goods_to_check: list[Goods2Check]
    restaurant_id: int
    city_id: int
    location: list[str]


class Config(BaseModel):
    papa_johns: PapaJohns
