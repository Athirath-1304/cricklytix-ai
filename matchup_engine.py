# matchup_engine.py
"""
Module for generating player matchup analysis using GPT.
"""
import openai
import pandas as pd
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

ERROR_LOG = "output/error.log"

def log_error(msg):
    os.makedirs(os.path.dirname(ERROR_LOG), exist_ok=True)
    with open(ERROR_LOG, "a") as f:
        f.write(f"[{datetime.now()}] {msg}\n")

def classify_advice(advice):
    """Classify advice as 'good' (green) or 'avoid' (red) for UI coloring."""
    advice_lower = advice.lower()
    if any(word in advice_lower for word in ["avoid", "struggle", "not recommended", "weak", "poor"]):
        return "avoid"
    if any(word in advice_lower for word in ["pick", "strong", "good", "recommended", "favorable", "great"]):
        return "good"
    return "neutral"

def generate_matchup_advice(head_to_head_df, openai_api_key=None):
    """
    For each batsman/bowler pair, send a prompt to GPT and return advice.
    Returns a DataFrame with 'advice' and 'advice_type' columns.
    """
    if openai_api_key is None:
        openai_api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = openai_api_key

    advices = []
    advice_types = []
    for idx, row in head_to_head_df.iterrows():
        batsman = row['batsman']
        bowler = row['bowler']
        avg = row['avg']
        sr = row['sr']
        innings = row['innings']
        prompt = (
            f"{batsman} vs {bowler} – Avg: {avg}, SR: {sr}, Innings: {innings} "
            "– give 2-line fantasy advice for this matchup."
        )
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=60
            )
            advice = response.choices[0].message['content'].strip()
        except Exception as e:
            advice = "Could not generate advice. Please try again later."
            log_error(f"Matchup: {batsman} vs {bowler} | Error: {e}")
        advices.append(advice)
        advice_types.append(classify_advice(advice))
    head_to_head_df['advice'] = advices
    head_to_head_df['advice_type'] = advice_types
    return head_to_head_df
