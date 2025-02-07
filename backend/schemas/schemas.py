from dataclasses import dataclass, field
from datetime import datetime
from typing import List
import logging
from app.database import db

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import registry
from sqlalchemy.ext.declarative import declarative_base
from entities.player import Player
from entities.team import Team
from entities.session import Session
from entities.attendance import Attendance

logging.basicConfig()
logging.getLogger('sqlalchemy').setLevel(logging.ERROR)


mapper_registry = registry()
Base = declarative_base()


@dataclass
class PlayerTable(db.Model):
    __tablename__ = 'players'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String)
    dob: datetime = Column(DateTime)
    joined_group_date: datetime = Column(DateTime)
    

@dataclass
class TeamTable(db.Model):
    __tablename__ = 'teams'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String)
    coach: str = Column(String)
    manager: str = Column(String)
    league: str = Column(String)
    players: List[Player] = field(default_factory=list)


@dataclass
class SessionTable(db.Model):
    __tablename__ = 'sessions'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    datetime: datetime = Column(DateTime) # type: ignore
    location: str = Column(String)
    session_type: str = Column(String)
    teams: List[str] = field(default_factory=list)
    attendance_records: List[Attendance] = field(default_factory=list)


@dataclass
class AttendanceTable(db.Model):
    __tablename__ = 'attendance'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    session_id: int = Column(Integer)
    player_id: int = Column(Integer)
    status: str = Column(String)


# Map the dataclass to the database table
def player_entity_mapper():
    mapper_registry.map_imperatively(Player, PlayerTable.__table__)
    logging.info('Mapped Player to PlayerTable')

def team_entity_mapper():
    mapper_registry.map_imperatively(Team, TeamTable.__table__)
    logging.info('Mapped Team to TeamTable')

def session_entity_mapper():
    mapper_registry.map_imperatively(Session, SessionTable.__table__)
    logging.info('Mapped Session to SessionTable')

def attendance_entity_mapper():
    mapper_registry.map_imperatively(Attendance, AttendanceTable.__table__)
    logging.info('Mapped Attendance to AttendanceTable')
