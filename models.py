from sqlalchemy import Column, Integer, String, Boolean, DateTime
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
