# match_simulator.py
"""
Full T20 match simulation using GPT (openai v1+ client).
"""
import os
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

ERROR_LOG = "output/error.log"
SIM_LOG = "output/simulations.log"


def log_error(msg):
    os.makedirs(os.path.dirname(ERROR_LOG), exist_ok=True)
    with open(ERROR_LOG, "a") as f:
        f.write(f"[{datetime.now()}] {msg}\n")


def log_simulation(input_data, summary):
    os.makedirs(os.path.dirname(SIM_LOG), exist_ok=True)
    with open(SIM_LOG, "a") as f:
        f.write(f"[{datetime.now()}] INPUT: {input_data}\nSUMMARY: {summary}\n---\n")


def simulate_match(
    team1_xi: list,
    team2_xi: list,
    venue: str,
    pitch: str,
    weather: str,
    openai_api_key: str = None,
    team1_context: str = None,
    team2_context: str = None,
) -> str:
    """
    Simulate a T20 match with GPT-4o. Returns a detailed match summary string.
    team1_context / team2_context are optional player stat strings that improve
    the quality of the simulation when provided by the caller.
    Uses openai v1+ client syntax.
    """
    if openai_api_key is None:
        openai_api_key = os.getenv("OPENAI_API_KEY")

    client = OpenAI(api_key=openai_api_key)

    t1_block = team1_context or ', '.join(team1_xi)
    t2_block = team2_context or ', '.join(team2_xi)

    prompt = f"""Simulate a T20 cricket match between these two teams.

Team 1:
{t1_block}

Team 2:
{t2_block}

Venue: {venue}
Pitch: {pitch}
Weather: {weather}

Write a detailed, realistic match summary covering:
- Toss result and decision
- Total runs and wickets for each innings
- Top 2-3 batting and bowling performers with stats
- Key turning points (big over, wicket cluster, etc.)
- Final result with margin (runs or wickets)
- 2-line fantasy advice: which players to target next game

Use real cricket knowledge about each player's strengths and the venue's characteristics.
Format it as a proper match report — readable and specific."""

    input_data = {
        "team1_xi": team1_xi,
        "team2_xi": team2_xi,
        "venue": venue,
        "pitch": pitch,
        "weather": weather,
    }

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=700,
        )
        summary = response.choices[0].message.content.strip()
    except Exception as e:
        summary = "Could not simulate match. Please check your API key and try again."
        log_error(f"Simulation error | Input: {input_data} | {e}")

    log_simulation(input_data, summary)
    return summary
