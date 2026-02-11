import os
from fastapi import FastAPI, HTTPException, Header, Query
import json
import random
from firebase_admin import credentials, auth
from fastapi import Depends
import firebase_admin
from sqlalchemy.orm import Session
from schemas import GameResultCreate
from database import SessionLocal, engine, Base
from models import Game
from typing import Optional

PHRASES = {}

if not firebase_admin._apps:
    cred_json = os.environ.get("FIREBASE_SERVICE_ACCOUNT")
    if not cred_json:
        raise RuntimeError("Firebase service account not configured")

    cred = credentials.Certificate(json.loads(cred_json))
    firebase_admin.initialize_app(cred)

def load_phrases():
    languages = ["it", "en"]  # aggiungi qui le lingue

    for lang in languages:
        filename = f"phrases_{lang}.json"
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                PHRASES[lang] = {p["id"]: p for p in data}

def get_current_user_id(authorization: Optional[str] = Header(None)):

    if authorization is None:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization format")

    token = authorization.split(" ")[1]

    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token["uid"]

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

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
    user_id: str = Depends(get_current_user_id),
):
    
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

@app.get("/games/mine")
def get_my_games(
    user_id: str = Depends(get_current_user_id()),
    db: Session = Depends(get_db),
):
    games = db.query(Game).filter(Game.user_id == user_id).order_by(Game.played_at.desc()).all()
    
    load_phrases()
    results = []

    for g in games:
        phrase = next((p for p in PHRASES if p["id"] == g.phrase_id), None)

        results.append({
            "id": g.id,
            "phrase_text": phrase["text"] if phrase else "N/A",
            "won": g.won,
            "duration_seconds": g.duration_seconds,
            "lives_left": g.lives_left,
            "played_at": g.played_at.isoformat()
        })

    return results
