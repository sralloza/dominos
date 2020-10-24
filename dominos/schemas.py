from datetime import date, datetime
from enum import Enum
from typing import Dict, List

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
    name: str
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
    expires: date


class WorkingCode(AppliedPromotion):
    code: str


class ShowableWorkingCode(BaseModel):
    description: str
    expires: date
    code: str


class Information(BaseModel):
    shop: Shop
    updated: datetime
    order_types: Dict[str, List[ShowableWorkingCode]]
