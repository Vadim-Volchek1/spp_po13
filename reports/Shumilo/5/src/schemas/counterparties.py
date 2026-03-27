from pydantic import BaseModel


class CounterpartyBase(BaseModel):
    name: str
    inn: str | None = None
    kpp: str | None = None
    type: str


class CounterpartyCreate(CounterpartyBase):
    pass


class CounterpartyUpdate(BaseModel):
    name: str | None = None
    inn: str | None = None
    kpp: str | None = None
    type: str | None = None


class CounterpartyOut(CounterpartyBase):
    id: int

    model_config = {
        "from_attributes": True
    }
