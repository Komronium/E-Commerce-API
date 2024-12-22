from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.auth import Token, LoginRequest, SignupRequest, ChangePasswordRequest
from app.schemas.user import UserOut
from app.api.deps import get_db_dependency, get_current_user
from app.services.auth import AuthService

router = APIRouter(tags=['Auth'], prefix='/api/v1')


@router.post('/login', response_model=Token, status_code=status.HTTP_200_OK)
def login(
    login_request: LoginRequest,
    db: Session = Depends(get_db_dependency)
):
    return AuthService.login(db, login_request)


@router.post('/signup', response_model=UserOut, status_code=status.HTTP_200_OK)
def signup(
    signup_request: SignupRequest,
    db: Session = Depends(get_db_dependency)
):
    return AuthService.signup(db, signup_request)


@router.post('/change-password', status_code=status.HTTP_200_OK)
def change_password(
    request: ChangePasswordRequest,
    db: Session = Depends(get_db_dependency),
    current_user: User = Depends(get_current_user)
):
    return AuthService.change_password(db, request, current_user)
