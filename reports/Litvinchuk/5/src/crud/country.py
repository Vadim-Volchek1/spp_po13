"""CRUD-операции для сущности Country."""

from sqlalchemy.orm import Session

from src.models.country import Country


def get_all(db: Session):
    """Возвращает список всех стран."""
    return db.query(Country).all()


def get(db: Session, country_id: int):
    """Возвращает страну по её идентификатору."""
    return db.query(Country).filter(Country.id == country_id).first()


def create(db: Session, name: str, code: str):
    """Создаёт новую страну."""
    country = Country(name=name, code=code)
    db.add(country)
    db.commit()
    db.refresh(country)
    return country


def update(db: Session, country_id: int, name: str, code: str):
    """Обновляет данные страны по её идентификатору."""
    country = get(db, country_id)
    if not country:
        return None

    country.name = name
    country.code = code

    db.commit()
    db.refresh(country)
    return country


def delete(db: Session, country_id: int):
    """Удаляет страну по её идентификатору."""
    country = get(db, country_id)
    if not country:
        return False

    db.delete(country)
    db.commit()
    return True
