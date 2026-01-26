from pydantic import BaseModel, ConfigDict

class ResetPasswordResponse(BaseModel):
    """
    This class is a DTO when the admin change a password.
    """
    message: str
    temporary_password: str
    warning: str

    model_config = ConfigDict(
        from_attributes=True
    )
