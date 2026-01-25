# app/schemas/team.py
from typing import List
from pydantic import BaseModel, ConfigDict


class TeamPlayerMini(BaseModel):
    """
    This class is a soft DTO to show the player in the team.
    """

    # This is the player's id.
    id: int

    # This is the player's first name.
    first_name: str

    # This is the player's last name.
    last_name: str

    model_config = ConfigDict(
        from_attributes=True
    )



class PoolMini(BaseModel):
    """
    This class is a soft DTO to show the pool in the team.
    """

    # This is the pool's id.
    id: int

    # This is the pool's name.
    name: str

    model_config = ConfigDict(
        from_attributes=True
    )



class TeamResponse(BaseModel):
    """
    This class is the DTO of a team response.
    """

    # This is the team's id.
    id: int

    # This is the team's company name.
    company: str

    # This is the team's players.
    players: List[TeamPlayerMini]

    # This is the team's pool.
    pool: PoolMini

    model_config = ConfigDict(
        from_attributes=True
    )



class TeamRequest(BaseModel):
    """
    This class is the DTO of a team request.
    """

    # This is the team's company's name.
    company: str

    # This is the team's first player id.
    player1_id: int

    # This is the team's second player id.
    player2_id: int


    # This is the team's pool id.
    pool_id: int

    model_config = ConfigDict(
        from_attributes=True
    )



class TeamsListResponse(BaseModel):
    """
    This class is the list of teams... Just because in the spec it has.
    """

    # This is the list of teams.
    teams: List[TeamResponse]

    # This is the total of teams in the request.
    total: int

    model_config = ConfigDict(
        from_attributes=True
    )
