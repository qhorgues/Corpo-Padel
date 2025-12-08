# ============================================
# FICHIER : backend/app/models/models.py
# ============================================

from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Date, Time, CheckConstraint
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    last_name = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    company = Column(String, nullable=False)
    license_number = Column(String, nullable=False)
    birth_date = Column(DateTime(timezone=True), nullable=False)
    photo_url = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)  # JOUEUR ou ADMINISTRATEUR
    is_active = Column(Boolean, default=True)
    must_change_password = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Players(Base):
    __tablename__ = "players"
    __table_args__ = (
        CheckConstraint("license_number GLOB 'L[0-9][0-9][0-9][0-9][0-9][0-9]'", name='chk_license_format'),
    )
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    company = Column(String, nullable=False)
    license_number = Column(String, nullable=False, unique=True)
    birth_date = Column(Date, nullable=True)
    photo_url = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), unique=True, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class LoginAttempt(Base):
    __tablename__ = "login_attempts"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True, nullable=False)
    attempts_count = Column(Integer, default=0)
    last_attempt = Column(DateTime(timezone=True))
    locked_until = Column(DateTime(timezone=True), nullable=True)

class Pools(Base):
    __tablename__ = "pools"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
class Teams(Base):
    __tablename__ = "teams"
    __table_args__ = (
        CheckConstraint('player1_id != player2_id', name='chk_different_players'),
    )
    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, nullable=False)
    player1_id = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"), nullable=False)
    player2_id = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"), nullable=False)
    pool_id = Column(Integer, ForeignKey("pools.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
class Matches(Base):
    __tablename__ = "matches"
    __table_args__ = (
        CheckConstraint('court_number BETWEEN 1 AND 10', name='chk_court_number'),
        CheckConstraint("status IN ('A_VENIR', 'TERMINE', 'ANNULE')", name='chk_status'),
        CheckConstraint('team1_id != team2_id', name='chk_different_teams'),
    )
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    team1_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"), nullable=False)
    team2_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"), nullable=False)
    court_number = Column(Integer, nullable=False)
    status = Column(String, nullable=False, default='A_VENIR')
    score_team1 = Column(String, nullable=True)
    score_team2 = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Events(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    event_date = Column(Date, nullable=False)
    event_time = Column(Time, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())