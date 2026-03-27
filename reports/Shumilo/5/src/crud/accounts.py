from sqlalchemy.orm import Session
from models import Account
from schemas.accounts import AccountCreate, AccountUpdate


def get_all(db: Session):
    return db.query(Account).all()


def get(db: Session, account_id: int):
    return db.query(Account).filter(Account.id == account_id).first()


def create(db: Session, data: AccountCreate):
    obj = Account(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update(db: Session, account_id: int, data: AccountUpdate):
    obj = get(db, account_id)
    if not obj:
        return None
    for key, value in data.dict(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete(db: Session, account_id: int):
    obj = get(db, account_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
