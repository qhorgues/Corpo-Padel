# app/schemas/result.py
from datetime import date
from typing import List
from pydantic import BaseModel, ConfigDict


class OpponentsResponse(BaseModel):
    """
    This class is a soft resume of the opponent.
    """

    # The company's name of the opponent.
    company: str

    # The players in the opponent team.
    players: List[str]

    model_config = ConfigDict(
        from_attributes=True
    )



class ResultItemResponse(BaseModel):
    """
    This class is the result of a specific match.
    """

    # The match's id.
    match_id: int

    # The match's date.
    date: date

    # The opponent.
    opponents: OpponentsResponse

    # The score.
    score: str

    # The result.
    result: str

    # The court.
    court_number: int

    model_config = ConfigDict(
        from_attributes=True
    )



class StatisticsResponse(BaseModel):
    """
    This is a soft information in statistic of a player.
    """
    
    # The number of matches.
    total_matches: int

    # The number of wins.
    wins: int

    # The number of looses.
    losses: int

    # The win rate.
    win_rate: float

    model_config = ConfigDict(
        from_attributes=True
    )



class MyResultsResponse(BaseModel):
    """
    This is the DTO of the response.
    """

    # The results.
    results: List[ResultItemResponse]

    # The statistic.
    statistics: StatisticsResponse

    model_config = ConfigDict(
        from_attributes=True
    )
