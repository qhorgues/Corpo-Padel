# app/schemas/profile.py
from datetime import date
from typing import Optional
from pydantic import EmailStr
from pydantic import BaseModel, ConfigDict
from .player import UserRole


class ProfileUser(BaseModel):
    """
    This class show the profile of a user.
    """

    # The user's id.
    id: int

    # The user's mail.
    email: EmailStr

    # The user's role.
    role: UserRole

    model_config = ConfigDict(
        from_attributes=True
    )



class ProfilePlayer(BaseModel):
    """
    This class show the profile of a player.
    """

    # The player's id.
    id: int

    # The player's first name.
    first_name: str


    # The player's last name.
    last_name: str


    # The player's company name.
    company: str


    # The player's license.
    license_number: str


    # The player's birth date.
    birth_date: Optional[date]


    # The player's profile picture.
    photo_url: Optional[str]

    model_config = ConfigDict(
        from_attributes=True
    )



class ProfileResponse(BaseModel):
    """
    This class is a DTO of profile response.
    """
    
    # The user profile.
    user: ProfileUser

    # The player profile.
    player: ProfilePlayer

    model_config = ConfigDict(
        from_attributes=True
    )
