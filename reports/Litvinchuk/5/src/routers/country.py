"""Маршруты для работы со странами."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.crud.country import create, delete, get, get_all, update
from src.database import SessionLocal

router = APIRouter(prefix="/countries", tags=["Countries"])


def get_db():
    """Создаёт сессию БД и закрывает её после завершения запроса."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class CountryCreate(BaseModel):
    """Схема создания и обновления страны."""

    name: str
    code: str


class CountryRead(BaseModel):
    """Схема чтения страны."""

    id: int
    name: str
    code: str

    class Config:  # pylint: disable=too-few-public-methods
        """Конфигурация Pydantic-схемы."""

        orm_mode = True


@router.get("/", response_model=List[CountryRead])
def list_countries(db: Session = Depends(get_db)):
    """Возвращает список всех стран."""
    return get_all(db)


@router.get("/{country_id}", response_model=CountryRead)
def read_country(country_id: int, db: Session = Depends(get_db)):
    """Возвращает страну по её идентификатору."""
    obj = get(db, country_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Country not found")
    return obj


@router.post("/", response_model=CountryRead, status_code=201)
def create_country(data: CountryCreate, db: Session = Depends(get_db)):
    """Создаёт новую страну."""
    return create(db, data.name, data.code)


@router.put("/{country_id}", response_model=CountryRead)
def update_country(country_id: int, data: CountryCreate, db: Session = Depends(get_db)):
    """Обновляет страну по её идентификатору."""
    obj = update(db, country_id, data.name, data.code)
    if not obj:
        raise HTTPException(status_code=404, detail="Country not found")
    return obj


@router.delete("/{country_id}", status_code=204)
def delete_country(country_id: int, db: Session = Depends(get_db)):
    """Удаляет страну по её идентификатору."""
    ok = delete(db, country_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Country not found")
