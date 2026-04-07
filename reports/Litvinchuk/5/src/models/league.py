"""Модель Лиги."""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base


class League(Base):  # pylint: disable=too-few-public-methods
    """ORM-модель лиги."""

    __tablename__ = "leagues"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)

    country = relationship("Country", back_populates="leagues")
    seasons = relationship("Season", back_populates="league")
