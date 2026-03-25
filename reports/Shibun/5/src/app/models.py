from sqlalchemy import Column, Integer, String, Date, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base


class Citizen(Base):
    __tablename__ = "citizens"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    birth_date = Column(Date)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String)
    registration_date = Column(Date, default=datetime.utcnow)

    applications = relationship("Application", back_populates="citizen")
    skills = relationship("CitizenSkill", back_populates="citizen")


class Employer(Base):
    __tablename__ = "employers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    inn = Column(String, unique=True, index=True, nullable=False)
    address = Column(String)
    contact_email = Column(String)

    vacancies = relationship("Vacancy", back_populates="employer")


class Vacancy(Base):
    __tablename__ = "vacancies"

    id = Column(Integer, primary_key=True, index=True)
    employer_id = Column(Integer, ForeignKey("employers.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    salary_from = Column(Integer)
    salary_to = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    employer = relationship("Employer", back_populates="vacancies")
    applications = relationship("Application", back_populates="vacancy")


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    citizen_id = Column(Integer, ForeignKey("citizens.id"), nullable=False)
    vacancy_id = Column(Integer, ForeignKey("vacancies.id"), nullable=False)
    status = Column(String, default="new")
    applied_at = Column(DateTime, default=datetime.utcnow)

    citizen = relationship("Citizen", back_populates="applications")
    vacancy = relationship("Vacancy", back_populates="applications")


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    citizens = relationship("CitizenSkill", back_populates="skill")


class CitizenSkill(Base):
    __tablename__ = "citizen_skills"

    citizen_id = Column(Integer, ForeignKey("citizens.id"), primary_key=True)
    skill_id = Column(Integer, ForeignKey("skills.id"), primary_key=True)

    citizen = relationship("Citizen", back_populates="skills")
    skill = relationship("Skill", back_populates="citizens")
