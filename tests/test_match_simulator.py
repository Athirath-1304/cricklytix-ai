import pytest
from match_simulator import simulate_match
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/..'))

def dummy_chat_completion_create(*args, **kwargs):
    raise Exception("API error")

def test_simulate_match_fallback(monkeypatch):
    monkeypatch.setattr("openai.ChatCompletion.create", dummy_chat_completion_create)
    summary = simulate_match(["A"], ["B"], "Venue", "Pitch", "Weather", openai_api_key="dummy")
    assert "Could not simulate match" in summary 