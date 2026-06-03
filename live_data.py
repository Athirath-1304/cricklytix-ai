# live_data.py
"""
Live and recent cricket match data via CricAPI (https://cricapi.com).
Requires CRICAPI_KEY in .env — free tier gives 100 requests/day.
Falls back gracefully when no key is present.
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

CRICAPI_BASE = "https://api.cricapi.com/v1"
TIMEOUT = 8


def get_live_matches(api_key: str = None) -> tuple:
    """
    Fetch currently live or recent matches.
    Returns (list_of_matches, error_string).
    On success error_string is None; on failure list is None.
    """
    if api_key is None:
        api_key = os.getenv("CRICAPI_KEY")

    if not api_key:
        return None, (
            "Add CRICAPI_KEY to your .env for live scores. "
            "Free tier at cricapi.com (100 req/day)."
        )

    try:
        resp = requests.get(
            f"{CRICAPI_BASE}/currentMatches",
            params={"apikey": api_key, "offset": 0},
            timeout=TIMEOUT,
        )
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as e:
        return None, f"Network error fetching live data: {e}"

    if data.get("status") != "success":
        return None, f"CricAPI error: {data.get('reason', 'Unknown')}"

    matches = data.get("data", [])
    return matches if matches else ([], None)


def get_upcoming_matches(api_key: str = None) -> tuple:
    """Fetch upcoming scheduled matches."""
    if api_key is None:
        api_key = os.getenv("CRICAPI_KEY")

    if not api_key:
        return None, "No CRICAPI_KEY found."

    try:
        resp = requests.get(
            f"{CRICAPI_BASE}/matches",
            params={"apikey": api_key, "offset": 0},
            timeout=TIMEOUT,
        )
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as e:
        return None, f"Network error: {e}"

    if data.get("status") != "success":
        return None, f"CricAPI error: {data.get('reason', 'Unknown')}"

    return data.get("data", []), None


def format_score(match: dict) -> str:
    """Return a compact one-line score string for a match dict."""
    scores = match.get("score", [])
    if not scores:
        return match.get("status", "No score available")
    parts = [
        f"{s.get('inning', '?')}: {s.get('r', '?')}/{s.get('w', '?')} "
        f"({s.get('o', '?')} ov)"
        for s in scores
    ]
    return " | ".join(parts)
