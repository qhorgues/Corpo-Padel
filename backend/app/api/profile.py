from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.deps import get_current_user
from app.models.models import User, Player
from app.schemas.profile import ProfilePhoto, ProfileResponse, ProfilePlayer, ProfileUser, ProfilePlayerRequest

router = APIRouter()


@router.get("/me", response_model=ProfileResponse)
def get_profile(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    This function gets the current user's profile.

    param : db - The session of database.
    param : current_user - The connected user.
    return : Return the profile.
    """
    player = db.query(Player).filter(Player.user_id == current_user.id).first()

    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player not found",
        )

    return ProfileResponse(
        user=ProfileUser.model_validate(current_user),
        player=ProfilePlayer.model_validate(player)
    )



@router.put("/me", response_model=ProfileResponse)
def update_profile(data: ProfilePlayerRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    This function updates the current user's profile.

    param : data - The player's informations.
    param : db - The session of database.
    param : current_user - The connected user.
    return : Return the profile updated.
    """
    player = db.query(Player).filter(Player.user_id == current_user.id).first()

    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player not found",
        )

    player.first_name = data.first_name
    player.last_name = data.last_name
    player.company = data.company
    player.license_number = data.license_number
    player.birth_date = data.birth_date
    player.photo_url = data.photo_url
    if data.email is not None:
        player.user.email = data.email

    db.commit()
    db.refresh(player)

    return ProfileResponse(
        user=ProfileUser.model_validate(current_user),
        player=ProfilePlayer.model_validate(player)
    )



@router.put("/me/photo", status_code=status.HTTP_201_CREATED)
def upload_profile_photo(data: ProfilePhoto, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    This function stores the profile photo URI.

    param : uri - The URI of the photo.
    param : db - The session of database.
    param : current_user - The connected user.
    return : Return the stored photo URI.
    """
    player = db.query(Player).filter(Player.user_id == current_user.id).first()

    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player not found",
        )

    player.photo_url = data.photo_url
    db.commit()
    db.refresh(player)

    return {"photo_url": player.photo_url}



@router.delete("/me/photo", status_code=status.HTTP_204_NO_CONTENT)
def delete_profile_photo(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    This function deletes the profile photo URI.

    param : db - The session of database.
    param : current_user - The connected user.
    return : Return no content.
    """
    player = db.query(Player).filter(Player.user_id == current_user.id).first()

    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player not found",
        )

    player.photo_url = None
    db.commit()

    return
