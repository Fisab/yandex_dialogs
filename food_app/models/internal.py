from pydantic import BaseModel


class Status(BaseModel):
    status: str


class DeliveryTime(BaseModel):
    delivery_time: str


class GoodsOutOfStock(BaseModel):
    doesnt_exists: list[int]
