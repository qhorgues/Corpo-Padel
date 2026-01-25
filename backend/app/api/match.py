from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.deps import get_current_user, get_current_admin
from app.models.models import Match
from app.schemas.match import MatchRequest, MatchResponse, MatchesListResponse

router = APIRouter()


@router.get("", response_model=MatchesListResponse)
def list_matches(db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    """
    This function gets all the matchs.

    param : db - The database.
    param : _ - The client.
    return : Return all the matchs.
    """
    matches = db.query(Match).all()
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
    match = db.query(Match).get(match_id)
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

    match = Match(**data.model_dump())
    db.add(match)
    db.commit()
    db.refresh(match)
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
    
    match = db.query(Match).get(match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    for key, value in data.model_dump().items():
        setattr(match, key, value)

    db.commit()
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
    match = db.query(Match).get(match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    db.delete(match)
    db.commit()
