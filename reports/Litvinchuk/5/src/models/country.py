"""Модель страны."""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base


class Country(Base):  # pylint: disable=too-few-public-methods
    """ORM-модель страны."""

    __tablename__ = "countries"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    code = Column(String(3), nullable=False, unique=True)

    leagues = relationship("League", back_populates="country")
    teams = relationship("Team", back_populates="country")
    players = relationship("Player", back_populates="country")
