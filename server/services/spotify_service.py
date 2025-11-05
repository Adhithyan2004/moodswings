import requests
from utils.token_storage import load_token
from services.ai_service import mood_to_genres


def dedupe_tracks(tracks):
    """Remove duplicate tracks by (name, artist) pair."""
    seen = set()
    unique = []
    for t in tracks:
        key = (t["name"].lower(), t["artist"].lower())
        if key not in seen:
            seen.add(key)
            unique.append(t)
    return unique


def search_tracks_by_mood(mood: str):
    user_id = "adhi_test_user"
    genres = mood_to_genres(mood)
    token_data = load_token(user_id)

    if not token_data:
        return {"error": "No Spotify token found. Please log in first."}

    headers = {"Authorization": f"Bearer {token_data['access_token']}"}

    # Use only first 2 genres for tighter results
    query = " ".join([f"genre:{g}" for g in genres[:2]])
    url = f"https://api.spotify.com/v1/search?q={query}&type=track&limit=20"

    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        return {
            "error": f"Spotify API failed ({res.status_code})",
            "details": res.json(),
        }

    data = res.json()
    tracks = [
        {
            "name": t["name"],
            "artist": t["artists"][0]["name"],
            "url": t["external_urls"]["spotify"],
        }
        for t in data["tracks"]["items"]
    ]

    # Deduplicate before returning
    tracks = dedupe_tracks(tracks)

    return {
        "mood": mood,
        "genres_used": genres,
        "tracks": tracks,
    }
