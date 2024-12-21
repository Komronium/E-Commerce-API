import uuid
from sqlalchemy import Column, UUID, String, Boolean
from app.db.base import Base


class User(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(String(length=128), nullable=True)
    email = Column(String(length=128), unique=True, nullable=False, index=True)
    password = Column(String(length=32), nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
