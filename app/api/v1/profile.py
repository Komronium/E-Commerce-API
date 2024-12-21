from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.schemas.user import UserOut, UserUpdate
from app.api.deps import get_db_dependency, get_current_user
from app.services.users import UserService

router = APIRouter(tags=['Profile'], prefix='/api/v1/profile')


@router.get('/', response_model=UserOut, status_code=status.HTTP_200_OK)
async def get_profile(
        current_user: UserOut = Depends(get_current_user)
):
    return current_user


@router.put('/', response_model=UserOut, status_code=status.HTTP_200_OK)
async def update_profile(
    update_request: UserUpdate,
    db: Session = Depends(get_db_dependency),
    current_user = Depends(get_current_user)
):
    return await UserService.update_user(db, current_user.id, update_request)


@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(
    db: Session = Depends(get_db_dependency),
    current_user = Depends(get_current_user)
):
    await UserService.delete_user(db, current_user.id)
