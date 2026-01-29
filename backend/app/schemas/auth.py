# ============================================
# FICHIER : backend/app/schemas/auth.py
# ============================================

from pydantic import BaseModel, EmailStr, Field, field_validator,  ConfigDict
from datetime import datetime
import re

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: int
    email: str
    role: str
    must_change_password: bool

    model_config = ConfigDict(
        from_attributes=True
    )

class UserCreationRequest(BaseModel):
    last_name: str
    first_name: str
    company: str
    license_number: str
    birth_date: datetime
    photo_url: str
    email: str
    password: str
    role: str
    is_active: bool

class UserDeletionRequest(BaseModel):
    email: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(...)
    confirm_password: str

    @field_validator("new_password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 12:
            raise ValueError('Le mot de passe doit contenir au moins 12 caractères')
        if len(v) > 60:
            raise ValueError('Le mot de passe doit contenir au plus 60 caractères')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Le mot de passe doit contenir au moins une majuscule')
        if not re.search(r'[a-z]', v):
            raise ValueError('Le mot de passe doit contenir au moins une minuscule')
        if not re.search(r'\d', v):
            raise ValueError('Le mot de passe doit contenir au moins un chiffre')
        if not re.search(r'[!@#$%^&*(),;.?":{}|<>]', v):
            raise ValueError('Le mot de passe doit contenir au moins un caractère spécial')
        if re.search(r'[ ]', v):
            raise ValueError('Le mot de passe ne doit pas contenir des espaces')
        return v
    
    @field_validator('confirm_password')
    @classmethod
    def passwords_match(cls, v, values):
        if 'new_password' in values.data and v != values.data['new_password']:
            raise ValueError('Les mots de passe ne correspondent pas')
        return v
