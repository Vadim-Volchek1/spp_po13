from datetime import date
from sqlalchemy.orm import Session
from models import Faculty, Group, Student, Subject, Grade

# Faculty
def add_faculty(db: Session, name: str):
    faculty = Faculty(name=name)
    db.add(faculty)
    db.commit()
    db.refresh(faculty)
    return faculty

def get_faculties(db: Session):
    return db.query(Faculty).all()

def update_faculty(db: Session, faculty_id: int, name: str):
    faculty = db.get(Faculty, faculty_id)
    faculty.name = name
    db.commit()
    return faculty

def delete_faculty(db: Session, faculty_id: int):
    faculty = db.get(Faculty, faculty_id)
    db.delete(faculty)
    db.commit()

# Group
def add_group(db: Session, name: str, faculty_id: int):
    group = Group(name=name, faculty_id=faculty_id)
    db.add(group)
    db.commit()
    db.refresh(group)
    return group

def get_groups(db: Session):
    return db.query(Group).all()

def update_group(db: Session, group_id: int, name: str, faculty_id: int):
    group = db.get(Group, group_id)
    group.name = name
    group.faculty_id = faculty_id
    db.commit()
    return group

def delete_group(db: Session, group_id: int):
    group = db.get(Group, group_id)
    db.delete(group)
    db.commit()

# Student
def add_student(db: Session, first_name: str, last_name: str, birth_date: date, group_id: int):
    student = Student(first_name=first_name, last_name=last_name, birth_date=birth_date, group_id=group_id)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

def get_students(db: Session):
    return db.query(Student).all()

def update_student(db: Session, student_id: int, student_data: dict):
    student = db.get(Student, student_id)
    for key, value in student_data.items():
        setattr(student, key, value)
    db.commit()
    return student

def delete_student(db: Session, student_id: int):
    student = db.get(Student, student_id)
    db.delete(student)
    db.commit()

# Subject
def add_subject(db: Session, name: str):
    subject = Subject(name=name)
    db.add(subject)
    db.commit()
    db.refresh(subject)
    return subject

def get_subjects(db: Session):
    return db.query(Subject).all()

def update_subject(db: Session, subject_id: int, name: str):
    subject = db.get(Subject, subject_id)
    subject.name = name
    db.commit()
    return subject

def delete_subject(db: Session, subject_id: int):
    subject = db.get(Subject, subject_id)
    db.delete(subject)
    db.commit()

# Grade
def add_grade(db: Session, student_id: int, subject_id: int, grade_value: int, grade_date: date = date.today()):
    grade = Grade(student_id=student_id, subject_id=subject_id, grade=grade_value, date=grade_date)
    db.add(grade)
    db.commit()
    db.refresh(grade)
    return grade

def get_grades(db: Session):
    return db.query(Grade).all()

def update_grade(db: Session, grade_id: int, grade_value: int, grade_date: date):
    grade = db.get(Grade, grade_id)
    grade.grade = grade_value
    grade.date = grade_date
    db.commit()
    return grade

def delete_grade(db: Session, grade_id: int):
    grade = db.get(Grade, grade_id)
    db.delete(grade)
    db.commit()
