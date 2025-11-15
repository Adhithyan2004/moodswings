# utils/token_storage.py
import json,redis
from core.config import settings

# Connect to local Redis (you can swap with Render credentials later)
r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True
)
 
def save_token(user_id: str, data: dict): 
    """Save Spotify token to Redis with 1-hour expiry."""
    r.setex(f"spotify:token:{user_id}", 3600, json.dumps(data))

def load_token(user_id: str):
    """Load token if available."""
    val = r.get(f"spotify:token:{user_id}")
    return json.loads(val) if val else None
