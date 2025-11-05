from fastapi import FastAPI
from routes import spotify, ai

app = FastAPI()

app.include_router(spotify.router, prefix="", tags=["Spotify"])
app.include_router(ai.router, prefix="", tags=["AI"])


@app.get("/")
def home():
    return "What ra too much scene putting ah"
