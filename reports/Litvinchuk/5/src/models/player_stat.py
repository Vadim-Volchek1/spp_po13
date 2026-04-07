"""Модель Статистики игрока в матче."""

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.database import Base


class PlayerStat(Base):  # pylint: disable=too-few-public-methods
    """ORM-модель статистики игрока."""

    __tablename__ = "player_stats"

    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=False)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)

    minutes_played = Column(Integer, nullable=False, default=0)
    goals = Column(Integer, nullable=False, default=0)
    assists = Column(Integer, nullable=False, default=0)
    yellow_cards = Column(Integer, nullable=False, default=0)
    red_cards = Column(Integer, nullable=False, default=0)

    match = relationship("Match", back_populates="player_stats")
    player = relationship("Player", back_populates="stats")
    team = relationship("Team", back_populates="player_stats")
