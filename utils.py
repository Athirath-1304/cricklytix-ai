# utils.py
"""
Utility functions for Cricklytix AI.
"""
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

def load_head_to_head_data(csv_path="data/head_to_head.csv"):
    """Load head-to-head data as a pandas DataFrame."""
    return pd.read_csv(csv_path)

def get_api_key(key_name="OPENAI_API_KEY", default=None):
    """Get API key from environment or .env file."""
    return os.getenv(key_name, default)
