from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from datetime import datetime
from database import Base

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)

    phrase_id = Column(String, index=True)
    language = Column(String)
    difficulty = Column(String)

    won = Column(Boolean)
    lives_left = Column(Integer)
    duration_seconds = Column(Integer)

    played_at = Column(DateTime, default=datetime.utcnow)

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    alias: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())

