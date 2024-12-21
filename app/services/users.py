from pydantic import UUID4
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserService:

    @staticmethod
    async def get_all_users(db: Session, page: int, limit: int, search: str = ''):
        query = db.query(User).filter(User.email.contains(search))
        return query.limit(limit).offset((page - 1) * limit).all()

    @staticmethod
    async def get_user(db: Session, user_id: UUID4):
       user = db.query(User).filter(User.id == user_id).first()
       if not user:
           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
       return user

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
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

        for key, value in user.model_dump().items():
            setattr(db_user, key, value or getattr(db_user, key))

        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    async def delete_user(db: Session, user_id: UUID4):
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

        db.delete(db_user)
        db.commit()
