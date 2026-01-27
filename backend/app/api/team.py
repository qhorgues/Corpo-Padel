from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.deps import get_current_user, get_current_admin
from app.models.models import Team
from app.schemas.team import TeamRequest, TeamResponse, TeamsListResponse

router = APIRouter()


@router.get("", response_model=TeamsListResponse)
def list_teams(pool_id: int | None = Query(None), company: str | None = Query(None), db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    """
    This function gets all the teams.

    param : pool_id - The team's pool id.
    param : company - The team's company name.
    param : db - The database.
    param : _ - The client.
    return : Return all the teams.
    """
    teams = db.query(Team)

    if pool_id is not None:
        teams = teams.filter(Team.pool_id == pool_id)

    if company is not None:
        teams = teams.filter(Team.company == company)

    teams = teams.all()

    return TeamsListResponse(teams=teams, total=len(teams))



@router.get("/{team_id}", response_model=TeamResponse)
def get_team(team_id: int, db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    """
    This function gets a specific teams.

    param : team_id - The team's id.
    param : db - The database.
    param : _ - The client.
    return : Return the team.
    """
    team = db.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return TeamResponse.model_validate(team)



@router.post("", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
def create_team(data: TeamRequest, db: Session = Depends(get_db), _: str = Depends(get_current_admin)):
    """
    This function creates a teams.

    param : data - The team's informations.
    param : db - The database.
    param : _ - The client.
    return : Return the team created.
    """
    team = Team(**data.model_dump())
    db.add(team)
    db.commit()
    db.refresh(team)
    return TeamResponse.model_validate(team)



@router.put("/{team_id}", response_model=TeamResponse)
def update_team(team_id: int, data: TeamRequest, db: Session = Depends(get_db), _: str = Depends(get_current_admin)):
    """
    This function updates a teams.

    param : team_id - The team's id.
    param : data - The team's informations.
    param : db - The database.
    param : _ - The client.
    return : Return the team updated.
    """
    team = db.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    for key, value in data.model_dump().items():
        setattr(team, key, value)

    db.commit()
    return TeamResponse.model_validate(team)



@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_team(team_id: int, db: Session = Depends(get_db), _: str = Depends(get_current_admin)):
    """
    This function remove a team.

    param : team_id - The team's id.
    param : db - The session of database.
    param : _ - The client.
    return : Return no content
    """
    team = db.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    db.delete(team)
    db.commit()
