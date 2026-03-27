from sqlalchemy.orm import Session
from models import Counterparty
from schemas.counterparties import CounterpartyCreate, CounterpartyUpdate


def get_all(db: Session):
    return db.query(Counterparty).all()


def get(db: Session, counterparty_id: int):
    return db.query(Counterparty).filter(Counterparty.id == counterparty_id).first()


def create(db: Session, data: CounterpartyCreate):
    obj = Counterparty(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update(db: Session, counterparty_id: int, data: CounterpartyUpdate):
    obj = get(db, counterparty_id)
    if not obj:
        return None
    for key, value in data.dict(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete(db: Session, counterparty_id: int):
    obj = get(db, counterparty_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
