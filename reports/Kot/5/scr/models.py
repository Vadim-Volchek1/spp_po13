from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Student(Base):
    __tablename__ = "students"
    student_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    enrollment_date = Column(Date, nullable=False)
    group_name = Column(String(20), nullable=False)
    grades = relationship("Grade", back_populates="student")
    attendances = relationship("Attendance", back_populates="student")


class Teacher(Base):
    __tablename__ = "teachers"
    teacher_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hire_date = Column(Date, nullable=False)
    department = Column(String(100), nullable=False)
    subjects = relationship("Subject", back_populates="teacher")


class Subject(Base):
    __tablename__ = "subjects"
    subject_id = Column(Integer, primary_key=True, index=True)
    subject_name = Column(String(100), unique=True, nullable=False)
    credits = Column(Integer, nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.teacher_id"))
    teacher = relationship("Teacher", back_populates="subjects")
    grades = relationship("Grade", back_populates="subject")
    attendances = relationship("Attendance", back_populates="subject")


class Grade(Base):
    __tablename__ = "grades"
    grade_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.student_id"))
    subject_id = Column(Integer, ForeignKey("subjects.subject_id"))
    grade = Column(Integer, nullable=False)
    grade_date = Column(Date, nullable=False)
    semester = Column(Integer, nullable=False)
    student = relationship("Student", back_populates="grades")
    subject = relationship("Subject", back_populates="grades")


class Attendance(Base):
    __tablename__ = "attendance"
    attendance_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.student_id"))
    subject_id = Column(Integer, ForeignKey("subjects.subject_id"))
    attendance_date = Column(Date, nullable=False)
    status = Column(String(20), nullable=False)
    student = relationship("Student", back_populates="attendances")
    subject = relationship("Subject", back_populates="attendances")
