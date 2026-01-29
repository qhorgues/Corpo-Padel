# app/schemas/match.py
from datetime import datetime, time
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from .team import TeamResponse

class EventMini(BaseModel):
    """
    This is a soft version of a event.
    """
    # The date of the event.
    event_date: datetime

    # The time of the event.
    event_time: time

    model_config = ConfigDict(
        from_attributes=True
    )


class MatchStatus(str, Enum):
    """
    This is the status of a match.
    """

    # The match is not played yet.
    A_VENIR = "A_VENIR"

    # The match is playing.
    ANNULE = "ANNULE"

    # The match is over.
    TERMINE = "TERMINE"



class MatchResponse(BaseModel):
    """
    This class is the DTO of match response.
    """

    # This is the match's id.
    id: int

    # This is the event of the match.
    event: EventMini

    # This is the match's court.
    court_number: int

    # This is the first team in the match.
    team1: TeamResponse

    # This is the second team in the match.
    team2: TeamResponse

    # This is the status of the match.
    status: MatchStatus

    # This is the score of the first team.
    score_team1: Optional[str] = None

    # This is the score of the second team.
    score_team2: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True
    )



class MatchRequest(BaseModel):
    """
    This class is the DTO of a match request.
    """

    # The court where the match is played.
    court_number: int

    # The match's status.
    status: MatchStatus

    # The first team id in the match.
    team1_id: int

    # The second team id in the match.
    team2_id: int

    # The score of first team in the match.
    score_team1: Optional[int] = None

    # The score of second team in the match.
    score_team2: Optional[int] = None

    model_config = ConfigDict(
        from_attributes=True
    )



class MatchesListResponse(BaseModel):
    """
    This class is the list of mtaches... Just because in the spec it has.
    """

    # This is the list of matches.
    matches: List[MatchResponse]

    # This is the total in the request.
    total: int

    model_config = ConfigDict(
        from_attributes=True
    )
