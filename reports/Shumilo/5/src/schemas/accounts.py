from pydantic import BaseModel


class AccountBase(BaseModel):
    code: str
    name: str
    is_active: bool = True


class AccountCreate(AccountBase):
    pass


class AccountUpdate(BaseModel):
    code: str | None = None
    name: str | None = None
    is_active: bool | None = None


class AccountOut(AccountBase):
    id: int

    model_config = {
        "from_attributes": True
    }
