from decimal import Decimal
from pydantic import BaseModel



class PostingBase(BaseModel):
    document_id: int
    debit_account_id: int
    credit_account_id: int
    amount: Decimal
    description: str | None = None


class PostingCreate(PostingBase):
    pass


class PostingUpdate(BaseModel):
    document_id: int | None = None
    debit_account_id: int | None = None
    credit_account_id: int | None = None
    amount: Decimal | None = None
    description: str | None = None


class PostingOut(PostingBase):
    id: int

    model_config = {
        "from_attributes": True
    }
