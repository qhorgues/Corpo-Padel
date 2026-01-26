from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from datetime import date
import re

from app.database import get_db
from app.api.deps import get_current_user, get_current_admin
from app.models.models import Event, Match, Team
from app.schemas.event import EventRequest, EventResponse, EventsListResponse

router = APIRouter()


@router.get("", response_model=EventsListResponse)
def list_events(db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    """
    This function gets all the events.

    param : db - The database.
    param : _ - The client.
    return : Return all the events.
    """
    events = db.query(Event).all()
    return EventsListResponse(events=events, total=len(events))



@router.get("/{event_id}", response_model=EventResponse)
def get_event(event_id: int, db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    """
    This function gets a specific event.

    param : event_id - The event's id.
    param : db - The session of database.
    param : _ - The client.
    return : Return the event.
    """
    event = db.query(Event).get(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return EventResponse.model_validate(event)



@router.post("", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(data: EventRequest, db: Session = Depends(get_db), _: str = Depends(get_current_admin)):
    """
    This function creates a event.

    param : data - The event's informations.
    param : db - The session of database.
    param : _ - The client.
    return : Return the event created.
    """
    if data.event_date < date.today():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Back to the future")
    
    if not re.match(r"^(?:[01]\d|2[0-3]):[0-5]\d$", data.event_time):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="event_time must be in HH:MM format (00:00–23:59)")

    if len(data.matches) < 1 or len(data.matches) > 3:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Matches need to be 1 to 3")
    
    pool_set = {}
    team_set = {}
    for match in data.matches:
        if match.court_number < 1 or match.court_number > 10:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Court need to be 1 to 10")
        
        if match.team1_id == match.team2_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="One teams in the match")
        
        if match.court_number in pool_set:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Two matchs in the same pool")
        pool_set.add(match.court_number)

        if match.team2_id in team_set or match.team1_id in team_set:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A team is playing twice in the same time")
        team_set.add(match.team1_id)
        team_set.add(match.team2_id)

    event = Event(
                event_date = data.event_date,
                event_time = data.event_time
            )

    db.add(event)

    for match in data.matches:
        team1 = db.query(Team).get(match.team1_id)
        team2 = db.query(Team).get(match.team2_id)

        if team1 is None or team2 is None:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="One team not found")

        db.add(Match(
                court_number=match.court_number,
                team1=team1,
                team2=team2,
                event=event
            )
        )

    db.commit()
    db.refresh(event)
    return EventResponse.model_validate(event)



@router.put("/{event_id}", response_model=EventResponse)
def update_event(event_id: int, data: EventRequest, db: Session = Depends(get_db), _: str = Depends(get_current_admin)):
    """
    This function updates a event.
    
    param : event_id - The event's id.
    param : data - The event's informations.
    param : db - The session of database.
    param : _ - The client.
    return : Return the event updated.
    """
    if data.event_date < date.today():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Back to the future")
    
    if not re.match(r"^(?:[01]\d|2[0-3]):[0-5]\d$", data.event_time):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="event_time must be in HH:MM format (00:00–23:59)")

    if len(data.matches) < 1 or len(data.matches) > 3:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Matches need to be 1 to 3")
    
    pool_set = {}
    team_set = {}
    for match in data.matches:
        if match.court_number < 1 or match.court_number > 10:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Court need to be 1 to 10")
        
        if match.team1_id == match.team2_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="One teams in the match")
        
        if match.court_number in pool_set:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Two matchs in the same pool")
        pool_set.add(match.court_number)

        if match.team2_id in team_set or match.team1_id in team_set:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A team is playing twice in the same time")
        team_set.add(match.team1_id)
        team_set.add(match.team2_id)
        
    event = db.query(Event).get(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    event.event_date = data.event_date
    event.event_time = data.event_time

    db.delete(event.matches)

    for match in data.matches:
        team1 = db.query(Team).get(match.team1_id)
        team2 = db.query(Team).get(match.team2_id)

        if team1 is None or team2 is None:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="One team not found")

        db.add(Match(
                court_number=match.court_number,
                team1=team1,
                team2=team2,
                event=event
            )
        )

    db.commit()
    return EventResponse.model_validate(event)



@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event_id: int, db: Session = Depends(get_db), _: str = Depends(get_current_admin)):
    """
    This function remove a event.

    param : event_id - The event's id.
    param : db - The session of database.
    param : _ - The client.
    return : Return no content
    """
    event = db.query(Event).get(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    for match in event.matches:
        if match.status != "A_VENIR":
            raise HTTPException(status_code=400, detail="Match over or cancel")

    db.delete(event)
    db.commit()
