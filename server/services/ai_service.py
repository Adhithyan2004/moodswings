import re
import ast
import google.generativeai as genai
from core.config import settings

# Initialize Gemini client
genai.configure(api_key=settings.GEMINI_API_KEY)

# In-memory cache for mood-to-genre results
mood_cache = {}

# Default fallback genres
FALLBACK_GENRES = {
    "sad": ["acoustic", "indie", "lofi"],
    "happy": ["pop", "dance", "electronic"],
    "chill": ["chill", "ambient", "r&b"],
    "angry": ["metal", "punk", "rock"],
    "romantic": ["r&b", "soul", "jazz"],
    "default": ["rock", "pop"],
}


def mood_to_genres(mood: str):
    """
    Uses Gemini to translate a mood/phrase into Spotify-friendly genres.
    Includes caching and fallback behavior.
    """
    mood_key = mood.strip().lower()

    # Return from cache if available
    if mood_key in mood_cache:
        print(f"Cache hit for mood: {mood_key}")
        return mood_cache[mood_key]

    # Step 2: Ask Gemini
    try:
        prompt = f"""
        You are a music mood mapper. Convert this mood into 1-3 Spotify-friendly genres.
        Input mood: "{mood}"
        Respond only as a Python list of lowercase genre names like ["pop", "indie", "chill"].
        Do NOT include any explanation, text, or markdown formatting.
        """

        model = genai.GenerativeModel("gemini-2.5-pro")
        response = model.generate_content(prompt)

        text = response.text.strip()
        print("Gemini raw output:", text)

        # Strip Markdown-style code blocks
        text = re.sub(r"^```[a-zA-Z]*\n?|```$", "", text).strip()

        try:
            genres = ast.literal_eval(text)
        except Exception:
            genres = None

        # Sanity check
        if not isinstance(genres, list) or not all(isinstance(g, str) for g in genres):
            genres = None

    except Exception as e:
        print("AI Error:", e)
        genres = None

    # Step 3: Fallback handling
    if not genres:
        # pick fallback based on keywords
        genres = next(
            (v for k, v in FALLBACK_GENRES.items() if k in mood_key),
            FALLBACK_GENRES["default"],
        )
        print(f"Using fallback for mood '{mood_key}': {genres}")

    #  Step 4: Cache result
    mood_cache[mood_key] = genres
    return genres
