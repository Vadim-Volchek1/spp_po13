from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from .. import schemas, crud
from ..database import get_db

router = APIRouter(prefix="/citizens", tags=["citizens"])


@router.get("/", response_model=List[schemas.CitizenOut])
def read_citizens(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_citizens(db, skip=skip, limit=limit)


@router.get("/{citizen_id}", response_model=schemas.CitizenOut)
def read_citizen(citizen_id: int, db: Session = Depends(get_db)):
    citizen = crud.get_citizen(db, citizen_id)
    if not citizen:
        raise HTTPException(status_code=404, detail="Citizen not found")
    return citizen


@router.post("/", response_model=schemas.CitizenOut)
def create_citizen(citizen: schemas.CitizenCreate, db: Session = Depends(get_db)):
    return crud.create_citizen(db, citizen)


@router.put("/{citizen_id}", response_model=schemas.CitizenOut)
def update_citizen(citizen_id: int, citizen_data: schemas.CitizenUpdate, db: Session = Depends(get_db)):
    citizen = crud.update_citizen(db, citizen_id, citizen_data)
    if not citizen:
        raise HTTPException(status_code=404, detail="Citizen not found")
    return citizen


@router.delete("/{citizen_id}")
def delete_citizen(citizen_id: int, db: Session = Depends(get_db)):
    citizen = crud.delete_citizen(db, citizen_id)
    if not citizen:
        raise HTTPException(status_code=404, detail="Citizen not found")
    return {"detail": "Citizen deleted"}
