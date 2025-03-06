from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func  # pylint: disable=no-member

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())  # pylint: disable=not-callable
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  # pylint: disable=not-callable
