from enum import Enum
from typing import List

from pydantic import BaseModel, validator
from .utils import remove_accents


class OrderType(Enum):
    pick_up = "recoger"
    delivery = "domicilio"

    def __str__(self):
        return f"<{self.name}>"

    def __repr__(self) -> str:
        return str(self)


class Coords(BaseModel):
    lat: float
    long: float


class Shop(BaseModel):
    id: int
    title: str
    phone: int
    schedule: str
    types: List[OrderType]
    coords: Coords


class Address(BaseModel):
    province: str
    city: str
    street_name: str
    street_number: int

    @validator("province")
    def validate_province(cls, v):
        return v.lower()

    @validator("city")
    def validate_city(cls, v):
        return remove_accents(v).upper()

    @validator("street_name")
    def validate_street_name(cls, v):
        return remove_accents(v).upper()


class AppliedPromotion(BaseModel):
    order_type: OrderType
    description: str
    expires: str


class WorkingCode(AppliedPromotion):
    code: str
