from pydantic import BaseModel

class GameResultCreate(BaseModel):
    phrase_id: str
    language: str
    difficulty: str
    won: bool
    lives_left: int
    duration_seconds: int

class UserCreate(BaseModel):
    alias: str

class UserResponse(BaseModel):
    id: str
    alias: str
