from datetime import timedelta
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import EmailStr
from app.core.security import hash_password, verify_password, create_access_token
from app.core.config import settings
from app.models.user import User
from app.api.deps import get_current_user
from app.schemas.auth import LoginRequest, SignupRequest, ChangePasswordRequest


class AuthService:

    @staticmethod
    def authenticate(db: Session, email: EmailStr, password: str):
        user = db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.password):
            return None
        return user

    @staticmethod
    def login(db: Session, login_request: LoginRequest):
        user = AuthService.authenticate(db, login_request.email, login_request.password)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')

        access_token = create_access_token(
            data={'sub': user.email},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return {'access_token': access_token, 'token_type': 'bearer'}

    @staticmethod
    def signup(db: Session, signup_request: SignupRequest):
        existing_user = db.query(User).filter(User.email == signup_request.email).first()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already exists')

        hashed_password = hash_password(signup_request.password)
        user = User(email=signup_request.email, password=hashed_password, name=signup_request.name)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def change_password(db: Session, request: ChangePasswordRequest, current_user: User = Depends(get_current_user)):
        if not verify_password(request.old_password, current_user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Old password is incorrect',
            )

        new_hashed_password = hash_password(request.new_password)
        current_user.password = new_hashed_password
        db.add(current_user)
        db.commit()
        return {'message': 'Password updated successfully'}
