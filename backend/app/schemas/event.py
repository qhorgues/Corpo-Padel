# app/schemas/event.py
from datetime import date, time
from typing import List
from pydantic import ModelBase, ConfigDict
from .match import MatchResponse, MatchRequest


class EventResponse(ModelBase):
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
    matches: List[MatchResponse]

    model_config = ConfigDict(
        from_attributes=True
    )



class EventRequest(ModelBase):
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



class EventsListResponse(ModelBase):
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
