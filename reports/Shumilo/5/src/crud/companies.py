from sqlalchemy.orm import Session
from models import Company
from schemas.companies import CompanyCreate, CompanyUpdate


def get_all(db: Session):
    return db.query(Company).all()


def get(db: Session, company_id: int):
    return db.query(Company).filter(Company.id == company_id).first()


def create(db: Session, data: CompanyCreate):
    obj = Company(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update(db: Session, company_id: int, data: CompanyUpdate):
    obj = get(db, company_id)
    if not obj:
        return None
    for key, value in data.dict(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete(db: Session, company_id: int):
    obj = get(db, company_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
