# app/schemas/player.py
from enum import Enum
from datetime import date
from typing import Optional, List
from pydantic import BaseModel, EmailStr, ConfigDict

class UserRole(str, Enum):
    """
    This class is the enumeration of the role.
    """

    # The user is an admin.
    ADMINISTRATEUR = "ADMINITRATEUR"

    # The user is a player.
    JOUEUR = "JOUEUR"

    

class PlayerResponse(BaseModel):
    """
    This class is the DTO of a player response.
    """

    # This is the player's id.
    id: int

    # This is the player's first name.
    first_name: str

    # This is the player's last name.
    last_name: str

    # This is the player's company name.
    company: str

    # This is the player's license.
    license_number: str

    # This is the player's birth date.
    birth_date: Optional[date] = None

    # This is the player's profile picture.
    photo_url: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True
    )



class PlayerRequest(BaseModel):
    """
    This class is the DTO of a player request.
    """

    # This is the player's first name.
    first_name: str

    # This is the player's last name.
    last_name: str

    # This is the player's company name.
    company: str

    # This is the player's license.
    license_number: str

    # This is the player's mail.
    email: EmailStr

    # This is the player's password.
    password: str

    model_config = ConfigDict(
        from_attributes=True
    )



class PlayersListResponse(BaseModel):
    """
    This class is the list of players... Just because in the spec it has.
    """

    # This is the list of players.
    players: List[PlayerResponse]

    # This is the total in the request.
    total: int

    model_config = ConfigDict(
        from_attributes=True
    )
