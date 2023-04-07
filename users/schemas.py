from pydantic import BaseModel, EmailStr, Field


class LoginUser(BaseModel):
    """
    Basic fields for login.
    """
    email: EmailStr = Field(...)
    password: str = Field(...)


class SignUpUser(LoginUser):
    """
    Add required fields for sign up.
    """
    name: str = Field(...)
    password_confirmation: str = Field(...)
