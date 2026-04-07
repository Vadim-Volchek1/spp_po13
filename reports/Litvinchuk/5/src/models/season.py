"""Модель сезона."""

from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base


class Season(Base):  # pylint: disable=too-few-public-methods
    """ORM-модель сезона."""

    __tablename__ = "seasons"

    id = Column(Integer, primary_key=True)
    league_id = Column(Integer, ForeignKey("leagues.id"), nullable=False)
    name = Column(String(20), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    league = relationship("League", back_populates="seasons")
    matches = relationship("Match", back_populates="season")
