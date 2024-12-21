from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.schemas.user import UserOut, UserUpdate
from app.api.deps import get_db_dependency, get_current_user
from app.services.users import UserService

router = APIRouter(tags=['Profile'], prefix='/api/v1/profile')


@router.get('/', response_model=UserOut)
def get_profile(user = Depends(get_current_user)):
    return user


@router.put('/', response_model=UserOut)
async def update_profile(data: UserUpdate,
                   db: Session = Depends(get_db_dependency),
                   user = Depends(get_current_user)):
    return await UserService.update_user(db, user.id, data)


@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(db: Session = Depends(get_db_dependency),
                   user = Depends(get_current_user)):
    return await UserService.delete_user(db, user.id)
