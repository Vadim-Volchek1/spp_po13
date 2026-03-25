from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from .. import schemas, crud
from ..database import get_db

router = APIRouter(prefix="/vacancies", tags=["vacancies"])


@router.get("/", response_model=List[schemas.VacancyOut])
def read_vacancies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_vacancies(db, skip=skip, limit=limit)


@router.get("/{vacancy_id}", response_model=schemas.VacancyOut)
def read_vacancy(vacancy_id: int, db: Session = Depends(get_db)):
    vacancy = crud.get_vacancy(db, vacancy_id)
    if not vacancy:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    return vacancy


@router.post("/", response_model=schemas.VacancyOut)
def create_vacancy(vacancy: schemas.VacancyCreate, db: Session = Depends(get_db)):
    return crud.create_vacancy(db, vacancy)


@router.put("/{vacancy_id}", response_model=schemas.VacancyOut)
def update_vacancy(vacancy_id: int, vacancy_data: schemas.VacancyUpdate, db: Session = Depends(get_db)):
    vacancy = crud.update_vacancy(db, vacancy_id, vacancy_data)
    if not vacancy:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    return vacancy


@router.delete("/{vacancy_id}")
def delete_vacancy(vacancy_id: int, db: Session = Depends(get_db)):
    vacancy = crud.delete_vacancy(db, vacancy_id)
    if not vacancy:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    return {"detail": "Vacancy deleted"}
