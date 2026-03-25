from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional


class CitizenBase(BaseModel):
    full_name: str
    birth_date: Optional[date] = None
    email: EmailStr
    phone: Optional[str] = None


class CitizenCreate(CitizenBase):
    pass


class CitizenUpdate(BaseModel):
    full_name: Optional[str] = None
    birth_date: Optional[date] = None
    phone: Optional[str] = None


class CitizenOut(CitizenBase):
    id: int
    registration_date: Optional[date] = None

    class Config:
        orm_mode = True


class EmployerBase(BaseModel):
    name: str
    inn: str
    address: Optional[str] = None
    contact_email: Optional[EmailStr] = None


class EmployerCreate(EmployerBase):
    pass


class EmployerUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    contact_email: Optional[EmailStr] = None


class EmployerOut(EmployerBase):
    id: int

    class Config:
        orm_mode = True


class VacancyBase(BaseModel):
    employer_id: int
    title: str
    description: Optional[str] = None
    salary_from: Optional[int] = None
    salary_to: Optional[int] = None
    is_active: Optional[bool] = True


class VacancyCreate(VacancyBase):
    pass


class VacancyUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    salary_from: Optional[int] = None
    salary_to: Optional[int] = None
    is_active: Optional[bool] = None


class VacancyOut(VacancyBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class ApplicationBase(BaseModel):
    citizen_id: int
    vacancy_id: int
    status: Optional[str] = "new"


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(BaseModel):
    status: Optional[str] = None


class ApplicationOut(ApplicationBase):
    id: int
    applied_at: datetime

    class Config:
        orm_mode = True


class SkillBase(BaseModel):
    name: str


class SkillCreate(SkillBase):
    pass


class SkillOut(SkillBase):
    id: int

    class Config:
        orm_mode = True
