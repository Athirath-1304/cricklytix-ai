import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

def fetch_h2h_stats(batsman_id, bowler_id, batsman_name, bowler_name):
    url = f"https://stats.espncricinfo.com/ci/engine/player/{batsman_id}.html?class=3;opposition={bowler_id};template=results;type=batting"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/115.0.0.0 Safari/537.36"
        )
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        os.makedirs("output", exist_ok=True)
        with open("output/error.log", "a") as log:
            log.write(f"[{time.ctime()}] Failed to fetch: {url} (Status: {response.status_code})\n")
        print(f"Failed to fetch data for {batsman_name} vs {bowler_name}")
        return None
    soup = BeautifulSoup(response.content, "lxml")
    table = soup.find("table", class_="engineTable")
    # Save the table HTML for debugging
    os.makedirs("output", exist_ok=True)
    with open(f"output/{batsman_name}_vs_{bowler_name}.html", "w", encoding="utf-8") as f:
        f.write(str(table))
    if not table:
        print(f"No table found for {batsman_name} vs {bowler_name}")
        return {
            "batsman": batsman_name,
            "bowler": bowler_name,
            "avg": 0,
            "sr": 0,
            "innings": 0
        }
    for row in table.find_all("tr"):
        if "Overall" in row.text:
            cols = [col.text.strip() for col in row.find_all("td")]
            if len(cols) >= 8:
                return {
                    "batsman": batsman_name,
                    "bowler": bowler_name,
                    "avg": float(cols[6]) if cols[6] != "-" else 0,
                    "sr": float(cols[7]) if cols[7] != "-" else 0,
                    "innings": int(cols[1]) if cols[1] != "-" else 0
                }
    print(f"No 'Overall' row for {batsman_name} vs {bowler_name}")
    return {
        "batsman": batsman_name,
        "bowler": bowler_name,
        "avg": 0,
        "sr": 0,
        "innings": 0
    }

def run_scraper():
    # Use pairs with known T20 history
    pairs = [
        (253802, 21422, "Virat Kohli", "Sunil Narine"),
        (34102, 311067, "Rohit Sharma", "Mitchell Starc"),
        (277916, 430246, "Jos Buttler", "Yuzvendra Chahal"),
    ]
    results = []
    for batsman_id, bowler_id, batsman_name, bowler_name in pairs:
        print(f"Fetching {batsman_name} vs {bowler_name}...")
        stats = fetch_h2h_stats(batsman_id, bowler_id, batsman_name, bowler_name)
        if stats:
            results.append(stats)
        time.sleep(1)  # Be polite to ESPNcricinfo
    df = pd.DataFrame(results)
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/head_to_head.csv", index=False)
    print("Updated data/head_to_head.csv with latest head-to-head stats.")

if __name__ == "__main__":
    run_scraper() 