# Cricklytix AI

> **AI-powered Fantasy Cricket Analysis & Match Simulation**

Cricklytix AI is a portfolio-grade project that combines advanced data engineering with generative AI to help fantasy cricket players make smarter decisions. It features a Versus Engine for player-vs-player matchup analysis and a Match Simulation Engine for AI-generated match outcomes, all powered by GPT-4o and presented in a modern Streamlit dashboard.

---

## 🚀 Features

- **Versus Engine:**
  - Analyzes batsman vs bowler head-to-head data
  - Uses GPT-4o to generate concise, actionable fantasy advice for each matchup
- **Match Simulation Engine:**
  - Simulates full cricket matches based on team XIs, venue, pitch, and weather
  - Returns detailed, readable summaries with runs, wickets, star performers, and fantasy tips
- **Streamlit Dashboard:**
  - Intuitive UI for running analyses and simulations
  - Color-coded, user-friendly results
- **Data Engineering:**
  - Loads and processes structured CSV data
  - Saves outputs and logs for reproducibility
- **Robust Logging & Error Handling:**
  - Logs errors to `output/error.log`
  - User-friendly fallback messages
- **Unit Tests:**
  - Ensures reliability of core functions

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **Streamlit** (dashboard UI)
- **OpenAI GPT-4o** (AI analysis & simulation)
- **Pandas** (data processing)
- **dotenv** (API key management)

---

## 📦 Project Structure

```
cricklytix_ai/
├── app.py                # Streamlit dashboard UI
├── matchup_engine.py     # Player matchup analysis (GPT)
├── match_simulator.py    # Match simulation (GPT)
├── utils.py              # Utility functions
├── data/
│   └── head_to_head.csv  # Batsman vs bowler data
├── output/               # Generated logs/results
├── requirements.txt      # Dependencies
└── .env                  # API key (OPENAI_API_KEY)
```

---

## ⚡ Quickstart

1. **Clone the repo & install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Add your OpenAI API key to `.env`:**
   ```env
   OPENAI_API_KEY=sk-...
   ```
3. **Run the app:**
   ```bash
   streamlit run app.py
   ```

---

## 🎯 Use Cases

- **Fantasy Sports:** Get expert-level, AI-powered advice for your fantasy cricket picks.
- **Data Engineering Portfolio:** Showcase your skills in data ingestion, processing, and AI integration.
- **AI Product Demo:** Demonstrate the power of LLMs in sports analytics and simulation.

---

## 🧠 How It Works

- **Versus Engine:**
  - Loads head-to-head stats from CSV
  - Sends context-rich prompts to GPT-4o for each batsman/bowler pair
  - Displays concise, actionable advice
- **Match Simulation:**
  - Collects team XIs, venue, pitch, and weather
  - Prompts GPT-4o to simulate the match and generate a detailed summary

---

## 🤝 Contributing

Pull requests and suggestions are welcome! For major changes, please open an issue first.

---

## 📄 License

MIT 

---

## 🚀 Deployment

### Option A: Streamlit Cloud

1. Push your code to a public GitHub repo.
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud) and sign in.
3. Click "New app", select your repo and `app.py` as the entry point.
4. Add your `OPENAI_API_KEY` as a secret in the Streamlit Cloud settings.
5. Deploy and share your app link!

### Option B: HuggingFace Spaces

1. Create a new Space at [huggingface.co/spaces](https://huggingface.co/spaces).
2. Choose "Streamlit" as the SDK.
3. Upload your code and requirements.txt.
4. Add your `OPENAI_API_KEY` as a secret or environment variable.
5. Deploy and share your Space!

---

## 🏷️ GitHub & LinkedIn Polish

- **GitHub Topics:** `data-engineering`, `openai`, `gpt-4`, `streamlit`, `fantasy-cricket`, `sports-analytics`, `portfolio-project`, `ai-simulation`
- **Project Description:**
  > AI-powered fantasy cricket analysis and match simulation. Combines data engineering, LLMs, and product design for a portfolio-grade sports analytics app.
- **LinkedIn Post Example:**
  > 🚀 Excited to share Cricklytix AI — my new portfolio project! It combines data engineering, GPT-4o, and a modern Streamlit dashboard to deliver fantasy cricket insights and match simulations. Built for sports fans, data geeks, and recruiters alike. Check it out and let me know your thoughts! #DataEngineering #OpenAI #SportsAnalytics #Portfolio 