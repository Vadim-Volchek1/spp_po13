from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class ClientBase(BaseModel):
    firstName: str
    lastName: str
    sex: Optional[str] = None
    nickName: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None


class ClientCreate(ClientBase):
    pass


class ClientResponse(ClientBase):
    cl_id: int

    class Config:
        from_attributes = True


class ManufacturerBase(BaseModel):
    name: str
    establish_date: Optional[date] = None


class ManufacturerCreate(ManufacturerBase):
    pass


class ManufacturerResponse(ManufacturerBase):
    man_id: int

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    name: str
    price: float = Field(..., gt=0)
    man_id: int


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    pr_id: int

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    cl_id: int
    total_sum: float = Field(..., gt=0)


class OrderCreate(OrderBase):
    pass


class OrderResponse(OrderBase):
    ord_id: int
    date_order: date

    class Config:
        from_attributes = True


class OrderSummaryBase(BaseModel):
    ord_id: int
    pr_id: int
    count: int = Field(..., gt=0)


class OrderSummaryCreate(OrderSummaryBase):
    pass


class OrderSummaryResponse(OrderSummaryBase):
    ord_s_id: int

    class Config:
        from_attributes = True
