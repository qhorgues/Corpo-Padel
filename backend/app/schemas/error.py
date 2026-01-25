# app/schemas/error.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class ErrorResponse(BaseModel):
    """
    This class represent basic error information.
    """

    # This is the detail of the error.
    detail: str



class LoginErrorResponse(BaseModel):
    """
    This class represent an error in login.
    """
    
    # This is the detail of the error.
    detail: str

    # This is the number of remaining try.
    attempts_remaining: int



class AccountLockedResponse(BaseModel):
    """
    This class represent a login with a blocked account.
    """
    
    # This is the detail of the error.
    detail: str

    # When the account is unlocked
    locked_until: datetime

    # The number of minute remaining.
    minutes_remaining: int
