import requests
from services.ai_service import mood_to_genres
from core.auth import refresh_spotify_token 


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


def search_tracks_by_mood(mood: str, user_id: str):
    # Step 1: Get genres from AI
    genres = mood_to_genres(mood)

    # Step 2: Ensure valid Spotify token
    token_data = refresh_spotify_token(user_id)
    if not token_data:
        return {
            "error": "Spotify session expired or missing. Please log in again."
        }

    headers = {"Authorization": f"Bearer {token_data['access_token']}"}

    # Step 3: Build search query using top 2 genres
    query = " ".join([f"genre:{g}" for g in genres[:2]])
    url = f"https://api.spotify.com/v1/search?q={query}&type=track&limit=20"

    res = requests.get(url, headers=headers)

    # Step 4: Handle token expiration / invalidation
    if res.status_code == 401:
        # Spotify says token invalid → refresh manually once
        print(" Spotify token expired, refreshing...")
        token_data = refresh_spotify_token(user_id)
        if not token_data:
            return {"error": "Spotify token expired. Please log in again."}

        headers = {"Authorization": f"Bearer {token_data['access_token']}"}
        res = requests.get(url, headers=headers)

    if res.status_code != 200:
        return {
            "error": f"Spotify API failed ({res.status_code})",
            "details": res.json(),
        }

    #  Step 5: Parse track results
    data = res.json()
    tracks = [
        {
            "name": t["name"],
            "artist": t["artists"][0]["name"],
            "url": t["external_urls"]["spotify"],
            "preview_url": t.get("preview_url"),
            "image": t["album"]["images"][0]["url"]
            if t["album"]["images"]
            else None,
        }
        for t in data["tracks"]["items"]
    ]

    # Step 6: Deduplicate before returning
    tracks = dedupe_tracks(tracks)

    return {
        "mood": mood,
        "genres_used": genres,
        "tracks": tracks,
    }
