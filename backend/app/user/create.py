from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import User, LoginAttempt
from app.schemas.auth import LoginRequest, TokenResponse, UserCreationRequest, UserResponse, ChangePasswordRequest
from app.core.security import verify_password, get_password_hash, create_access_token
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/create")
def create(
    request: UserCreationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user.role == "ADMINISTRATEUR":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Vous devez être un administateur pour créer un compte"
        )
    
    new_user = db.query(User).filter(User.email == "admin@padel.com").first()
    if not new_user:
        new_user = User(
            email=request.email,
            password_hash=get_password_hash(request.password),
            role=request.role,
            is_active=request.is_active
        )
        db.add(new_user)
        db.commit()
        return {"message": "L'utilisateur a bien été créé"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Le compte existe déjà"
        )