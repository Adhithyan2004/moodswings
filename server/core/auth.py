import requests
import time
from urllib.parse import quote
from core.config import settings
from utils.token_storage import save_token, load_token


def get_auth_url():
    """Generate Spotify authorization URL."""
    scopes = (
        "playlist-modify-public "
        "user-read-private "
        "user-top-read "
        "user-library-read "
        "user-read-email "
        "user-library-modify"
    )
    redirect_uri = quote(settings.SPOTIFY_REDIRECT_URI, safe="")

    return (
        f"https://accounts.spotify.com/authorize?"
        f"client_id={settings.SPOTIFY_CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri={redirect_uri}"
        f"&scope={scopes}"
    )


def exchange_code_for_token(code: str):
    """
    Exchange Spotify authorization code for access + refresh token,
    fetch user profile, and save both in Redis.
    """
    # Step 1: Exchange code for tokens
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": settings.SPOTIFY_REDIRECT_URI,
            "client_id": settings.SPOTIFY_CLIENT_ID,
            "client_secret": settings.SPOTIFY_CLIENT_SECRET,
        },
    )

    data = response.json()

    if "access_token" not in data:
        return {"status": "error", "details": data}

    access_token = data["access_token"]

    # Step 2: Fetch Spotify user profile
    profile_res = requests.get(
        "https://api.spotify.com/v1/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    profile = profile_res.json()

    if "id" not in profile:
        return {"status": "error", "details": profile}

    user_id = profile["id"]

    # Step 3: Add expiry timestamp and ensure refresh_token exists
    expires_in = data.get("expires_in", 3600)
    data["expires_at"] = time.time() + expires_in

    # Some refresh responses might not include refresh_token; preserve old one
    existing = load_token(user_id)
    if existing and "refresh_token" in existing and "refresh_token" not in data:
        data["refresh_token"] = existing["refresh_token"]

    # Step 4: Save tokens in Redis
    save_token(user_id, data)

    # Step 5: Return data to frontend
    return {
        "status": "success",
        "user_id": user_id,
        "message": "Spotify authorization successful.",
        "data": {
            "expires_in": expires_in,
            "scope": data.get("scope"),
        },
    }


def refresh_spotify_token(user_id: str):
    """
    Refresh Spotify access token if expired.
    Uses refresh_token stored in Redis.
    """
    token_data = load_token(user_id)
    if not token_data:
        return None

    # Still valid
    if time.time() < token_data.get("expires_at", 0):
        return token_data

    refresh_token = token_data.get("refresh_token")
    if not refresh_token:
        print(f"⚠️ No refresh token available for user {user_id}")
        return None

    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": settings.SPOTIFY_CLIENT_ID,
            "client_secret": settings.SPOTIFY_CLIENT_SECRET,
        },
    )

    data = response.json()

    if "access_token" not in data:
        print(f"⚠️ Failed to refresh token for {user_id}: {data}")
        return None

    # Merge new access_token + expiry
    token_data["access_token"] = data["access_token"]
    token_data["expires_in"] = data.get("expires_in", 3600)
    token_data["expires_at"] = time.time() + token_data["expires_in"]

    # Keep the refresh token if Spotify didn't send a new one
    if "refresh_token" in data:
        token_data["refresh_token"] = data["refresh_token"]

    save_token(user_id, token_data)
    print(f"✅ Token refreshed for user {user_id}")
    return token_data
