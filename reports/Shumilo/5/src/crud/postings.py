from sqlalchemy.orm import Session
from models import Posting
from schemas.postings import PostingCreate, PostingUpdate


def get_all(db: Session):
    return db.query(Posting).all()


def get(db: Session, posting_id: int):
    return db.query(Posting).filter(Posting.id == posting_id).first()


def create(db: Session, data: PostingCreate):
    obj = Posting(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update(db: Session, posting_id: int, data: PostingUpdate):
    obj = get(db, posting_id)
    if not obj:
        return None
    for key, value in data.dict(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete(db: Session, posting_id: int):
    obj = get(db, posting_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
