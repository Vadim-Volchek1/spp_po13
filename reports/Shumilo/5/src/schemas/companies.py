from pydantic import BaseModel


class CompanyBase(BaseModel):
    name: str
    inn: str | None = None
    kpp: str | None = None


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: str | None = None
    inn: str | None = None
    kpp: str | None = None


class CompanyOut(CompanyBase):
    id: int

    model_config = {
        "from_attributes": True
    }
