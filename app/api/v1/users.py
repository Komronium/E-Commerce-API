from pydantic import UUID4
from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.schemas.user import UserOut, UserCreate, UserUpdate
from app.api.deps import get_db_dependency, get_admin_user
from app.services.users import UserService

router = APIRouter(
    tags=['Users'],
    prefix='/api/v1/users',
    dependencies=[Depends(get_admin_user)]
)


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[UserOut])
async def get_all_users(
    db: Session = Depends(get_db_dependency),
    page: int = Query(default=1, ge=1, description='page'),
    limit: int = Query(default=20, ge=1, le=100, description='limit'),
    search: str | None = Query(default=None, max_length=128, description='search')
):
    return await UserService.get_all_users(db, page, limit, search)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db_dependency)
):
    return await UserService.create_user(db, user)


@router.get('/{user_id}', status_code=status.HTTP_200_OK, response_model=UserOut)
async def get_user(
    user_id: UUID4,
    db: Session = Depends(get_db_dependency)
):
    return await UserService.get_user(db, user_id)


@router.put('/{user_id}', status_code=status.HTTP_200_OK, response_model=UserOut)
async def update_user(
    user_id: UUID4,
    user: UserUpdate,
    db: Session = Depends(get_db_dependency)
):
    return await UserService.update_user(db, user_id, user)


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID4,
    db: Session = Depends(get_db_dependency)
):
    await UserService.delete_user(db, user_id)
    return {'detail': 'User deleted successfully'}
