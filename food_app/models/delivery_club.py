from __future__ import annotations
from typing import List
from pydantic import BaseModel, Field


class Building(BaseModel):
    block: str
    entrance: str


class Id(BaseModel):
    primary: str


class City(BaseModel):
    id: Id
    name: str


class Geo(BaseModel):
    city: City
    latitude: float
    longitude: float
    name: str


class Id1(BaseModel):
    primary: str


class LastMile(BaseModel):
    flat_number: str = Field(..., alias="flatNumber")
    floor: str
    intercom: str


class Address(BaseModel):
    building: Building
    geo: Geo
    id: Id1
    last_mile: LastMile = Field(..., alias="lastMile")


class Attributes(BaseModel):
    persons_qty: str = Field(..., alias="personsQty")


class Price(BaseModel):
    currency: str
    value: int


class Price1(BaseModel):
    currency: str
    value: int


class Reference(BaseModel):
    descriptor: str
    price: Price1
    type: str


class Discount(BaseModel):
    price: Price
    reference: Reference


class Id2(BaseModel):
    inventory: str
    primary: str


class Pure(BaseModel):
    currency: str
    value: int


class Single(BaseModel):
    currency: str
    value: int


class Total(BaseModel):
    currency: str
    value: int


class Price2(BaseModel):
    pure: Pure
    single: Single
    total: Total


class Item1(BaseModel):
    description: str
    descriptor: str
    id: Id2
    ingredients: List
    name: str
    price: Price2
    qty: int
    template: int


class CartItem(BaseModel):
    currency: str
    value: int


class Delivery(BaseModel):
    currency: str
    value: int


class DiscountItem(BaseModel):
    currency: str
    value: int


class OriginalItem(BaseModel):
    currency: str
    value: int


class ServiceFee(BaseModel):
    currency: str
    value: int


class Prices(BaseModel):
    cart: List[CartItem]
    delivery: Delivery
    discount: List[DiscountItem]
    original: List[OriginalItem]
    service_fee: ServiceFee = Field(..., alias="serviceFee")


class Qty(BaseModel):
    total: int
    unique: int


class Total1(BaseModel):
    prices: Prices
    qty: Qty


class Id3(BaseModel):
    primary: str


class Chain(BaseModel):
    category_id: int = Field(..., alias="categoryId")
    id: Id3
    image: str


class Delivery1(BaseModel):
    services: List[int]
    urgency: List[int]


class Id4(BaseModel):
    primary: str


class Vendor(BaseModel):
    address: str
    chain: Chain
    cook_avg_time: int = Field(..., alias="cookAvgTime")
    delivery: Delivery1
    id: Id4
    name: str
    phones: List[str]


class Basket(BaseModel):
    descriptor: str
    discounts: List[Discount]
    items: List[Item1]
    total: Total1
    uuid: str
    vendor: Vendor


class Price3(BaseModel):
    currency: str
    value: int


class Route(BaseModel):
    duration_mins: int = Field(..., alias="durationMins")


class Delivery2(BaseModel):
    price: Price3
    route: Route
    time: str
    type: int
    urgency: int


class Feedback(BaseModel):
    available: bool


class Id5(BaseModel):
    hash: str
    rr_hash: str = Field(..., alias="rrHash")


class Receipt(BaseModel):
    link: str
    name: str


class Payment(BaseModel):
    receipts: List[Receipt]
    status: int


class Reorder(BaseModel):
    available: bool


class Name(BaseModel):
    long: str
    short: str


class Status(BaseModel):
    description: str
    name: Name
    value: int


class DeliveryClubOrder(BaseModel):
    address: Address
    attributes: Attributes
    basket: Basket
    comment: str
    delivery: Delivery2
    feedback: Feedback
    id: Id5
    payment: Payment
    reorder: Reorder
    status: Status


class Model(BaseModel):
    total: int
    items: List[DeliveryClubOrder]
