import streamlit as st
import pandas as pd
from matchup_engine import generate_matchup_advice, classify_advice
from match_simulator import simulate_match
from utils import load_head_to_head_data, get_api_key
import os
from datetime import datetime

st.set_page_config(page_title="Cricklytix AI", layout="wide")
st.title("🏏 Cricklytix AI")
st.markdown(":crystal_ball: **AI-powered Fantasy Cricket Analysis & Match Simulation**")

# --- Versus Engine Section ---
st.header("1. Versus Engine (Player Matchup Analysis) :crossed_swords:")
st.info("Run the Versus Engine to get fantasy advice for player matchups.")

@st.cache_data
def get_h2h():
    return load_head_to_head_data()

def save_matchup_results(df):
    os.makedirs("output", exist_ok=True)
    fname = f"output/matchup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(fname, index=False)

if st.button("✨ Run Versus Engine (GPT-4o)"):
    h2h_df = get_h2h()
    with st.spinner("Analyzing matchups with GPT-4o..."):
        api_key = get_api_key()
        result_df = generate_matchup_advice(h2h_df, api_key)
    st.success("Analysis complete!")
    save_matchup_results(result_df)
    def color_advice(val, typ):
        if typ == "good":
            return "background-color: #d1fae5; color: #065f46; font-weight: bold;"
        elif typ == "avoid":
            return "background-color: #fee2e2; color: #991b1b; font-weight: bold;"
        else:
            return "background-color: #f3f4f6; color: #374151;"
    styled = result_df[["batsman", "bowler", "avg", "sr", "innings", "advice", "advice_type"]].style.apply(
        lambda row: [color_advice(row["advice"], row["advice_type"])]*6 + [""], axis=1)
    st.markdown(":sparkles: **Fantasy Advice Table**")
    st.dataframe(styled, use_container_width=True, hide_index=True)
    st.caption("Green = Good pick, Red = Avoid, Gray = Neutral")

# --- Match Simulation Section ---
st.header("2. Match Simulation Engine :cricket_bat_and_ball:")
st.info("Simulate a full match with AI-generated outcomes.")

with st.form("match_sim_form"):
    team1 = st.text_input("Team 1 Name", "Team Alpha")
    team2 = st.text_input("Team 2 Name", "Team Beta")
    team1_xi = st.text_area("Team 1 Playing XI (comma-separated)", "Player1, Player2, Player3, Player4, Player5, Player6, Player7, Player8, Player9, Player10, Player11")
    team2_xi = st.text_area("Team 2 Playing XI (comma-separated)", "PlayerA, PlayerB, PlayerC, PlayerD, PlayerE, PlayerF, PlayerG, PlayerH, PlayerI, PlayerJ, PlayerK")
    venue = st.text_input("Venue", "Wankhede Stadium")
    pitch = st.selectbox("Pitch Type", ["Batting", "Bowling", "Balanced", "Spin-friendly", "Pace-friendly"])
    weather = st.text_input("Weather", "Clear skies")
    submitted = st.form_submit_button("🏟️ Simulate Match (GPT-4o)")

if submitted:
    t1_xi = [p.strip() for p in team1_xi.split(",") if p.strip()]
    t2_xi = [p.strip() for p in team2_xi.split(",") if p.strip()]
    with st.spinner(":hourglass_flowing_sand: Simulating match with GPT-4o..."):
        api_key = get_api_key()
        summary = simulate_match(t1_xi, t2_xi, venue, pitch, weather, api_key)
    st.success(":trophy: Simulation complete!")
    # Save simulation summary
    os.makedirs("output", exist_ok=True)
    fname = f"output/sim_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(fname, "w") as f:
        f.write(summary)
    st.markdown(f"### {team1} vs {team2} — Match Summary")
    if "Could not simulate match" in summary:
        st.error("OpenAI API failed. Please check your key or try again later.")
    st.markdown(f"<div style='background:rgba(0,0,0,0.7);padding:1.5em;border-radius:1em;color:#0ff;font-size:1.1em'>{summary}</div>", unsafe_allow_html=True)

    # --- Save & Compare Feature ---
    st.subheader(":floppy_disk: Save & Compare Actual Result")
    actual_result = st.text_area("Enter actual match result (paste summary or main stats)")
    if st.button("Save Actual Result & Compare"):
        actuals_path = "output/actual_results.csv"
        import csv
        # Save actual result
        with open(actuals_path, "a", newline="") as f:
            writer = csv.writer(f)
            if os.stat(actuals_path).st_size == 0:
                writer.writerow(["datetime", "team1", "team2", "venue", "sim_summary", "actual_result"])
            writer.writerow([
                datetime.now().isoformat(), team1, team2, venue, summary, actual_result
            ])
        st.success("Actual result saved!")
        # Compare (simple string similarity)
        if actual_result.strip():
            from difflib import SequenceMatcher
            sim = SequenceMatcher(None, summary, actual_result).ratio()
            st.markdown(f"**Similarity between simulation and actual:** {sim:.2%}")
            if sim > 0.5:
                st.success("Simulation was fairly close to actual result!")
            else:
                st.info("Simulation and actual result differ significantly.")
