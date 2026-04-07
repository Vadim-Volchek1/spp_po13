"""Модель команды."""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base


class Team(Base):  # pylint: disable=too-few-public-methods
    """ORM-модель команды."""

    __tablename__ = "teams"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    country_id = Column(Integer, ForeignKey("countries.id"))
    founded_year = Column(Integer)

    country = relationship("Country", back_populates="teams")

    home_matches = relationship(
        "Match",
        back_populates="home_team",
        foreign_keys="Match.home_team_id",
    )

    away_matches = relationship(
        "Match",
        back_populates="away_team",
        foreign_keys="Match.away_team_id",
    )

    player_stats = relationship("PlayerStat", back_populates="team")
