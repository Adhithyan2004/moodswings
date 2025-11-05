import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
    SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
    GEMINI_API_KEY = os.getenv("OPENAI_API_KEY")
    REDIS_PORT = os.getenv("REDIS_PORT")
    REDIS_HOST = os.getenv("REDIS_HOST")


settings = Settings()
