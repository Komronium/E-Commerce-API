from pydantic import BaseModel, UUID4, EmailStr


class UserBase(BaseModel):
    name: str | None = None
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    email: EmailStr | None = None


class UserOut(UserBase):
    id: UUID4
    is_active: bool
    is_admin: bool

    class Config:
        from_attributes = True
