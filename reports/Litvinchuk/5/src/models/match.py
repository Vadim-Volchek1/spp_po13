"""Модель матча."""

from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.database import Base


class Match(Base):  # pylint: disable=too-few-public-methods
    """ORM-Модель матча."""

    __tablename__ = "matches"

    id = Column(Integer, primary_key=True)
    season_id = Column(Integer, ForeignKey("seasons.id"), nullable=False)
    home_team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    away_team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    match_date = Column(DateTime, nullable=False)
    home_goals = Column(Integer, nullable=False, default=0)
    away_goals = Column(Integer, nullable=False, default=0)

    __table_args__ = (CheckConstraint("home_team_id <> away_team_id", name="chk_diff_teams"),)

    season = relationship("Season", back_populates="matches")
    home_team = relationship("Team", foreign_keys=[home_team_id], back_populates="home_matches")
    away_team = relationship("Team", foreign_keys=[away_team_id], back_populates="away_matches")
    player_stats = relationship("PlayerStat", back_populates="match")
