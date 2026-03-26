from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional


class StudentBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    enrollment_date: date
    group_name: str


class StudentCreate(StudentBase):
    pass


class Student(StudentBase):
    student_id: int

    class Config:
        from_attributes = True


class TeacherBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    hire_date: date
    department: str


class TeacherCreate(TeacherBase):
    pass


class Teacher(TeacherBase):
    teacher_id: int

    class Config:
        from_attributes = True


class SubjectBase(BaseModel):
    subject_name: str
    credits: int
    teacher_id: Optional[int] = None


class SubjectCreate(SubjectBase):
    pass


class Subject(SubjectBase):
    subject_id: int

    class Config:
        from_attributes = True


class GradeBase(BaseModel):
    student_id: int
    subject_id: int
    grade: int
    grade_date: date
    semester: int


class GradeCreate(GradeBase):
    pass


class Grade(GradeBase):
    grade_id: int

    class Config:
        from_attributes = True


class AttendanceBase(BaseModel):
    student_id: int
    subject_id: int
    attendance_date: date
    status: str


class AttendanceCreate(AttendanceBase):
    pass


class Attendance(AttendanceBase):
    attendance_id: int

    class Config:
        from_attributes = True
