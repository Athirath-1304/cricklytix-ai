# matchup_engine.py
"""
Player matchup analysis using GPT (openai v1+ client).
"""
import os
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

ERROR_LOG = "output/error.log"


def log_error(msg):
    os.makedirs(os.path.dirname(ERROR_LOG), exist_ok=True)
    with open(ERROR_LOG, "a") as f:
        f.write(f"[{datetime.now()}] {msg}\n")


def classify_advice(advice: str) -> str:
    """Return 'good', 'avoid', or 'neutral' for UI colour-coding."""
    lower = advice.lower()
    if any(w in lower for w in ["avoid", "struggle", "not recommended", "weak", "poor", "difficult"]):
        return "avoid"
    if any(w in lower for w in ["pick", "strong", "good", "recommended", "favorable", "great", "excellent"]):
        return "good"
    return "neutral"


def generate_matchup_advice(head_to_head_df: pd.DataFrame, openai_api_key: str = None) -> pd.DataFrame:
    """
    For each batsman/bowler row, call GPT-4o and append 'advice' + 'advice_type' columns.
    Uses openai v1+ client syntax.
    """
    if openai_api_key is None:
        openai_api_key = os.getenv("OPENAI_API_KEY")

    client = OpenAI(api_key=openai_api_key)

    advices, advice_types = [], []

    for _, row in head_to_head_df.iterrows():
        batsman = row["batsman"]
        bowler = row["bowler"]
        avg = row["avg"]
        sr = row["sr"]
        innings = row["innings"]

        prompt = (
            f"{batsman} vs {bowler} — T20 H2H: Avg {avg}, SR {sr}, Innings {innings}. "
            "Give 2-line fantasy cricket advice: should I pick this batsman against this bowler? "
            "Be direct — say pick or avoid."
        )

        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=80,
            )
            advice = response.choices[0].message.content.strip()
        except Exception as e:
            advice = "Could not generate advice. Please check your API key."
            log_error(f"Matchup {batsman} vs {bowler}: {e}")

        advices.append(advice)
        advice_types.append(classify_advice(advice))

    head_to_head_df = head_to_head_df.copy()
    head_to_head_df["advice"] = advices
    head_to_head_df["advice_type"] = advice_types
    return head_to_head_df
