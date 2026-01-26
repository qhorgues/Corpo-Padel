from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import User
from app.api.deps import get_current_admin
from app.schemas.admin import ResetPasswordResponse
from app.core.security import get_password_hash
import secrets
import string

router = APIRouter()


def generate_temp_password() -> str:
    """Generate a random temporary password."""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()"
    return "".join(secrets.choice(alphabet) for _ in range(16))


@router.post("/accounts/{user_id}/reset-password", response_model=ResetPasswordResponse)
def reset_password(
    user_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(get_current_admin),
):
    """
    This function resets a user's password.

    param : user_id - The user's id.
    param : db - The session of database.
    param : _ - The client (admin).
    return : Return temporary password.
    """

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    temp_password = generate_temp_password()
    user.password_hash = get_password_hash(temp_password)
    db.commit()

    return ResetPasswordResponse(
        message="Mot de passe réinitialisé",
        temporary_password=temp_password,
        warning="Ce mot de passe ne sera affiché qu'une seule fois"
    )
