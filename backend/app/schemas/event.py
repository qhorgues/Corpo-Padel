# app/schemas/event.py
from datetime import date, time
from typing import List
from pydantic import BaseModel, ConfigDict
from .match import MatchResponse, MatchRequest, MatchStatus

class MatchMini(BaseModel):
    """
    This class is a soft DTO of match response.
    """

    # This is the match's id.
    id: int

    # This is the match's court.
    court_number: int

    # This is the first team in the match.
    team1_id: int

    # This is the second team in the match.
    team2_id: int

    # This is the status of the match.
    status: MatchStatus

    model_config = ConfigDict(
        from_attributes=True
    )


class EventResponse(BaseModel):
    """
    This class is a DTO for a event response.
    """

    # The event's id.
    id: int

    # The event's date.
    event_date: date

    # The event's time.
    event_time: time

    # The matches in the event.
    matches: List[MatchMini]

    model_config = ConfigDict(
        from_attributes=True
    )



class EventRequest(BaseModel):
    """
    This class is a DTO for a event request.
    """

    # The event's date.
    event_date: date

    # The event's time.
    event_time: time

    # The event's matches.
    matches: List[MatchRequest]

    model_config = ConfigDict(
        from_attributes=True
    )



class EventsListResponse(BaseModel):
    """
    This class is the list of mtaches... Just because in the spec it has.
    """

    # This is the events.
    events: List[EventResponse]

    # This is the total of events in the request.
    total: int

    model_config = ConfigDict(
        from_attributes=True
    )
