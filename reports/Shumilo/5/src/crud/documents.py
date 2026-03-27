from sqlalchemy.orm import Session
from models import Document
from schemas.documents import DocumentCreate, DocumentUpdate


def get_all(db: Session):
    return db.query(Document).all()


def get(db: Session, document_id: int):
    return db.query(Document).filter(Document.id == document_id).first()


def create(db: Session, data: DocumentCreate):
    obj = Document(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update(db: Session, document_id: int, data: DocumentUpdate):
    obj = get(db, document_id)
    if not obj:
        return None
    for key, value in data.dict(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete(db: Session, document_id: int):
    obj = get(db, document_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
