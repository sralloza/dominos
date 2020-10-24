from enum import Enum
from typing import List

from pydantic import BaseModel


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


class AppliedPromotion(BaseModel):
    order_type: OrderType
    description: str
    expires: str


class WorkingCode(AppliedPromotion):
    code: str
