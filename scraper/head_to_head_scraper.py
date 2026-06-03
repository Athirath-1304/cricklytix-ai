# scraper/head_to_head_scraper.py
"""
Scrapes IPL T20 head-to-head stats from ESPNcricinfo (class=6).
Merges fresh rows with the existing seeded CSV — pre-seeded data is
preserved if a scrape fails or returns zero innings.
"""
import os
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup

OUTPUT_CSV = "data/head_to_head.csv"
ERROR_LOG = "output/error.log"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

# (batsman_espn_id, bowler_espn_id, batsman_name, bowler_name)
PAIRS = [
    (253802, 21422,   "Virat Kohli",        "Sunil Narine"),
    (253802, 625383,  "Virat Kohli",        "Jasprit Bumrah"),
    (253802, 430246,  "Virat Kohli",        "Yuzvendra Chahal"),
    (253802, 788803,  "Virat Kohli",        "Rashid Khan"),
    (34102,  625383,  "Rohit Sharma",       "Jasprit Bumrah"),
    (34102,  21422,   "Rohit Sharma",       "Sunil Narine"),
    (34102,  311067,  "Rohit Sharma",       "Mitchell Starc"),
    (34102,  430246,  "Rohit Sharma",       "Yuzvendra Chahal"),
    (277916, 430246,  "Jos Buttler",        "Yuzvendra Chahal"),
    (277916, 625383,  "Jos Buttler",        "Jasprit Bumrah"),
    (277916, 788803,  "Jos Buttler",        "Rashid Khan"),
    (481896, 625383,  "Suryakumar Yadav",   "Jasprit Bumrah"),
    (481896, 788803,  "Suryakumar Yadav",   "Rashid Khan"),
    (655671, 430246,  "Shubman Gill",       "Yuzvendra Chahal"),
    (655671, 788803,  "Shubman Gill",       "Rashid Khan"),
    (655671, 56143,   "Shubman Gill",       "Mohammed Shami"),
    (422108, 625383,  "KL Rahul",           "Jasprit Bumrah"),
    (422108, 21422,   "KL Rahul",           "Sunil Narine"),
    (489889, 430246,  "Sanju Samson",       "Yuzvendra Chahal"),
    (489889, 625383,  "Sanju Samson",       "Jasprit Bumrah"),
    (32540,  430246,  "David Warner",       "Yuzvendra Chahal"),
    (32540,  788803,  "David Warner",       "Rashid Khan"),
    (53,     625383,  "Rishabh Pant",       "Jasprit Bumrah"),
    (53,     788803,  "Rishabh Pant",       "Rashid Khan"),
    (45789,  625383,  "Faf du Plessis",     "Jasprit Bumrah"),
    (45789,  21422,   "Faf du Plessis",     "Sunil Narine"),
    (300733, 625383,  "Andre Russell",      "Jasprit Bumrah"),
    (300733, 430246,  "Andre Russell",      "Yuzvendra Chahal"),
    (1125918, 625383, "Yashasvi Jaiswal",   "Jasprit Bumrah"),
    (1125918, 788803, "Yashasvi Jaiswal",   "Rashid Khan"),
    (1151273, 625383, "Tilak Varma",        "Jasprit Bumrah"),
    (1151273, 430246, "Tilak Varma",        "Yuzvendra Chahal"),
    (1151304, 625383, "Rinku Singh",        "Jasprit Bumrah"),
    (1151304, 788803, "Rinku Singh",        "Rashid Khan"),
    (1207645, 625383, "Abhishek Sharma",    "Jasprit Bumrah"),
    (1207645, 430246, "Abhishek Sharma",    "Yuzvendra Chahal"),
]


def log_error(msg: str):
    os.makedirs(os.path.dirname(ERROR_LOG), exist_ok=True)
    with open(ERROR_LOG, "a") as f:
        f.write(f"[{time.ctime()}] {msg}\n")


def fetch_h2h(batsman_id: int, bowler_id: int, batsman_name: str, bowler_name: str) -> dict | None:
    """
    Fetch IPL T20 (class=6) head-to-head stats for one pair.
    Returns dict with avg/sr/innings, or None on network failure.
    """
    url = (
        f"https://stats.espncricinfo.com/ci/engine/player/{batsman_id}.html"
        f"?class=6;opposition={bowler_id};template=results;type=batting"
    )
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
    except requests.RequestException as e:
        log_error(f"Request failed {batsman_name} vs {bowler_name}: {e}")
        return None

    if resp.status_code != 200:
        log_error(f"HTTP {resp.status_code} for {batsman_name} vs {bowler_name}")
        return None

    soup = BeautifulSoup(resp.content, "lxml")

    for table in soup.find_all("table", class_="engineTable"):
        for row in table.find_all("tr"):
            cells = [td.get_text(strip=True) for td in row.find_all("td")]
            if not cells or cells[0] not in ("Overall", "Total"):
                continue
            try:
                return {
                    "batsman": batsman_name,
                    "bowler":  bowler_name,
                    "innings": int(cells[1]) if cells[1].isdigit() else 0,
                    "avg":     float(cells[6]) if cells[6] not in ("-", "") else 0.0,
                    "sr":      float(cells[7]) if cells[7] not in ("-", "") else 0.0,
                }
            except (IndexError, ValueError) as e:
                log_error(f"Parse error {batsman_name} vs {bowler_name}: {e}")
                return None

    # No innings found vs this bowler
    return {"batsman": batsman_name, "bowler": bowler_name, "innings": 0, "avg": 0.0, "sr": 0.0}


def run_scraper(delay: float = 1.5):
    """
    Scrape all PAIRS, merge with existing CSV.
    Scraped rows overwrite pre-seeded rows for the same pair only when innings > 0.
    """
    existing = {}
    if os.path.exists(OUTPUT_CSV):
        df_ex = pd.read_csv(OUTPUT_CSV)
        for _, row in df_ex.iterrows():
            existing[(row["batsman"], row["bowler"])] = row.to_dict()

    scraped = 0
    for batsman_id, bowler_id, batsman_name, bowler_name in PAIRS:
        print(f"  {batsman_name} vs {bowler_name}...", end=" ", flush=True)
        result = fetch_h2h(batsman_id, bowler_id, batsman_name, bowler_name)
        key = (batsman_name, bowler_name)
        if result and result["innings"] > 0:
            existing[key] = result
            scraped += 1
            print(f"avg={result['avg']} sr={result['sr']} inn={result['innings']}")
        elif result:
            existing.setdefault(key, result)
            print("no IPL innings")
        else:
            print("failed")
        time.sleep(delay)

    os.makedirs("data", exist_ok=True)
    df_out = pd.DataFrame(list(existing.values()))[["batsman", "bowler", "avg", "sr", "innings"]]
    df_out.to_csv(OUTPUT_CSV, index=False)
    print(f"\nDone. {scraped}/{len(PAIRS)} pairs updated. CSV has {len(df_out)} rows.")


if __name__ == "__main__":
    run_scraper()
