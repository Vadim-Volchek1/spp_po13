from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
import crud
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Academic Performance API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Students endpoints
@app.post("/students/", response_model=schemas.Student)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    return crud.create_student(db, student)


@app.get("/students/", response_model=List[schemas.Student])
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_students(db, skip=skip, limit=limit)


@app.get("/students/{student_id}", response_model=schemas.Student)
def read_student(student_id: int, db: Session = Depends(get_db)):
    db_student = crud.get_student(db, student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student


@app.put("/students/{student_id}", response_model=schemas.Student)
def update_student(
    student_id: int, student: schemas.StudentCreate, db: Session = Depends(get_db)
):
    db_student = crud.update_student(db, student_id, student)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student


@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    if not crud.delete_student(db, student_id):
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}


# Teachers endpoints
@app.post("/teachers/", response_model=schemas.Teacher)
def create_teacher(teacher: schemas.TeacherCreate, db: Session = Depends(get_db)):
    return crud.create_teacher(db, teacher)


@app.get("/teachers/", response_model=List[schemas.Teacher])
def read_teachers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_teachers(db, skip=skip, limit=limit)


@app.get("/teachers/{teacher_id}", response_model=schemas.Teacher)
def read_teacher(teacher_id: int, db: Session = Depends(get_db)):
    db_teacher = crud.get_teacher(db, teacher_id)
    if db_teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return db_teacher


@app.put("/teachers/{teacher_id}", response_model=schemas.Teacher)
def update_teacher(
    teacher_id: int, teacher: schemas.TeacherCreate, db: Session = Depends(get_db)
):
    db_teacher = crud.update_teacher(db, teacher_id, teacher)
    if db_teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return db_teacher


@app.delete("/teachers/{teacher_id}")
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    if not crud.delete_teacher(db, teacher_id):
        raise HTTPException(status_code=404, detail="Teacher not found")
    return {"message": "Teacher deleted successfully"}


# Subjects endpoints
@app.post("/subjects/", response_model=schemas.Subject)
def create_subject(subject: schemas.SubjectCreate, db: Session = Depends(get_db)):
    return crud.create_subject(db, subject)


@app.get("/subjects/", response_model=List[schemas.Subject])
def read_subjects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_subjects(db, skip=skip, limit=limit)


@app.get("/subjects/{subject_id}", response_model=schemas.Subject)
def read_subject(subject_id: int, db: Session = Depends(get_db)):
    db_subject = crud.get_subject(db, subject_id)
    if db_subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")
    return db_subject


@app.put("/subjects/{subject_id}", response_model=schemas.Subject)
def update_subject(
    subject_id: int, subject: schemas.SubjectCreate, db: Session = Depends(get_db)
):
    db_subject = crud.update_subject(db, subject_id, subject)
    if db_subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")
    return db_subject


@app.delete("/subjects/{subject_id}")
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    if not crud.delete_subject(db, subject_id):
        raise HTTPException(status_code=404, detail="Subject not found")
    return {"message": "Subject deleted successfully"}


# Grades endpoints
# ========== Grades endpoints ==========
@app.post("/grades/", response_model=schemas.Grade, status_code=status.HTTP_201_CREATED)
def create_grade(grade: schemas.GradeCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_grade(db, grade)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/grades/", response_model=List[schemas.Grade])
def read_grades(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        return crud.get_grades(db, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading grades: {str(e)}")


@app.get("/grades/student/{student_id}", response_model=List[schemas.Grade])
def read_student_grades(student_id: int, db: Session = Depends(get_db)):
    try:
        return crud.get_student_grades(db, student_id)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error reading student grades: {str(e)}"
        )


@app.get("/grades/{grade_id}", response_model=schemas.Grade)
def read_grade(grade_id: int, db: Session = Depends(get_db)):
    db_grade = crud.get_grade(db, grade_id)
    if db_grade is None:
        raise HTTPException(status_code=404, detail="Grade not found")
    return db_grade


@app.put("/grades/{grade_id}", response_model=schemas.Grade)
def update_grade(
    grade_id: int, grade: schemas.GradeCreate, db: Session = Depends(get_db)
):
    db_grade = crud.update_grade(db, grade_id, grade)
    if db_grade is None:
        raise HTTPException(status_code=404, detail="Grade not found")
    return db_grade


@app.delete("/grades/{grade_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_grade(grade_id: int, db: Session = Depends(get_db)):
    if not crud.delete_grade(db, grade_id):
        raise HTTPException(status_code=404, detail="Grade not found")
    return None


# Attendance endpoints
@app.post("/attendances/", response_model=schemas.Attendance)
def create_attendance(
    attendance: schemas.AttendanceCreate, db: Session = Depends(get_db)
):
    return crud.create_attendance(db, attendance)


@app.get("/attendances/", response_model=List[schemas.Attendance])
def read_attendances(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_attendances(db, skip=skip, limit=limit)


@app.get("/attendances/student/{student_id}", response_model=List[schemas.Attendance])
def read_student_attendance(student_id: int, db: Session = Depends(get_db)):
    return crud.get_student_attendance(db, student_id)


@app.get("/attendances/{attendance_id}", response_model=schemas.Attendance)
def read_attendance(attendance_id: int, db: Session = Depends(get_db)):
    db_attendance = crud.get_attendance(db, attendance_id)
    if db_attendance is None:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    return db_attendance


@app.put("/attendances/{attendance_id}", response_model=schemas.Attendance)
def update_attendance(
    attendance_id: int,
    attendance: schemas.AttendanceCreate,
    db: Session = Depends(get_db),
):
    db_attendance = crud.update_attendance(db, attendance_id, attendance)
    if db_attendance is None:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    return db_attendance


@app.delete("/attendances/{attendance_id}")
def delete_attendance(attendance_id: int, db: Session = Depends(get_db)):
    if not crud.delete_attendance(db, attendance_id):
        raise HTTPException(status_code=404, detail="Attendance record not found")
    return {"message": "Attendance record deleted successfully"}


@app.get("/")
def root():
    return {"message": "Academic Performance API is running", "docs": "/docs"}
