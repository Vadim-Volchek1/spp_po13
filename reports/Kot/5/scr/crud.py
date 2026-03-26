from sqlalchemy.orm import Session
import models
import schemas


# ========== Students ==========
def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Student).offset(skip).limit(limit).all()


def get_student(db: Session, student_id: int):
    return (
        db.query(models.Student).filter(models.Student.student_id == student_id).first()
    )


def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def update_student(db: Session, student_id: int, student: schemas.StudentCreate):
    db_student = get_student(db, student_id)
    if db_student:
        for key, value in student.model_dump().items():
            setattr(db_student, key, value)
        db.commit()
        db.refresh(db_student)
    return db_student


def delete_student(db: Session, student_id: int):
    db_student = get_student(db, student_id)
    if db_student:
        db.delete(db_student)
        db.commit()
        return True
    return False


# ========== Teachers ==========
def get_teachers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Teacher).offset(skip).limit(limit).all()


def get_teacher(db: Session, teacher_id: int):
    return (
        db.query(models.Teacher).filter(models.Teacher.teacher_id == teacher_id).first()
    )


def create_teacher(db: Session, teacher: schemas.TeacherCreate):
    db_teacher = models.Teacher(**teacher.model_dump())
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher


def update_teacher(db: Session, teacher_id: int, teacher: schemas.TeacherCreate):
    db_teacher = get_teacher(db, teacher_id)
    if db_teacher:
        for key, value in teacher.model_dump().items():
            setattr(db_teacher, key, value)
        db.commit()
        db.refresh(db_teacher)
    return db_teacher


def delete_teacher(db: Session, teacher_id: int):
    db_teacher = get_teacher(db, teacher_id)
    if db_teacher:
        db.delete(db_teacher)
        db.commit()
        return True
    return False


# ========== Subjects ==========
def get_subjects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Subject).offset(skip).limit(limit).all()


def get_subject(db: Session, subject_id: int):
    return (
        db.query(models.Subject).filter(models.Subject.subject_id == subject_id).first()
    )


def create_subject(db: Session, subject: schemas.SubjectCreate):
    db_subject = models.Subject(**subject.model_dump())
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject


def update_subject(db: Session, subject_id: int, subject: schemas.SubjectCreate):
    db_subject = get_subject(db, subject_id)
    if db_subject:
        for key, value in subject.model_dump().items():
            setattr(db_subject, key, value)
        db.commit()
        db.refresh(db_subject)
    return db_subject


def delete_subject(db: Session, subject_id: int):
    db_subject = get_subject(db, subject_id)
    if db_subject:
        db.delete(db_subject)
        db.commit()
        return True
    return False


# ========== Grades ==========
def get_grades(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Grade).offset(skip).limit(limit).all()


def get_grade(db: Session, grade_id: int):
    return db.query(models.Grade).filter(models.Grade.grade_id == grade_id).first()


def get_student_grades(db: Session, student_id: int):
    return db.query(models.Grade).filter(models.Grade.student_id == student_id).all()


def create_grade(db: Session, grade: schemas.GradeCreate):
    db_grade = models.Grade(**grade.model_dump())
    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)
    return db_grade


def update_grade(db: Session, grade_id: int, grade: schemas.GradeCreate):
    db_grade = get_grade(db, grade_id)
    if db_grade:
        for key, value in grade.model_dump().items():
            setattr(db_grade, key, value)
        db.commit()
        db.refresh(db_grade)
    return db_grade


def delete_grade(db: Session, grade_id: int):
    db_grade = get_grade(db, grade_id)
    if db_grade:
        db.delete(db_grade)
        db.commit()
        return True
    return False


# ========== Attendance ==========
def get_attendances(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Attendance).offset(skip).limit(limit).all()


def get_attendance(db: Session, attendance_id: int):
    return (
        db.query(models.Attendance)
        .filter(models.Attendance.attendance_id == attendance_id)
        .first()
    )


def get_student_attendance(db: Session, student_id: int):
    return (
        db.query(models.Attendance)
        .filter(models.Attendance.student_id == student_id)
        .all()
    )


def create_attendance(db: Session, attendance: schemas.AttendanceCreate):
    db_attendance = models.Attendance(**attendance.model_dump())
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance


def update_attendance(
    db: Session, attendance_id: int, attendance: schemas.AttendanceCreate
):
    db_attendance = get_attendance(db, attendance_id)
    if db_attendance:
        for key, value in attendance.model_dump().items():
            setattr(db_attendance, key, value)
        db.commit()
        db.refresh(db_attendance)
    return db_attendance


def delete_attendance(db: Session, attendance_id: int):
    db_attendance = get_attendance(db, attendance_id)
    if db_attendance:
        db.delete(db_attendance)
        db.commit()
        return True
    return False
