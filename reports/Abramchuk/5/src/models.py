from datetime import date
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Faculty(Base):
    __tablename__ = "faculties"

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)
    groups = relationship("Group", back_populates="faculty")

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    faculty_id = Column(Integer, ForeignKey("faculties.id"))

    name = Column(String, nullable=False)
    faculty = relationship("Faculty", back_populates="groups")
    students = relationship("Student", back_populates="group")

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"))

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)

    group = relationship("Group", back_populates="students")
    grades = relationship("Grade", back_populates="student")

class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    grades = relationship("Grade", back_populates="subject")

class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    subject_id = Column(Integer, ForeignKey("subjects.id"))

    grade = Column(Integer, nullable=False)
    date = Column(Date, default=date.today)

    student = relationship("Student", back_populates="grades")
    subject = relationship("Subject", back_populates="grades")
