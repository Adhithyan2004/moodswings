from fastapi import FastAPI
from routes import spotify, ai
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)


app.include_router(spotify.router, prefix="", tags=["Spotify"])
app.include_router(ai.router, prefix="", tags=["AI"])


@app.get("/")
def home():
    return "What ra sudeep too much scene putting ur"
