from datetime import timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from pydantic import EmailStr
from app.core.security import hash_password, verify_password, create_access_token
from app.core.config import settings
from app.models.user import User
from app.schemas.auth import LoginRequest, SignupRequest


class AuthService:

    @staticmethod
    def authenticate(db: Session, email: EmailStr, password: str):
        user = db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.password):
            return None
        return user

    @staticmethod
    def login(db: Session, data: LoginRequest):
        user = AuthService.authenticate(db, data.email, data.password)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')

        access_token = create_access_token(
            data={'sub': user.email},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return {'access_token': access_token, 'token_type': 'bearer'}

    @staticmethod
    def signup(db: Session, data: SignupRequest):
        existing_user = db.query(User).filter(User.email == data.email).first()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already exists')

        hashed_password = hash_password(data.password)
        user = User(email=data.email, password=hashed_password, name=data.name)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
