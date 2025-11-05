from fastapi import APIRouter, Query
from core.auth import get_auth_url, exchange_code_for_token
from services.spotify_service import search_tracks_by_mood

router = APIRouter(prefix="/spotify")


@router.get("/login")
def login():
    return {"auth_url": get_auth_url()}


@router.get("/callback")
def callback(code: str = Query(...)):
    return exchange_code_for_token(code)


@router.get("/search")
def search_tracks(mood: str = Query(..., description="User mood like happy/sad")):
    return search_tracks_by_mood(mood)
