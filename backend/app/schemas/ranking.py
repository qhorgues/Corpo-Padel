from typing import List
from pydantic import BaseModel, ConfigDict


class RankingItemResponse(BaseModel):
    position: int
    company: str
    matches_played: int
    wins: int
    losses: int
    points: int
    sets_won: int
    sets_lost: int

    model_config = ConfigDict(
        from_attributes=True
    )


class RankingsResponse(BaseModel):
    rankings: List[RankingItemResponse]

    model_config = ConfigDict(
        from_attributes=True
    )
