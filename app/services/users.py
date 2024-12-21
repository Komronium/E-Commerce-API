from pydantic import UUID4
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserService:

    @staticmethod
    def _get_user_or_404(db: Session, user_id: UUID4) -> User:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'User with ID {user_id} not found',
            )
        return user


    @staticmethod
    async def get_all_users(db: Session, page: int, limit: int, search: str = ''):
        query = db.query(User).filter(User.email.contains(search))
        return query.limit(limit).offset((page - 1) * limit).all()

    @staticmethod
    async def get_user(db: Session, user_id: UUID4):
        return UserService._get_user_or_404(db, user_id)

    @staticmethod
    async def create_user(db: Session, user: UserCreate):
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already exists')
        hashed_password = hash_password(user.password)
        user.password = hashed_password
        db_user = User(**user.model_dump())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    async def update_user(db: Session, user_id: UUID4, user: UserUpdate):
        db_user = UserService._get_user_or_404(db, user_id)

        for key, value in user.model_dump().items():
            if value is not None:
                setattr(db_user, key, value)

        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    async def delete_user(db: Session, user_id: UUID4):
        db_user = UserService._get_user_or_404(db, user_id)
        db.delete(db_user)
        db.commit()
