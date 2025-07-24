import os
import pandas as pd
import pytest
from utils import load_head_to_head_data, get_api_key

def test_load_head_to_head_data():
    df = load_head_to_head_data("data/head_to_head.csv")
    assert not df.empty
    assert set(["batsman", "bowler", "avg", "sr", "innings"]).issubset(df.columns)

def test_get_api_key(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "testkey123")
    assert get_api_key() == "testkey123" 