# player_db.py
"""
IPL 2025/2026 player database — roles, teams, and career T20 stats.
Stats reflect career IPL averages through the 2025 season.
"""

PLAYERS = [
    # ── Batsmen / Wicket-keepers ────────────────────────────────────────────
    {"name": "Virat Kohli",         "team": "RCB",  "role": "Batsman",       "bat_avg": 50.2, "bat_sr": 130.7, "bowl_eco": None},
    {"name": "Rohit Sharma",        "team": "MI",   "role": "Batsman",       "bat_avg": 30.1, "bat_sr": 130.4, "bowl_eco": None},
    {"name": "Shubman Gill",        "team": "GT",   "role": "Batsman",       "bat_avg": 45.8, "bat_sr": 142.2, "bowl_eco": None},
    {"name": "KL Rahul",            "team": "LSG",  "role": "Wicket-keeper", "bat_avg": 41.2, "bat_sr": 132.5, "bowl_eco": None},
    {"name": "Jos Buttler",         "team": "RR",   "role": "Wicket-keeper", "bat_avg": 38.5, "bat_sr": 149.1, "bowl_eco": None},
    {"name": "Faf du Plessis",      "team": "RCB",  "role": "Batsman",       "bat_avg": 32.8, "bat_sr": 134.7, "bowl_eco": None},
    {"name": "Suryakumar Yadav",    "team": "MI",   "role": "Batsman",       "bat_avg": 45.6, "bat_sr": 175.4, "bowl_eco": None},
    {"name": "Rishabh Pant",        "team": "DC",   "role": "Wicket-keeper", "bat_avg": 35.8, "bat_sr": 153.2, "bowl_eco": None},
    {"name": "Sanju Samson",        "team": "RR",   "role": "Wicket-keeper", "bat_avg": 38.2, "bat_sr": 149.3, "bowl_eco": None},
    {"name": "David Warner",        "team": "DC",   "role": "Batsman",       "bat_avg": 35.1, "bat_sr": 140.5, "bowl_eco": None},
    {"name": "Ruturaj Gaikwad",     "team": "CSK",  "role": "Batsman",       "bat_avg": 38.4, "bat_sr": 134.5, "bowl_eco": None},
    {"name": "Travis Head",         "team": "SRH",  "role": "Batsman",       "bat_avg": 44.8, "bat_sr": 168.3, "bowl_eco": None},
    {"name": "Heinrich Klaasen",    "team": "SRH",  "role": "Wicket-keeper", "bat_avg": 44.3, "bat_sr": 166.8, "bowl_eco": None},
    {"name": "MS Dhoni",            "team": "CSK",  "role": "Wicket-keeper", "bat_avg": 38.0, "bat_sr": 136.2, "bowl_eco": None},
    {"name": "Ishan Kishan",        "team": "MI",   "role": "Wicket-keeper", "bat_avg": 29.5, "bat_sr": 136.7, "bowl_eco": None},
    {"name": "Devdutt Padikkal",    "team": "RR",   "role": "Batsman",       "bat_avg": 27.4, "bat_sr": 130.8, "bowl_eco": None},
    # 2025/2026 era additions
    {"name": "Yashasvi Jaiswal",    "team": "RR",   "role": "Batsman",       "bat_avg": 40.6, "bat_sr": 163.5, "bowl_eco": None},
    {"name": "Tilak Varma",         "team": "MI",   "role": "Batsman",       "bat_avg": 38.4, "bat_sr": 148.6, "bowl_eco": None},
    {"name": "Rinku Singh",         "team": "KKR",  "role": "Batsman",       "bat_avg": 34.8, "bat_sr": 168.2, "bowl_eco": None},
    {"name": "Abhishek Sharma",     "team": "SRH",  "role": "Batsman",       "bat_avg": 32.6, "bat_sr": 172.4, "bowl_eco": None},
    {"name": "Jake Fraser-McGurk",  "team": "DC",   "role": "Batsman",       "bat_avg": 28.4, "bat_sr": 182.6, "bowl_eco": None},
    {"name": "Riyan Parag",         "team": "RR",   "role": "Batsman",       "bat_avg": 28.1, "bat_sr": 142.8, "bowl_eco": None},
    {"name": "Priyansh Arya",       "team": "PBKS", "role": "Batsman",       "bat_avg": 26.8, "bat_sr": 175.4, "bowl_eco": None},
    {"name": "Phil Salt",           "team": "KKR",  "role": "Wicket-keeper", "bat_avg": 30.2, "bat_sr": 158.6, "bowl_eco": None},

    # ── All-rounders ────────────────────────────────────────────────────────
    {"name": "Hardik Pandya",       "team": "MI",   "role": "All-rounder",   "bat_avg": 28.5, "bat_sr": 148.2, "bowl_eco": 9.1},
    {"name": "Andre Russell",       "team": "KKR",  "role": "All-rounder",   "bat_avg": 32.4, "bat_sr": 178.5, "bowl_eco": 9.8},
    {"name": "Ravindra Jadeja",     "team": "CSK",  "role": "All-rounder",   "bat_avg": 24.8, "bat_sr": 132.1, "bowl_eco": 7.6},
    {"name": "Sunil Narine",        "team": "KKR",  "role": "All-rounder",   "bat_avg": 20.2, "bat_sr": 163.5, "bowl_eco": 6.7},
    {"name": "Washington Sundar",   "team": "SRH",  "role": "All-rounder",   "bat_avg": 22.1, "bat_sr": 128.4, "bowl_eco": 7.3},
    {"name": "Glenn Maxwell",       "team": "RCB",  "role": "All-rounder",   "bat_avg": 28.6, "bat_sr": 158.2, "bowl_eco": 8.5},
    {"name": "Liam Livingstone",    "team": "PBKS", "role": "All-rounder",   "bat_avg": 26.8, "bat_sr": 155.3, "bowl_eco": 9.2},
    {"name": "Marcus Stoinis",      "team": "LSG",  "role": "All-rounder",   "bat_avg": 28.4, "bat_sr": 152.8, "bowl_eco": 9.5},
    {"name": "Axar Patel",          "team": "DC",   "role": "All-rounder",   "bat_avg": 23.1, "bat_sr": 144.6, "bowl_eco": 7.8},
    {"name": "Shardul Thakur",      "team": "KKR",  "role": "All-rounder",   "bat_avg": 18.2, "bat_sr": 151.0, "bowl_eco": 9.4},
    {"name": "Venkatesh Iyer",      "team": "KKR",  "role": "All-rounder",   "bat_avg": 30.2, "bat_sr": 152.4, "bowl_eco": 9.8},
    {"name": "Nitish Kumar Reddy",  "team": "SRH",  "role": "All-rounder",   "bat_avg": 26.8, "bat_sr": 148.6, "bowl_eco": 9.4},
    {"name": "Mitchell Marsh",      "team": "DC",   "role": "All-rounder",   "bat_avg": 28.4, "bat_sr": 155.8, "bowl_eco": 9.6},
    {"name": "Cameron Green",       "team": "MI",   "role": "All-rounder",   "bat_avg": 24.6, "bat_sr": 148.2, "bowl_eco": 9.5},

    # ── Bowlers ─────────────────────────────────────────────────────────────
    {"name": "Jasprit Bumrah",      "team": "MI",   "role": "Bowler",        "bat_avg": None, "bat_sr": None, "bowl_eco": 6.7},
    {"name": "Yuzvendra Chahal",    "team": "RR",   "role": "Bowler",        "bat_avg": None, "bat_sr": None, "bowl_eco": 7.9},
    {"name": "Mohammed Shami",      "team": "GT",   "role": "Bowler",        "bat_avg": None, "bat_sr": None, "bowl_eco": 8.2},
    {"name": "Rashid Khan",         "team": "GT",   "role": "Bowler",        "bat_avg": None, "bat_sr": None, "bowl_eco": 6.7},
    {"name": "Mitchell Starc",      "team": "KKR",  "role": "Bowler",        "bat_avg": None, "bat_sr": None, "bowl_eco": 9.3},
    {"name": "Trent Boult",         "team": "MI",   "role": "Bowler",        "bat_avg": None, "bat_sr": None, "bowl_eco": 8.1},
    {"name": "Kagiso Rabada",       "team": "PBKS", "role": "Bowler",        "bat_avg": None, "bat_sr": None, "bowl_eco": 8.6},
    {"name": "Mohammed Siraj",      "team": "RCB",  "role": "Bowler",        "bat_avg": None, "bat_sr": None, "bowl_eco": 9.0},
    {"name": "Arshdeep Singh",      "team": "PBKS", "role": "Bowler",        "bat_avg": None, "bat_sr": None, "bowl_eco": 8.9},
    {"name": "Deepak Chahar",       "team": "CSK",  "role": "Bowler",        "bat_avg": None, "bat_sr": None, "bowl_eco": 8.3},
    {"name": "T Natarajan",         "team": "SRH",  "role": "Bowler",        "bat_avg": None, "bat_sr": None, "bowl_eco": 9.1},
    {"name": "Kuldeep Yadav",       "team": "DC",   "role": "Bowler",        "bat_avg": None, "bat_sr": None, "bowl_eco": 8.0},
    {"name": "Varun Chakravarthy",  "team": "KKR",  "role": "Bowler",        "bat_avg": None, "bat_sr": None, "bowl_eco": 7.7},
    {"name": "Pat Cummins",         "team": "SRH",  "role": "Bowler",        "bat_avg": None, "bat_sr": None, "bowl_eco": 9.2},
    {"name": "Harshal Patel",       "team": "RCB",  "role": "Bowler",        "bat_avg": None, "bat_sr": None, "bowl_eco": 9.0},
    # 2025/2026 era additions
    {"name": "Mayank Yadav",        "team": "LSG",  "role": "Bowler",        "bat_avg": None, "bat_sr": None, "bowl_eco": 7.4},
    {"name": "Noor Ahmad",          "team": "GT",   "role": "Bowler",        "bat_avg": None, "bat_sr": None, "bowl_eco": 8.2},
    {"name": "Akash Deep",          "team": "RCB",  "role": "Bowler",        "bat_avg": None, "bat_sr": None, "bowl_eco": 9.1},
    {"name": "Tushar Deshpande",    "team": "CSK",  "role": "Bowler",        "bat_avg": None, "bat_sr": None, "bowl_eco": 9.5},
    {"name": "Anrich Nortje",       "team": "DC",   "role": "Bowler",        "bat_avg": None, "bat_sr": None, "bowl_eco": 8.8},
    {"name": "Josh Hazlewood",      "team": "RCB",  "role": "Bowler",        "bat_avg": None, "bat_sr": None, "bowl_eco": 8.3},
]

IPL_TEAMS = ["CSK", "DC", "GT", "KKR", "LSG", "MI", "PBKS", "RCB", "RR", "SRH"]

VENUES = [
    "Wankhede Stadium, Mumbai",
    "M. Chinnaswamy Stadium, Bangalore",
    "Eden Gardens, Kolkata",
    "MA Chidambaram Stadium, Chennai",
    "Narendra Modi Stadium, Ahmedabad",
    "Sawai Mansingh Stadium, Jaipur",
    "Punjab Cricket Association Stadium, Mohali",
    "Rajiv Gandhi International Stadium, Hyderabad",
    "Arun Jaitley Stadium, Delhi",
    "BRSABV Ekana Cricket Stadium, Lucknow",
    "Dr. DY Patil Sports Academy, Mumbai",
    "Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium, Lucknow",
]


def get_all_player_names() -> list:
    return sorted(p["name"] for p in PLAYERS)


def get_players_by_team(team: str) -> list:
    return sorted(p["name"] for p in PLAYERS if p["team"] == team)


def get_batsmen() -> list:
    return sorted(p["name"] for p in PLAYERS if p["role"] in ("Batsman", "Wicket-keeper", "All-rounder"))


def get_bowlers() -> list:
    return sorted(p["name"] for p in PLAYERS if p["role"] in ("Bowler", "All-rounder"))


def get_player(name: str) -> dict | None:
    return next((p for p in PLAYERS if p["name"] == name), None)


def build_player_context(names: list) -> str:
    """Compact stats string injected into GPT simulation prompts."""
    lines = []
    for name in names:
        p = get_player(name)
        if not p:
            lines.append(name)
            continue
        parts = [f"{name} ({p['team']}, {p['role']})"]
        if p["bat_avg"]:
            parts.append(f"bat avg {p['bat_avg']}, SR {p['bat_sr']}")
        if p["bowl_eco"]:
            parts.append(f"eco {p['bowl_eco']}")
        lines.append(" — ".join(parts))
    return "\n".join(lines)
