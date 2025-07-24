# match_simulator.py
"""
Module for simulating a full cricket match using GPT.
"""
import openai
import os
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

def simulate_match(team1_xi, team2_xi, venue, pitch, weather, openai_api_key=None):
    """
    Simulate a match using GPT and return a summary.
    team1_xi, team2_xi: list of player names
    venue, pitch, weather: strings
    Returns: string summary
    """
    if openai_api_key is None:
        openai_api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = openai_api_key

    prompt = f"""
Simulate a T20 cricket match between these teams:

Team 1: {', '.join(team1_xi)}
Team 2: {', '.join(team2_xi)}
Venue: {venue}
Pitch: {pitch}
Weather: {weather}

Give a detailed, readable summary including:
- Total runs, wickets for each team
- Star performers (bat, bowl)
- Turning points
- Final result
- 2-line fantasy advice
"""
    input_data = {
        "team1_xi": team1_xi,
        "team2_xi": team2_xi,
        "venue": venue,
        "pitch": pitch,
        "weather": weather
    }
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=600
        )
        summary = response.choices[0].message['content'].strip()
    except Exception as e:
        summary = "Could not simulate match. Please try again later."
        log_error(f"Simulation Error | Input: {input_data} | Error: {e}")
    log_simulation(input_data, summary)
    return summary
