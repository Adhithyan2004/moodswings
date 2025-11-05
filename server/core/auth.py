import requests
from urllib.parse import quote
from core.config import settings
from utils.token_storage import save_token

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
    Exchange Spotify's authorization code for an access token
    and save it to Redis.
    """
    user_id = "adhi_test_user"

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

    if "access_token" in data:
        # Save to Redis with TTL
        save_token(user_id, data)
        return {
            "status": "success",
            "message": "Spotify authorization successful.",
            "data": {
                "expires_in": data.get("expires_in"),
                "scope": data.get("scope"),
            },
        }

    # If we didn’t get a token, return error info
    return {"status": "error", "details": data}
