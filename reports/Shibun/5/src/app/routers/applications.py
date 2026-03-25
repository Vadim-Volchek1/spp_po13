from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from .. import schemas, crud
from ..database import get_db

router = APIRouter(prefix="/applications", tags=["applications"])


@router.get("/", response_model=List[schemas.ApplicationOut])
def read_applications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_applications(db, skip=skip, limit=limit)


@router.get("/{application_id}", response_model=schemas.ApplicationOut)
def read_application(application_id: int, db: Session = Depends(get_db)):
    application = crud.get_application(db, application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application


@router.post("/", response_model=schemas.ApplicationOut)
def create_application(application: schemas.ApplicationCreate, db: Session = Depends(get_db)):
    return crud.create_application(db, application)


@router.put("/{application_id}", response_model=schemas.ApplicationOut)
def update_application(application_id: int, application_data: schemas.ApplicationUpdate, db: Session = Depends(get_db)):
    application = crud.update_application(db, application_id, application_data)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application


@router.delete("/{application_id}")
def delete_application(application_id: int, db: Session = Depends(get_db)):
    application = crud.delete_application(db, application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return {"detail": "Application deleted"}
