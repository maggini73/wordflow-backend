from fastapi import FastAPI, Query
import json
import random

app = FastAPI()

# carichiamo il json una sola volta
with open("phrases.json", "r", encoding="utf-8") as f:
    PHRASES = json.load(f)


@app.get("/phrase")
def get_random_phrase(
    language: str = Query(...),
  
    difficulty: str = Query(...)
):
    filtered = [
        p for p in PHRASES
        if p["language"] == language and p["difficulty"] == difficulty
    ]

    if not filtered:
        return {"error": "No phrases found"}

    return random.choice(filtered)
