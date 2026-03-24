from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel



# Пользователь
class CustomerBase(BaseModel):
    fnane: str
    sname: str
    adres: str
    phone: str


class CustomerCreate(CustomerBase):
    pass


class Customer(CustomerBase):
    id: int

    class Config:
        from_attributes = True


# Заказы
class OrderBase(BaseModel):
    id_customer: int


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    id: int
    date: datetime

    class Config:
        from_attributes = True


# Товары
class GoodBase(BaseModel):
    name: str
    postavshchik: str
    stoimost: float
    id_sclad: Optional[int] = None


class GoodCreate(GoodBase):
    pass


class Good(GoodBase):
    id: int

    class Config:
        from_attributes = True


# Ноборы заказов
class NaborOrderBase(BaseModel):
    id_order: int
    id_good: int
    count: int


class NaborOrderCreate(NaborOrderBase):
    pass


class NaborOrder(NaborOrderBase):
    class Config:
        from_attributes = True


# Склад
class ScladBase(BaseModel):
    name: str
    adres: str


class ScladCreate(ScladBase):
    pass


class Sclad(ScladBase):
    id: int
    goods: List[Good] = []

    class Config:
        from_attributes = True
