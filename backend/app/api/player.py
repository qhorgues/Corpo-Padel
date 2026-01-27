# app/api/players.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import get_current_user, get_current_admin
from app.models.models import Player, User
from app.schemas.player import PlayerRequest, PlayerResponse, PlayersListResponse

router = APIRouter()


@router.get("", response_model=PlayersListResponse)
def list_players(db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    """
    This function gets all the players.

    param : db - The session of database.
    param : _ - The client.
    return : Return all the players.
    """
    players = db.query(Player).all()

    return PlayersListResponse(
        players=players,
        total=len(players),
    )



@router.get("/{player_id}", response_model=PlayerResponse)
def get_player(player_id: int, db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    """
    This function gets a specific player.

    param : player_id - The player's id.
    param : db - The session of database.
    param : _ - The client.
    return : Return the player.
    """
    player = db.get(Player, player_id)

    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player not found",
        )

    return PlayerResponse.model_validate(player)



@router.post("", response_model=PlayerResponse, status_code=status.HTTP_201_CREATED)
def create_player(data: PlayerRequest, db: Session = Depends(get_db), _: str = Depends(get_current_admin)):
    """
    This function creates a player.

    param : data - The player's informations.
    param : db - The session of database.
    param : _ - The client.
    return : Return the player created.
    """
    from app.core.security import get_password_hash #Dynamic import, because need to initialize .env
    
    try:
        user = db.query(User).filter(User.email == data.email).first()
        if user is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )

        user = User(email = data.email,
                    password_hash = get_password_hash(data.password),
                    role = data.role
                )
        db.add(user)
        player = Player(first_name = data.first_name,
                        last_name = data.last_name,
                        company = data.company,
                        license_number = data.license_number,
                        birth_date = data.birth_date,
                        photo_url = data.photo_url,
                        user = user
                    )
        db.add(player)
        db.commit()
    except:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid field")
    db.refresh(player)

    return PlayerResponse.model_validate(player)



@router.put("/{player_id}", response_model=PlayerResponse)
def update_player(player_id: int, data: PlayerRequest, db: Session = Depends(get_db),_: str = Depends(get_current_admin)):
    """
    This function updates a player.
    
    param : player_id - The player's id.
    param : data - The player's informations.
    param : db - The session of database.
    param : _ - The client.
    return : Return the player updated.
    """
    from app.core.security import get_password_hash #Dynamic import, because need to initialize .env

    player = db.get(Player, player_id)

    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player not found",
        )

    try:
        user = player.user
        user.email = data.email
        user.password_hash = get_password_hash(data.password)
        user.role = data.role
        
        player.first_name = data.first_name
        player.last_name = data.last_name
        player.company = data.company
        player.license_number = data.license_number
        player.birth_date = data.birth_date
        player.photo_url = data.photo_url

        db.commit()
    except:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid field")

    return PlayerResponse.model_validate(player)



@router.delete("/{player_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_player(player_id: int, db: Session = Depends(get_db), _: str = Depends(get_current_admin)):
    """
    This function remove a player.

    param : player_id - The player's id.
    param : db - The session of database.
    param : _ - The client.
    return : Return no content
    """
    player = db.get(Player, player_id)

    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player not found",
        )

    db.delete(player)
    db.commit()
