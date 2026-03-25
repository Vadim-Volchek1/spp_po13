from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from .. import schemas, crud
from ..database import get_db

router = APIRouter(prefix="/employers", tags=["employers"])


@router.get("/", response_model=List[schemas.EmployerOut])
def read_employers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_employers(db, skip=skip, limit=limit)


@router.get("/{employer_id}", response_model=schemas.EmployerOut)
def read_employer(employer_id: int, db: Session = Depends(get_db)):
    employer = crud.get_employer(db, employer_id)
    if not employer:
        raise HTTPException(status_code=404, detail="Employer not found")
    return employer


@router.post("/", response_model=schemas.EmployerOut)
def create_employer(employer: schemas.EmployerCreate, db: Session = Depends(get_db)):
    return crud.create_employer(db, employer)


@router.put("/{employer_id}", response_model=schemas.EmployerOut)
def update_employer(employer_id: int, employer_data: schemas.EmployerUpdate, db: Session = Depends(get_db)):
    employer = crud.update_employer(db, employer_id, employer_data)
    if not employer:
        raise HTTPException(status_code=404, detail="Employer not found")
    return employer


@router.delete("/{employer_id}")
def delete_employer(employer_id: int, db: Session = Depends(get_db)):
    employer = crud.delete_employer(db, employer_id)
    if not employer:
        raise HTTPException(status_code=404, detail="Employer not found")
    return {"detail": "Employer deleted"}
