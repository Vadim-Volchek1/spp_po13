from sqlalchemy.orm import Session
from . import models, schemas


# Citizens
def get_citizens(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Citizen).offset(skip).limit(limit).all()


def get_citizen(db: Session, citizen_id: int):
    return db.query(models.Citizen).filter(models.Citizen.id == citizen_id).first()


def create_citizen(db: Session, citizen: schemas.CitizenCreate):
    db_obj = models.Citizen(**citizen.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_citizen(db: Session, citizen_id: int, citizen_data: schemas.CitizenUpdate):
    db_obj = get_citizen(db, citizen_id)
    if not db_obj:
        return None
    for field, value in citizen_data.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_citizen(db: Session, citizen_id: int):
    db_obj = get_citizen(db, citizen_id)
    if not db_obj:
        return None
    db.delete(db_obj)
    db.commit()
    return db_obj


# Employers
def get_employers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Employer).offset(skip).limit(limit).all()


def get_employer(db: Session, employer_id: int):
    return db.query(models.Employer).filter(models.Employer.id == employer_id).first()


def create_employer(db: Session, employer: schemas.EmployerCreate):
    db_obj = models.Employer(**employer.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_employer(db: Session, employer_id: int, employer_data: schemas.EmployerUpdate):
    db_obj = get_employer(db, employer_id)
    if not db_obj:
        return None
    for field, value in employer_data.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_employer(db: Session, employer_id: int):
    db_obj = get_employer(db, employer_id)
    if not db_obj:
        return None
    db.delete(db_obj)
    db.commit()
    return db_obj


# Vacancies
def get_vacancies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Vacancy).offset(skip).limit(limit).all()


def get_vacancy(db: Session, vacancy_id: int):
    return db.query(models.Vacancy).filter(models.Vacancy.id == vacancy_id).first()


def create_vacancy(db: Session, vacancy: schemas.VacancyCreate):
    db_obj = models.Vacancy(**vacancy.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_vacancy(db: Session, vacancy_id: int, vacancy_data: schemas.VacancyUpdate):
    db_obj = get_vacancy(db, vacancy_id)
    if not db_obj:
        return None
    for field, value in vacancy_data.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_vacancy(db: Session, vacancy_id: int):
    db_obj = get_vacancy(db, vacancy_id)
    if not db_obj:
        return None
    db.delete(db_obj)
    db.commit()
    return db_obj


# Applications
def get_applications(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Application).offset(skip).limit(limit).all()


def get_application(db: Session, application_id: int):
    return db.query(models.Application).filter(models.Application.id == application_id).first()


def create_application(db: Session, application: schemas.ApplicationCreate):
    db_obj = models.Application(**application.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_application(db: Session, application_id: int, application_data: schemas.ApplicationUpdate):
    db_obj = get_application(db, application_id)
    if not db_obj:
        return None
    for field, value in application_data.dict(exclude_unset=True).items():
        setattr(db_obj, field, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_application(db: Session, application_id: int):
    db_obj = get_application(db, application_id)
    if not db_obj:
        return None
    db.delete(db_obj)
    db.commit()
    return db_obj


# Skills
def get_skills(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Skill).offset(skip).limit(limit).all()


def get_skill(db: Session, skill_id: int):
    return db.query(models.Skill).filter(models.Skill.id == skill_id).first()


def create_skill(db: Session, skill: schemas.SkillCreate):
    db_obj = models.Skill(**skill.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_skill(db: Session, skill_id: int):
    db_obj = get_skill(db, skill_id)
    if not db_obj:
        return None
    db.delete(db_obj)
    db.commit()
    return db_obj
