from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.schemas.auth import Token, LoginRequest, SignupRequest
from app.schemas.user import UserOut
from app.api.deps import get_db_dependency
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
