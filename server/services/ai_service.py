import re
import ast
import google.generativeai as genai
from core.config import settings
from constants.spotify_geners import VALID_SPOTIFY_GENRES

genai.configure(api_key=settings.GEMINI_API_KEY)

mood_cache = {}

FALLBACK_GENRES = {
    "sad": ["acoustic", "indie", "lofi"],
    "happy": ["pop", "dance", "electronic"],
    "chill": ["chill", "ambient", "soul"],
    "angry": ["metal", "punk", "rock"],
    "romantic": ["r-n-b", "soul", "jazz"],
    "default": ["pop", "rock"],
}


def clean_genres(genres):
    """Keep only recognized Spotify genres."""
    cleaned = []
    for g in genres:
        g = g.strip().lower()

        # exact match
        if g in VALID_SPOTIFY_GENRES:
            cleaned.append(g)
            continue

        # fuzzy: replace space with hyphen
        g2 = g.replace(" ", "-")
        if g2 in VALID_SPOTIFY_GENRES:
            cleaned.append(g2)

    return cleaned


def mood_to_genres(mood: str):
    mood_key = mood.strip().lower()

    # Cache
    if mood_key in mood_cache:
        return mood_cache[mood_key]

    # Ask Gemini
    try:
        prompt = f"""
        You are a Spotify genre mapper. Convert the user's mood into 1-3
        *valid Spotify genres* that exist in the Spotify catalog.

        Input mood: "{mood}"

        Respond ONLY as a Python list, lowercase, like:
        ["pop", "dance", "chill"].
        No markdown, no explanation.
        """

        model = genai.GenerativeModel("gemini-2.5-pro")
        response = model.generate_content(prompt)

        text = response.text.strip()
        text = re.sub(r"^```[a-zA-Z]*\n?|```$", "", text).strip()

        try:
            genres = ast.literal_eval(text)
        except Exception:
            genres = None

        if not isinstance(genres, list):
            genres = None

    except Exception:
        genres = None

    # If Gemini broke, fallback
    if not genres:
        genres = next(
            (v for k, v in FALLBACK_GENRES.items() if k in mood_key),
            FALLBACK_GENRES["default"],
        )

    # Clean and validate
    genres = clean_genres(genres)

    # If cleaning removed everything → Fallback again
    if not genres:
        genres = next(
            (v for k, v in FALLBACK_GENRES.items() if k in mood_key),
            FALLBACK_GENRES["default"],
        )

    mood_cache[mood_key] = genres
    return genres
