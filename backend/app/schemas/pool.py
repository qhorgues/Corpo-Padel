# app/schemas/pool.py
from typing import List
from pydantic import BaseModel, ConfigDict
from .team import TeamResponse


class PoolResponse(BaseModel):
    """
    This class is a DTO of the pool response.
    """

    # This is the pool's id.
    id: int

    # This is the pool's name.
    name: str

    # This is the number of teams in the pool.
    teams_count: int

    # This is the teams in the pool.
    teams: List[str]

    model_config = ConfigDict(
        from_attributes=True
    )



class PoolRequest(BaseModel):
    """
    This class is a DTO of the pool request.
    """

    # This is the pool's name.
    name: str

    # This is a list of teams's id.
    team_ids: List[int]

    model_config = ConfigDict(
        from_attributes=True
    )



class PoolsListResponse(BaseModel):
    """
    This class is the list of pools... Just because in the spec it has.
    """

    # This pools.
    pools: List[PoolResponse]

    # The number of pools.
    total : int

    model_config = ConfigDict(
        from_attributes=True
    )
