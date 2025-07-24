import unittest
from unittest.mock import patch, MagicMock
import os
import pandas as pd
from matchup_engine import generate_matchup_advice
from match_simulator import simulate_match
from utils import get_api_key, load_head_to_head_data

class TestCricklytix(unittest.TestCase):
    @patch("openai.ChatCompletion.create")
    def test_generate_matchup_advice(self, mock_openai):
        # Mock OpenAI response
        mock_openai.return_value = MagicMock(
            choices=[MagicMock(message={"content": "Kohli struggles vs Rashid. Avoid him."})]
        )
        df = pd.DataFrame({
            "batsman": ["Virat Kohli"],
            "bowler": ["Rashid Khan"],
            "avg": [19.2],
            "sr": [81],
            "innings": [5]
        })
        result = generate_matchup_advice(df, openai_api_key="dummy")
        self.assertIn("advice", result.columns)
        self.assertTrue(isinstance(result["advice"].iloc[0], str) and len(result["advice"].iloc[0]) > 10)

    @patch("openai.ChatCompletion.create")
    def test_simulate_match(self, mock_openai):
        # Mock OpenAI response
        mock_openai.return_value = MagicMock(
            choices=[MagicMock(message={"content": "India scores 172/8. Australia falls short. India wins!\nStar performers: Kohli, Bumrah."})]
        )
        result = simulate_match(
            ["Rohit", "Gill", "Kohli"],
            ["Warner", "Smith", "Starc"],
            "Wankhede", "Flat", "Humid",
            openai_api_key="dummy"
        )
        self.assertIn("India", result)
        self.assertIn("Star performers", result)
        self.assertGreater(len(result), 30)

    def test_get_api_key(self):
        os.environ["OPENAI_API_KEY"] = "testkey123"
        self.assertEqual(get_api_key(), "testkey123")
        del os.environ["OPENAI_API_KEY"]
        self.assertIsNone(get_api_key())

    def test_load_head_to_head_data(self):
        # Should load the sample CSV
        df = load_head_to_head_data("data/head_to_head.csv")
        self.assertFalse(df.empty)
        self.assertIn("batsman", df.columns)

    @patch("openai.ChatCompletion.create")
    def test_integration_end_to_end(self, mock_openai):
        # Mock both GPT calls
        mock_openai.side_effect = [
            MagicMock(choices=[MagicMock(message={"content": "Advice: Pick Kohli."})]),
            MagicMock(choices=[MagicMock(message={"content": "Match summary: India wins. Kohli stars."})])
        ]
        # 1. Versus Engine
        df = pd.DataFrame({
            "batsman": ["Virat Kohli"],
            "bowler": ["Rashid Khan"],
            "avg": [19.2],
            "sr": [81],
            "innings": [5]
        })
        advice_df = generate_matchup_advice(df, openai_api_key="dummy")
        self.assertTrue(len(advice_df["advice"].iloc[0]) > 10)
        # 2. Match Simulation
        summary = simulate_match(
            ["Rohit", "Gill", "Kohli"],
            ["Warner", "Smith", "Starc"],
            "Wankhede", "Flat", "Humid",
            openai_api_key="dummy"
        )
        self.assertGreater(len(summary), 20)

    def tearDown(self):
        # Clean up any environment variables or files if needed
        pass

if __name__ == "__main__":
    unittest.main() 