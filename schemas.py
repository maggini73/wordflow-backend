from pydantic import BaseModel

class GameResultCreate(BaseModel):
    phrase_id: str
    language: str
    difficulty: str
    won: bool
    lives_left: int
    duration_seconds: int
