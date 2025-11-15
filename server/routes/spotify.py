from fastapi import APIRouter, Query
from fastapi.responses import RedirectResponse
from core.auth import get_auth_url, exchange_code_for_token
from services.spotify_service import search_tracks_by_mood
from core.config import settings
import requests
from utils.token_storage import load_token

router = APIRouter(prefix="/spotify")


@router.get("/login")
def login():
    return {"auth_url": get_auth_url()}


@router.get("/callback")
def callback(code: str):
    data = exchange_code_for_token(code)

    if data.get("status") == "success":
        user_id = data.get("user_id")

        return RedirectResponse(
            url=f"{settings.FRONTEND_URL}/?user_id={user_id}"
        )

    return data

@router.get("/search")
def search_tracks(
    mood: str = Query(...),
    user_id: str = Query(...)
):
    return search_tracks_by_mood(mood, user_id)

@router.get("/me")
def get_user_profile(user_id: str = Query(...)):
    token_data = load_token(user_id)
    if not token_data:
        return {"error": "No Spotify token found"}

    headers = {"Authorization": f"Bearer {token_data['access_token']}"}
    res = requests.get("https://api.spotify.com/v1/me", headers=headers)

    if res.status_code != 200:
        return {
            "error": f"Failed to fetch profile ({res.status_code})",
            "details": res.json(),
        }

    data = res.json()
    return {
        "id": data.get("id"),
        "display_name": data.get("display_name"),
        "email": data.get("email"),
        "images": data.get("images", []),
    }
