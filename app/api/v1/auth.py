from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.auth import Token, LoginRequest, SignupRequest
from app.schemas.user import UserOut
from app.api.deps import get_db_dependency
from app.services.auth import AuthService

router = APIRouter(tags=['Auth'], prefix='/api/v1')


@router.post('/login', response_model=Token)
def login(data: LoginRequest, db: Session = Depends(get_db_dependency)):
    return AuthService.login(db, data)


@router.post('/signup', response_model=UserOut)
def signup(data: SignupRequest, db: Session = Depends(get_db_dependency)):
    return AuthService.signup(db, data)
