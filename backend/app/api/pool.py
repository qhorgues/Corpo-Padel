from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.deps import get_current_user, get_current_admin
from app.models.models import Match, Pool, Team, User
from app.schemas.pool import PoolRequest, PoolResponse, PoolsListResponse

router = APIRouter()


@router.get("", response_model=PoolsListResponse)
def list_pools(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    """
    This function gets all the pools.

    param : db - The database.
    param : _ - The client.
    return : Return all the pools.
    """
    pools = db.query(Pool).all()
    pools_response = [
        PoolResponse(
            id=pool.id,
            name=pool.name,
            teams_count=len(pool.teams),
            teams=[team.company for team in pool.teams]
        )
        for pool in pools
    ]
    return PoolsListResponse(pools=pools_response, total=len(pools))



@router.get("/{pool_id}", response_model=PoolResponse)
def get_pool(pool_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    """
    This function gets a specific pool.

    param : pool_id - The pool's id.
    param : db - The session of database.
    param : _ - The client.
    return : Return the pool.
    """
    pool = db.get(Pool, pool_id)
    if not pool:
        raise HTTPException(status_code=404, detail="Pool not found")
    return PoolResponse.model_validate(pool)



@router.post("", response_model=PoolResponse, status_code=status.HTTP_201_CREATED)
def create_pool(data: PoolRequest, db: Session = Depends(get_db), _: User = Depends(get_current_admin)):
    """
    This function creates a pool.

    param : data - The pool's informations.
    param : db - The session of database.
    param : _ - The client.
    return : Return the pool created.
    """
    if len(data.team_ids) != 6:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A pool has 6 teams")

    pool = Pool(name=data.name)
    db.add(pool)

    for team_id in data.team_ids:
        team = db.get(Team, team_id)
        if team is None:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
        team.pool = pool

    db.commit()
    db.refresh(pool)
    return PoolResponse(
        id=pool.id,
        name=pool.name,
        teams_count=len(pool.teams),
        teams=[team.company for team in pool.teams]
    )



@router.put("/{pool_id}", response_model=PoolResponse)
def update_pool(pool_id: int, data: PoolRequest, db: Session = Depends(get_db), _: User = Depends(get_current_admin)):
    """
    This function updates a pool.
    
    param : pool_id - The pool's id.
    param : data - The pool's informations.
    param : db - The session of database.
    param : _ - The client.
    return : Return the pool updated.
    """
    if len(data.team_ids) != 6:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A pool has 6 teams")
    
    pool = db.get(Pool, pool_id)
    if not pool:
        raise HTTPException(status_code=404, detail="Pool not found")
    
    for team in pool.teams:
        result = db.query(Match).filter(Match.status == "TERMINE").first()
        if result is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A team had already played")
    
    pool = Pool(name=data.name)

    for team_id in pool.teams:
        team = db.get(Team, team_id)
        team.pool = None

    for team_id in data.team_ids:
        team = db.get(Team, team_id)
        if team is None:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
        team.pool = pool

    db.commit()
    return PoolResponse(
        id=pool.id,
        name=pool.name,
        teams_count=len(pool.teams),
        teams=[team.company for team in pool.teams]
    )



@router.delete("/{pool_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pool(pool_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_admin)):
    """
    This function remove a pool.

    param : pool_id - The pool's id.
    param : db - The session of database.
    param : _ - The client.
    return : Return no content
    """
    pool = db.get(Pool, pool_id)
    if not pool:
        raise HTTPException(status_code=404, detail="Pool not found")
    
    for team in pool.teams:
        result = db.query(Match).filter(Match.status == "TERMINE").first()
        if result is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A team had already played")

    db.delete(pool)
    db.commit()
