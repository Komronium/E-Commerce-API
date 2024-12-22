from pydantic import BaseModel, Field, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class SignupRequest(BaseModel):
    name: str | None = None
    email: EmailStr
    password: str = Field(..., min_length=8)


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str
