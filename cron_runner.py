import schedule
import time
import subprocess

def job():
    print("[cron_runner] Running head-to-head scraper...")
    result = subprocess.run(["python3", "scraper/head_to_head_scraper.py"], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("[cron_runner] Error:", result.stderr)
    print("[cron_runner] Scraper run complete.")

schedule.every().hour.do(job)

if __name__ == "__main__":
    print("[cron_runner] Starting hourly scheduler for head-to-head scraper...")
    job()  # Run once at start
    while True:
        schedule.run_pending()
        time.sleep(10) 