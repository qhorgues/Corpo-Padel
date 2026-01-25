from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.deps import get_current_user, get_current_admin
from app.models.models import Pool
from app.schemas.pool import PoolRequest, PoolResponse, PoolsListResponse

router = APIRouter()


@router.get("", response_model=PoolsListResponse)
def list_pools(db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    """
    This function gets all the pools.

    param : db - The database.
    param : _ - The client.
    return : Return all the pools.
    """
    pools = db.query(Pool).all()
    return PoolsListResponse(pools=pools, total=len(pools))



@router.get("/{pool_id}", response_model=PoolResponse)
def get_pool(pool_id: int, db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    """
    This function gets a specific pool.

    param : pool_id - The pool's id.
    param : db - The session of database.
    param : _ - The client.
    return : Return the pool.
    """
    pool = db.query(Pool).get(pool_id)
    if not pool:
        raise HTTPException(status_code=404, detail="Pool not found")
    return PoolResponse.model_validate(pool)



@router.post("", response_model=PoolResponse, status_code=status.HTTP_201_CREATED)
def create_pool(data: PoolRequest, db: Session = Depends(get_db), _: str = Depends(get_current_admin)):
    """
    This function creates a pool.

    param : data - The pool's informations.
    param : db - The session of database.
    param : _ - The client.
    return : Return the pool created.
    """
    if len(data.team_ids) != 6:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A pool has 6 teams")

    pool = Pool(**data.model_dump())
    db.add(pool)
    db.commit()
    db.refresh(pool)
    return PoolResponse.model_validate(pool)



@router.put("/{pool_id}", response_model=PoolResponse)
def update_pool(pool_id: int, data: PoolRequest, db: Session = Depends(get_db), _: str = Depends(get_current_admin)):
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
    
    pool = db.query(Pool).get(pool_id)
    if not pool:
        raise HTTPException(status_code=404, detail="Pool not found")

    for key, value in data.model_dump().items():
        setattr(pool, key, value)

    db.commit()
    return PoolResponse.model_validate(pool)



@router.delete("/{pool_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pool(pool_id: int, db: Session = Depends(get_db), _: str = Depends(get_current_admin)):
    """
    This function remove a pool.

    param : pool_id - The pool's id.
    param : db - The session of database.
    param : _ - The client.
    return : Return no content
    """
    pool = db.query(Pool).get(pool_id)
    if not pool:
        raise HTTPException(status_code=404, detail="Pool not found")

    db.delete(pool)
    db.commit()
