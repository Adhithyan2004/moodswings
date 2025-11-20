from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from core.auth import get_auth_url, exchange_code_for_token
from services.spotify_service import search_tracks_by_mood
from core.config import settings
from utils.token_storage import load_token
import requests
import traceback

router = APIRouter(prefix="/spotify")


@router.get("/login")
def login():
    """Return Spotify auth URL."""
    try:
        return {"auth_url": get_auth_url()}
    except Exception as e:
        print(" /login error:", traceback.format_exc())
        raise HTTPException(status_code=500, detail="Failed to generate Spotify auth URL.")


@router.get("/callback")
def callback(code: str):
    """Spotify OAuth redirect handler."""
    try:
        data = exchange_code_for_token(code)

        if data.get("status") == "success":
            user_id = data.get("user_id")
            print(f"✅ Spotify auth success for user: {user_id}")
            return RedirectResponse(url=f"{settings.FRONTEND_URL}/?user_id={user_id}")

        print("❌ Spotify Auth Error:", data)
        return RedirectResponse(url=f"{settings.FRONTEND_URL}/?error=spotify_auth_failed")

    except Exception:
        print("🔥 Callback crashed:", traceback.format_exc())
        return RedirectResponse(url=f"{settings.FRONTEND_URL}/?error=server_crash")


@router.get("/search")
def search_tracks(mood: str = Query(...), user_id: str = Query(...)):
    """Search Spotify tracks by mood."""
    try:
        return search_tracks_by_mood(mood, user_id)
    except Exception:
        print("⚠️ /search error:", traceback.format_exc())
        raise HTTPException(status_code=500, detail="Failed to search tracks.")


@router.get("/me")
def get_user_profile(user_id: str = Query(...)):
    """Fetch Spotify user profile from stored token."""
    try:
        token_data = load_token(user_id)
        if not token_data:
            print(f"⚠️ No token found for user {user_id}")
            return JSONResponse(status_code=404, content={"error": "No Spotify token found"})

        headers = {"Authorization": f"Bearer {token_data['access_token']}"}
        res = requests.get("https://api.spotify.com/v1/me", headers=headers)

        if res.status_code == 401:
            print(f"⚠️ Token expired for user {user_id}")
            return JSONResponse(status_code=401, content={"error": "Spotify token expired"})

        if res.status_code != 200:
            print(f"⚠️ Spotify profile fetch failed: {res.status_code} - {res.text}")
            return JSONResponse(
                status_code=res.status_code,
                content={"error": "Failed to fetch profile", "details": res.text}
            )

        data = res.json()
        print(f"✅ Profile fetched for {user_id}")
        return {
            "id": data.get("id"),
            "display_name": data.get("display_name"),
            "email": data.get("email"),
            "images": data.get("images", []),
        }

    except Exception:
        print("🔥 /me route crashed:", traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal server error")
