# app/api/players.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import get_current_user, get_current_admin
from app.models.models import Player, User
from app.schemas.player import PlayerRequest, PlayerResponse, PlayersListResponse
from app.schemas.error import ErrorResponse

router = APIRouter()


@router.get("", response_model=PlayersListResponse, responses={403: {"model": ErrorResponse}},)
def list_players(db: Session = Depends(get_db), _: str = Depends(get_current_admin),):
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


@router.get("/{player_id}", response_model=PlayerResponse, responses={404: {"model": ErrorResponse}},)
def get_player(player_id: int, db: Session = Depends(get_db), _: str = Depends(get_current_user),):
    """
    This function gets a specific player.

    param : player_id - The player's id.
    param : db - The session of database.
    param : _ - The client.
    return : Return the player.
    """
    player = db.query(Player).get(player_id)

    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Joueur introuvable",
        )

    return PlayerResponse.model_validate(player)



@router.post("", response_model=PlayerResponse, status_code=status.HTTP_201_CREATED,)
def create_player(data: PlayerRequest, db: Session = Depends(get_db), _: str = Depends(get_current_admin),):
    """
    This function creates a player.

    param : data - The player's informations.
    param : db - The session of database.
    param : _ - The client.
    return : Return the player created.
    """
    user = User(email = data.email,
                pasword_hash = data.password,
                role = data.role
            )
    db.add(user)
    db.refresh(user)
    player = Player(first_name = data.first_name,
                    last_name = data.last_name,
                    company = data.company,
                    license = data.license_number,
                    birth_date = data.birth_date,
                    photo_url = data.photo_url,
                    user = user
                )
    db.add(player)
    db.commit()
    db.refresh(player)

    return PlayerResponse.model_validate(player)



@router.put("/{player_id}", response_model=PlayerResponse,)
def update_player(player_id: int, data: PlayerRequest, db: Session = Depends(get_db),_: str = Depends(get_current_admin),):
    """
    This function updates a player.
    
    param : player_id - The player's id.
    param : data - The player's informations.
    param : db - The session of database.
    param : _ - The client.
    return : Return the player updated.
    """
    player = db.query(Player).get(player_id)

    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Joueur introuvable",
        )

    for k, v in data.model_dump().items():
        setattr(player, k, v)

    db.commit()
    return PlayerResponse.model_validate(player)



@router.delete("/{player_id}", status_code=204,)
def delete_player(player_id: int, db: Session = Depends(get_db), _: str = Depends(get_current_admin),):
    """
    This function gets a specific player.

    param : player_id - The player's id.
    param : db - The session of database.
    param : _ - The client.
    return : Return no content
    """
    player = db.query(Player).get(player_id)

    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Joueur introuvable",
        )

    db.delete(player)
    db.commit()

    return
