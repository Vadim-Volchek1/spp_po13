from datetime import date
from decimal import Decimal

from pydantic import BaseModel



class DocumentBase(BaseModel):
    company_id: int
    counterparty_id: int | None = None
    doc_number: str
    doc_date: date
    doc_type: str
    total_amount: Decimal


class DocumentCreate(DocumentBase):
    pass


class DocumentUpdate(BaseModel):
    company_id: int | None = None
    counterparty_id: int | None = None
    doc_number: str | None = None
    doc_date: date | None = None
    doc_type: str | None = None
    total_amount: Decimal | None = None


class DocumentOut(DocumentBase):
    id: int

    model_config = {
        "from_attributes": True
    }
