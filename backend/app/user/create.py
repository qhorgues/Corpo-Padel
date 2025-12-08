from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.database import get_db
from app.models.models import User
from app.schemas.auth import UserCreationRequest, TokenResponse
from app.core.security import get_password_hash
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/create-user", response_model=TokenResponse)
def create_user(
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
                last_name=request.last_name,
                first_name=request.first_name,
                company=request.company,
                license_number=request.license_number,
                birth_date=request.birth_date,
                photo_url=request.photo_url,
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