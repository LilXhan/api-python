from pydantic import BaseModel, Field
from random import randint
from enum import Enum

def random_destination():
    return randint(11000, 11999)

class ShipmentStatus(str, Enum):
    placed = 'placed'
    in_transit = 'in_transit'
    out_for_delivery = 'out_for_delivery'
    delivered = 'delivered'

class BaseShipment(BaseModel):
    content: str
    weight: float = Field(le=25)
    destination: int

class ShipmentRead(BaseShipment):
    status: ShipmentStatus

class ShipmentCreate(BaseShipment):
    pass

class ShipmentUpdate(BaseModel):
    content: str | None = Field(default=None)
    weight: float | None = Field(default=0, le=25)
    destination: int | None = Field(default=0)
    status: ShipmentStatus