# ============================================
# FICHIER : backend/app/models/models.py
# ============================================

from sqlalchemy import Column, Integer, String, Boolean, Date, Time, DateTime, Text, ForeignKey, CheckConstraint, func
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    """
    This class represents a user.
    """
    __tablename__ = "users"

    # This attribute represents the user's id.
    id = Column(Integer, primary_key=True, index=True)

    # This attribute represents the user's email.
    email = Column(String, nullable=False, unique=True)

    # This attribute represents the user's password.
    password_hash = Column(String, nullable=False)

    # This attribute represents the user's role. Only JOUEUR or ADMINISTRATEUR.
    role = Column(
        String,
        CheckConstraint("role IN ('JOUEUR', 'ADMINISTRATEUR')"),
        nullable=False
    )

    # This attribute represents if the user is active.
    is_active = Column(Boolean, default=True)

    # This attribute represents if the user need to change their password.
    must_change_password = Column(Boolean, default=False)

    # This attribute represents when the user is created.
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # This attribute represents when the user is updated.
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


    # This is the player information linked to the user.
    player = relationship("Player", back_populates="user", uselist=False, cascade="all, delete-orphan")



class Player(Base):
    """
    This class represents a player.
    """
    __tablename__ = "players"

    # This attribute is the player's id.
    id = Column(Integer, primary_key=True)

    # This attribute is the player's first name.
    first_name = Column(String, nullable=False)

    # This attribute is the player's last name.
    last_name = Column(String, nullable=False)

    # This attribute is the player's company name.
    company = Column(String, nullable=False)

    # This attribute is the player's license number.
    license_number = Column(
        String,
        nullable=False,
        unique=True
    )

    # This attribute is the player's birth date.
    birth_date = Column(Date)

    # This attribute is the player's picture profile.
    photo_url = Column(Text)

    # This attribute represents when the player is created.
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # This attribute represents when the player is updated.
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # This "attribute" add a constrain to the license number.
    __table_args__ = (
        CheckConstraint(
            "license_number GLOB 'L[0-9][0-9][0-9][0-9][0-9][0-9]'",
            name="chk_license_format"
        ),
    )


    # This attribute is the foreign key to the user account.
    user_id = Column(ForeignKey("users.id"), index=True)

    # This is the user linked to the player.
    user = relationship("User", back_populates="player")



class Pool(Base):
    """
    This class represents a pool.
    """
    __tablename__ = "pools"

    # This attribute is the pool's id.
    id = Column(Integer, primary_key=True)

    # This attribute is the pool's name.
    name = Column(String, nullable=False, unique=True)

    # This attribute is when the pool was created.
    created_at = Column(DateTime(timezone=True), server_default=func.now())


    # This is the teams in this pool.
    teams = relationship("Team", back_populates="pool")



class Team(Base):
    """
    This class represents a team.
    """
    __tablename__ = "teams"

    # This attribute is the team's id.
    id = Column(Integer, primary_key=True)

    # This attribute is the team's company name.
    company = Column(String, nullable=False)

    # This attribute represents when the team is created.
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # This attribute represents when the team is updated.
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


    # This attribute is the first member of the team.
    player1_id = Column(ForeignKey("players.id"), nullable=False, index=True)

    # This attribute is the second member of the team.
    player2_id = Column(ForeignKey("players.id"), nullable=False, index=True)

    # This "attribute" checks if the players are not the same.
    __table_args__ = (
        CheckConstraint("player1_id != player2_id", name="chk_different_players"),
    )

    # This attribute is the pool of the team.
    pool_id = Column(ForeignKey("pools.id", ondelete="SET NULL"), index=True)

    # The first player linked.
    player1 = relationship("Player", foreign_keys=[player1_id])

    # The second player linked.
    player2 = relationship("Player", foreign_keys=[player2_id])

    # The pool linked.
    pool = relationship("Pool", back_populates="teams")



class Event(Base):
    """
    This class represents a event.
    """
    __tablename__ = "events"

    # This attribute is the event's id.
    id = Column(Integer, primary_key=True)

    # This attribute is the event's date.
    event_date = Column(Date, nullable=False, index=True)

    # This attribute is the event's time.
    event_time = Column(Time, nullable=False)

    # This attribute represents when the event is created.
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # This attribute represents when the event is updated.
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    matches = relationship("Match", back_populates="event", cascade="all, delete-orphan")



class Match(Base):
    """
    This class represents a match.
    """
    __tablename__ = "matches"

    # This attribute is the match's id.
    id = Column(Integer, primary_key=True, index=True)

    # This attribute is the court number (between 1 and 10).
    court_number = Column(
        Integer,
        CheckConstraint("court_number BETWEEN 1 AND 10"),
        nullable=False
    )

    # This attribute is the status of the match. A_VENIR, TERMINE, ANNULE.
    status = Column(
        String,
        CheckConstraint("status IN ('A_VENIR', 'TERMINE', 'ANNULE')"),
        nullable=False,
        default="A_VENIR",
        index=True
    )

    # This attribute is the score of the first team.
    score_team1 = Column(String)

    # This attribute is the score of the second team.
    score_team2 = Column(String)

    # This attribute represents when the match is created.
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # This attribute represents when the match is updated.
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


    # This attribute is the event's id.
    event_id = Column(ForeignKey("events.id"), nullable=False)

    # This attribute is the first team.
    team1_id = Column(ForeignKey("teams.id"), nullable=False, index=True)

    # This attribute is the second team.
    team2_id = Column(ForeignKey("teams.id", ondelete="CASCADE"), nullable=False, index=True)

    # This "attribute" check if the team don't play against itself.
    __table_args__ = (
        CheckConstraint("team1_id != team2_id", name="chk_different_teams"),
    )

    # This is the event linked.
    event = relationship("Event", back_populates="matches")

    # This is the first team linked.
    team1 = relationship("Team", foreign_keys=[team1_id])

    # This is the second team linked.
    team2 = relationship("Team", foreign_keys=[team2_id])



class LoginAttempt(Base):
    """
    This class represent when a user has their account blocked.
    """
    __tablename__ = "login_attempts"

    # This attribute is the id of the entity.
    id = Column(Integer, primary_key=True, index=True)

    # This attribute is the blocked account's email.
    email = Column(String, index=True, nullable=False, unique=True)

    # This attribute is the number of attempts.
    attempts_count = Column(Integer, default=0)

    # This attribute is when was the last attempts.
    last_attempt = Column(DateTime(timezone=True))

    # This attribute is when the account is unlucked.
    locked_until = Column(DateTime(timezone=True), nullable=True)
