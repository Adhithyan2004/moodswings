from fastapi import APIRouter, Query
from services.ai_service import mood_to_genres
from services.spotify_service import search_tracks_by_mood

router = APIRouter(prefix="/ai", tags=["AI"])


@router.get("/recommend")
def recommend(
    mood: str = Query(...),
    user_id: str = Query(...)
):
    genres = mood_to_genres(mood)
    return search_tracks_by_mood(", ".join(genres), user_id)

