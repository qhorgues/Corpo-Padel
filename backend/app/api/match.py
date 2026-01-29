from datetime import date, time, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.deps import get_current_user, get_current_admin
from app.models.models import Event, Match, Player, Team
from app.schemas.match import MatchRequest, MatchResponse, MatchStatus, MatchesListResponse

router = APIRouter()


@router.get("", response_model=MatchesListResponse)
def list_matches(upcoming : bool | None = Query(None), team_id : int | None = Query(None), status : MatchStatus | None = Query(None), my_matches : bool | None = Query(None), db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    """
    This function gets all the matchs.

    param : upcoming - Filter to the following 30 days.
    param : team_id - Filter to a team.
    param : status - Filter to a status.
    param : my_matches - Filter if the user plays the match.
    param : db - The database.
    param : user - The client.
    return : Return all the matchs.
    """
    matches = db.query(Match)

    if upcoming:
        today = date.today()
        matches = matches.join(Event).filter(
            Event.event_date.between(today, today + timedelta(days=30))
        )

    if status:
        matches = matches.filter(Match.status == status)

    if my_matches:
        player = db.query(Player).filter(Player.user_id == user.id).first()

        matches = matches.join(
            Team,
            or_(
                Team.id == Match.team1_id,
                Team.id == Match.team2_id,
            )
        ).filter(
            or_(
                Team.player1_id == player.id,
                Team.player2_id == player.id,
            )
        )

    matches = matches.all()
    return MatchesListResponse(matches=matches, total=len(matches))



@router.get("/{match_id}", response_model=MatchResponse)
def get_match(match_id: int, db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    """
    This function gets a specific match.

    param : match_id - The match's id.
    param : db - The session of database.
    param : _ - The client.
    return : Return the match.
    """
    match = db.get(Match, match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return MatchResponse.model_validate(match)



@router.post("", response_model=MatchResponse, status_code=status.HTTP_201_CREATED)
def create_match(data: MatchRequest, db: Session = Depends(get_db), _: str = Depends(get_current_admin)):
    """
    This function creates a match.

    param : data - The match's informations.
    param : db - The session of database.
    param : _ - The client.
    return : Return the match created.
    """
    if data.team1_id == data.team2_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A team cannot fight itself")
    
    if data.court_number < 1 or data.court_number > 10:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Court need to be 1 to 10")
    try:
        team1 = db.get(Team, data.team1_id)
        team2 = db.get(Team, data.team2_id)

        if team1 is None or team2 is None:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Team not found")
        
        event = Event(event_date=func.current_date(), event_time=time())
        db.add(event)

        match = Match(
            court_number=data.court_number,
            status=data.status,
            score_team1=data.score_team1,
            score_team2=data.score_team2,
            team1=team1,
            team2=team2,
            event=event
        )
        db.add(match)
        db.commit()
        db.refresh(match)
    except:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error in the field")
    return MatchResponse.model_validate(match)



@router.put("/{match_id}", response_model=MatchResponse)
def update_match(match_id: int, data: MatchRequest, db: Session = Depends(get_db), _: str = Depends(get_current_admin)):
    """
    This function updates a match.
    
    param : match_id - The match's id.
    param : data - The match's informations.
    param : db - The session of database.
    param : _ - The client.
    return : Return the match updated.
    """
    if data.team1_id == data.team2_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A team cannot fight itself")
    
    if data.court_number < 1 or data.court_number > 10:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Court need to be 1 to 10")
    
    match = db.get(Match, match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
        
    try:

        team1 = db.get(Team, data.team1_id)
        team2 = db.get(Team, data.team2_id)

        if team1 is None or team2 is None:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Team not found")

        match.court_number=data.court_number
        match.status=data.status
        match.score_team1=data.score_team1
        match.score_team2=data.score_team2
        match.team1=team1
        match.team2=team2

        db.commit()
    except:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error in the field")
    return MatchResponse.model_validate(match)



@router.delete("/{match_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_match(match_id: int, db: Session = Depends(get_db), _: str = Depends(get_current_admin)):
    """
    This function remove a match.

    param : match_id - The match's id.
    param : db - The session of database.
    param : _ - The client.
    return : Return no content
    """
    match = db.get(Match, match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    if match.status != "A_VENIR":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The match is over or canceled.")

    db.delete(match)
    db.commit()
