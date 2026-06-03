# app.py
"""
Cricklytix AI — Streamlit dashboard
"""
import os
import csv
from datetime import datetime
from difflib import SequenceMatcher

import streamlit as st

from matchup_engine import generate_matchup_advice
from match_simulator import simulate_match
from utils import load_head_to_head_data, get_api_key
from player_db import (
    IPL_TEAMS, VENUES,
    get_all_player_names, get_players_by_team,
    build_player_context,
)
from live_data import get_live_matches, format_score

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Cricklytix AI",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Sidebar: Live Scores ─────────────────────────────────────────────────────
with st.sidebar:
    st.header("📡 Live Scores")
    cricapi_key = get_api_key("CRICAPI_KEY")
    matches, error = get_live_matches(cricapi_key)

    if error:
        st.info(error)
    elif not matches:
        st.info("No live matches right now.")
    else:
        for m in matches[:6]:
            name = m.get("name", "Match")
            status = m.get("status", "")
            score_str = format_score(m)
            with st.container():
                st.markdown(f"**{name}**")
                st.caption(status)
                st.text(score_str)
                st.divider()

    st.markdown("---")
    st.caption("Live data: CricAPI · Analysis: GPT-4o")

# ── Header ───────────────────────────────────────────────────────────────────
st.title("🏏 Cricklytix AI")
st.markdown("**AI-powered Fantasy Cricket Analysis & Match Simulation · IPL 2025/2026**")
st.divider()

# ── Tab layout ───────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["⚔️ Versus Engine", "🏟️ Match Simulation"])

# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — Versus Engine
# ════════════════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("⚔️ Versus Engine — Player Matchup Analysis")
    st.info(
        "Loads head-to-head stats for top IPL batsman/bowler pairs and "
        "asks GPT-4o for fantasy advice on each matchup."
    )

    col_filter, col_run = st.columns([3, 1])

    with col_filter:
        batsman_filter = st.multiselect(
            "Filter by batsman (leave blank for all)",
            options=sorted(set(load_head_to_head_data()["batsman"].tolist())),
            default=[],
        )
        bowler_filter = st.multiselect(
            "Filter by bowler (leave blank for all)",
            options=sorted(set(load_head_to_head_data()["bowler"].tolist())),
            default=[],
        )

    @st.cache_data
    def get_h2h():
        return load_head_to_head_data()

    def save_matchup_results(df: pd.DataFrame):
        os.makedirs("output", exist_ok=True)
        fname = f"output/matchup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(fname, index=False)

    with col_run:
        st.write("")
        st.write("")
        run_vs = st.button("✨ Run Analysis (GPT-4o)", use_container_width=True)

    if run_vs:
        h2h_df = get_h2h()
        if batsman_filter:
            h2h_df = h2h_df[h2h_df["batsman"].isin(batsman_filter)]
        if bowler_filter:
            h2h_df = h2h_df[h2h_df["bowler"].isin(bowler_filter)]

        if h2h_df.empty:
            st.warning("No rows match those filters.")
        else:
            with st.spinner(f"Analysing {len(h2h_df)} matchups with GPT-4o…"):
                api_key = get_api_key()
                result_df = generate_matchup_advice(h2h_df, api_key)

            st.success(f"Done — {len(result_df)} matchups analysed.")
            save_matchup_results(result_df)

            def colour_row(row):
                if row["advice_type"] == "good":
                    colour = "background-color:#d1fae5;color:#065f46;font-weight:bold"
                elif row["advice_type"] == "avoid":
                    colour = "background-color:#fee2e2;color:#991b1b;font-weight:bold"
                else:
                    colour = "background-color:#f3f4f6;color:#374151"
                return [colour] * len(row)

            display_cols = ["batsman", "bowler", "avg", "sr", "innings", "advice", "advice_type"]
            styled = result_df[display_cols].style.apply(colour_row, axis=1)
            st.markdown("#### 🏏 Fantasy Advice Table")
            st.dataframe(styled, use_container_width=True, hide_index=True)
            st.caption("🟢 Green = Pick  ·  🔴 Red = Avoid  ·  ⚪ Gray = Neutral")

    # Raw H2H table (always shown for reference)
    with st.expander("📊 View raw H2H data"):
        st.dataframe(get_h2h(), use_container_width=True, hide_index=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — Match Simulation
# ════════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("🏟️ Match Simulation Engine")
    st.info(
        "Pick 11 players per side from the IPL 2025/2026 database, "
        "set the conditions, and let GPT-4o simulate the match."
    )

    all_players = get_all_player_names()

    # ── Team builder ─────────────────────────────────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Team 1")
        team1_name = st.text_input("Team 1 name", "Team Alpha", key="t1_name")
        build_mode_1 = st.radio(
            "Build XI by", ["IPL Team", "Manual pick"], horizontal=True, key="bm1"
        )
        if build_mode_1 == "IPL Team":
            ipl_team_1 = st.selectbox("Select IPL team", IPL_TEAMS, key="ipl1")
            suggested_1 = get_players_by_team(ipl_team_1)
            team1_xi = st.multiselect(
                "XI (select exactly 11)",
                options=all_players,
                default=suggested_1[:11],
                max_selections=11,
                key="xi1",
            )
        else:
            team1_xi = st.multiselect(
                "XI (select exactly 11)",
                options=all_players,
                max_selections=11,
                key="xi1_manual",
            )
        if team1_xi:
            st.caption(f"{len(team1_xi)}/11 selected")

    with col2:
        st.markdown("### Team 2")
        team2_name = st.text_input("Team 2 name", "Team Beta", key="t2_name")
        build_mode_2 = st.radio(
            "Build XI by", ["IPL Team", "Manual pick"], horizontal=True, key="bm2"
        )
        if build_mode_2 == "IPL Team":
            ipl_team_2 = st.selectbox("Select IPL team", IPL_TEAMS, index=1, key="ipl2")
            suggested_2 = get_players_by_team(ipl_team_2)
            team2_xi = st.multiselect(
                "XI (select exactly 11)",
                options=all_players,
                default=suggested_2[:11],
                max_selections=11,
                key="xi2",
            )
        else:
            team2_xi = st.multiselect(
                "XI (select exactly 11)",
                options=all_players,
                max_selections=11,
                key="xi2_manual",
            )
        if team2_xi:
            st.caption(f"{len(team2_xi)}/11 selected")

    # ── Match conditions ──────────────────────────────────────────────────────
    st.markdown("### Match Conditions")
    cond_col1, cond_col2, cond_col3 = st.columns(3)
    with cond_col1:
        venue = st.selectbox("Venue", VENUES)
    with cond_col2:
        pitch = st.selectbox("Pitch type", ["Batting", "Balanced", "Bowling", "Spin-friendly", "Pace-friendly"])
    with cond_col3:
        weather = st.text_input("Weather", "Clear skies")

    # ── Simulate ──────────────────────────────────────────────────────────────
    sim_btn = st.button("🏟️ Simulate Match (GPT-4o)", use_container_width=True)

    if sim_btn:
        if len(team1_xi) < 11 or len(team2_xi) < 11:
            st.warning(f"Both teams need 11 players. Team 1: {len(team1_xi)}, Team 2: {len(team2_xi)}.")
        else:
            # Inject real player stats into the prompt for richer simulation
            t1_context = build_player_context(team1_xi)
            t2_context = build_player_context(team2_xi)

            with st.spinner("Simulating match with GPT-4o…"):
                api_key = get_api_key()
                summary = simulate_match(
                    team1_xi, team2_xi, venue, pitch, weather, api_key,
                    team1_context=t1_context, team2_context=t2_context,
                )

            st.success("✅ Simulation complete!")

            os.makedirs("output", exist_ok=True)
            fname = f"output/sim_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(fname, "w") as f:
                f.write(summary)

            st.markdown(f"### {team1_name} vs {team2_name} — Match Report")
            if "Could not simulate" in summary:
                st.error("GPT-4o call failed. Check your OPENAI_API_KEY.")
            st.markdown(
                f"<div style='background:#0f172a;padding:1.5rem;border-radius:12px;"
                f"color:#e2e8f0;font-size:1rem;line-height:1.7;white-space:pre-wrap'>"
                f"{summary}</div>",
                unsafe_allow_html=True,
            )

            # ── Save & Compare ────────────────────────────────────────────────
            st.markdown("---")
            st.subheader("💾 Log Actual Result & Compare")
            actual = st.text_area("Paste the actual match result here")
            if st.button("Save & Compare"):
                actuals_path = "output/actual_results.csv"
                write_header = not os.path.exists(actuals_path) or os.stat(actuals_path).st_size == 0
                with open(actuals_path, "a", newline="") as f:
                    writer = csv.writer(f)
                    if write_header:
                        writer.writerow(["datetime", "team1", "team2", "venue", "sim_summary", "actual_result"])
                    writer.writerow([datetime.now().isoformat(), team1_name, team2_name, venue, summary, actual])
                st.success("Saved to output/actual_results.csv")
                if actual.strip():
                    similarity = SequenceMatcher(None, summary, actual).ratio()
                    st.metric("Simulation accuracy (string similarity)", f"{similarity:.1%}")
                    if similarity > 0.5:
                        st.success("Simulation was fairly close to reality!")
                    else:
                        st.info("Simulation and actual result differed significantly.")
