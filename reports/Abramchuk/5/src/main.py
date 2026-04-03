from datetime import date as dt_date

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import SessionLocal, engine, Base
import crud

# Создание всех таблиц
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Dekanat API")

# Подключение к БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic модели
class FacultyModel(BaseModel):
    name: str

class GroupModel(BaseModel):
    name: str
    faculty_id: int

class StudentModel(BaseModel):
    first_name: str
    last_name: str
    birth_date: dt_date
    group_id: int

class SubjectModel(BaseModel):
    name: str

class GradeModel(BaseModel):
    student_id: int
    subject_id: int
    grade: int
    date: dt_date = dt_date.today()

# Endpoints Faculty
@app.post("/faculties/")
def create_faculty(faculty: FacultyModel, db: Session = Depends(get_db)):
    return crud.add_faculty(db, faculty.name)

@app.get("/faculties/")
def read_faculties(db: Session = Depends(get_db)):
    return crud.get_faculties(db)

@app.put("/faculties/{faculty_id}")
def update_faculty(faculty_id: int, faculty: FacultyModel, db: Session = Depends(get_db)):
    return crud.update_faculty(db, faculty_id, faculty.name)

@app.delete("/faculties/{faculty_id}")
def delete_faculty(faculty_id: int, db: Session = Depends(get_db)):
    crud.delete_faculty(db, faculty_id)
    return {"message": "Faculty deleted"}

# Endpoints Group
@app.post("/groups/")
def create_group(group: GroupModel, db: Session = Depends(get_db)):
    return crud.add_group(db, group.name, group.faculty_id)

@app.get("/groups/")
def read_groups(db: Session = Depends(get_db)):
    return crud.get_groups(db)

@app.put("/groups/{group_id}")
def update_group(group_id: int, group: GroupModel, db: Session = Depends(get_db)):
    return crud.update_group(db, group_id, group.name, group.faculty_id)

@app.delete("/groups/{group_id}")
def delete_group(group_id: int, db: Session = Depends(get_db)):
    crud.delete_group(db, group_id)
    return {"message": "Group deleted"}

# Endpoints Student
@app.post("/students/")
def create_student(student: StudentModel, db: Session = Depends(get_db)):
    return crud.add_student(db, student.first_name, student.last_name, student.birth_date, student.group_id)

@app.get("/students/")
def read_students(db: Session = Depends(get_db)):
    return crud.get_students(db)

@app.put("/students/{student_id}")
def update_student(student_id: int, db: Session = Depends(get_db)):
    return crud.update_student(db, student_id, {
        "first_name": "John",
        "last_name": "Doe",
        "birth_date": dt_date(2000,1,1),
        "group_id": 1
    })

@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    crud.delete_student(db, student_id)
    return {"message": "Student deleted"}

# Endpoints Subject
@app.post("/subjects/")
def create_subject(subject: SubjectModel, db: Session = Depends(get_db)):
    return crud.add_subject(db, subject.name)

@app.get("/subjects/")
def read_subjects(db: Session = Depends(get_db)):
    return crud.get_subjects(db)

@app.put("/subjects/{subject_id}")
def update_subject(subject_id: int, subject: SubjectModel, db: Session = Depends(get_db)):
    return crud.update_subject(db, subject_id, subject.name)

@app.delete("/subjects/{subject_id}")
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    crud.delete_subject(db, subject_id)
    return {"message": "Subject deleted"}

# Endpoints Grade
@app.post("/grades/")
def create_grade(grade: GradeModel, db: Session = Depends(get_db)):
    return crud.add_grade(db, grade.student_id, grade.subject_id, grade.grade, grade.date)

@app.get("/grades/")
def read_grades(db: Session = Depends(get_db)):
    return crud.get_grades(db)

@app.put("/grades/{grade_id}")
def update_grade(grade_id: int, grade: GradeModel, db: Session = Depends(get_db)):
    return crud.update_grade(db, grade_id, grade.grade, grade.date)

@app.delete("/grades/{grade_id}")
def delete_grade(grade_id: int, db: Session = Depends(get_db)):
    crud.delete_grade(db, grade_id)
    return {"message": "Grade deleted"}
