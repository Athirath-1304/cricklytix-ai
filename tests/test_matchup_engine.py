import pandas as pd
import pytest
from matchup_engine import generate_matchup_advice, classify_advice

class DummyOpenAI:
    class ChatCompletion:
        @staticmethod
        def create(*args, **kwargs):
            class Resp:
                choices = [type("obj", (), {"message": {"content": "Kohli struggles vs Rashid. Avoid picking him today."}})]
            return Resp()

def test_generate_matchup_advice(monkeypatch):
    df = pd.DataFrame({
        "batsman": ["Virat Kohli"],
        "bowler": ["Rashid Khan"],
        "avg": [19.2],
        "sr": [81],
        "innings": [5]
    })
    monkeypatch.setattr("openai.ChatCompletion", DummyOpenAI.ChatCompletion)
    result = generate_matchup_advice(df, openai_api_key="dummy")
    assert "advice" in result.columns
    assert "avoid" in result["advice_type"].iloc[0]

def test_classify_advice():
    assert classify_advice("Avoid picking him") == "avoid"
    assert classify_advice("Good pick") == "good"
    assert classify_advice("Consider") == "neutral" 