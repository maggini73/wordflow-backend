import os
from fastapi import FastAPI, Query
import json
import random
from firebase_admin import credentials, auth
from fastapi import Depends
import firebase_admin
from sqlalchemy.orm import Session
from schemas import GameResultCreate
from database import SessionLocal, engine, Base
from models import Game


if not firebase_admin._apps:
    cred_json = os.environ.get("FIREBASE_SERVICE_ACCOUNT")
    if not cred_json:
        raise RuntimeError("Firebase service account not configured")

    cred = credentials.Certificate(json.loads(cred_json))
    firebase_admin.initialize_app(cred)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/phrase")
def get_random_phrase(
    language: str = Query(...),
  
    difficulty: str = Query(...)
):
    
    # carichiamo il json una sola volta
    with open("phrases_"+language+".json", "r", encoding="utf-8") as f:
        PHRASES = json.load(f)

    filtered = [
        p for p in PHRASES
        if p["language"] == language and p["difficulty"] == difficulty
    ]

    if not filtered:
        return {"error": "No phrases found"}

    return random.choice(filtered)

@app.post("/games")
def save_game_result(
    data: GameResultCreate,
    db: Session = Depends(get_db),
):
    # TEMPORANEO: user_id finto
    user_id = "DEBUG_USER"

    game = Game(
        user_id=user_id,
        phrase_id=data.phrase_id,
        language=data.language,
        difficulty=data.difficulty,
        won=data.won,
        lives_left=data.lives_left,
        duration_seconds=data.duration_seconds,
    )

    db.add(game)
    db.commit()
    db.refresh(game)

    return {
        "status": "ok",
        "game_id": game.id,
    }

