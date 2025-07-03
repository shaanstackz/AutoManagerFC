import schedule
import time
from data_fetcher import fetch_all_players, select_best_lineup

def job():
    print("🕒 Running AutoManager...")
    players = fetch_all_players()
    best11 = select_best_lineup(players)
    print("\n🔝 Starting 11:")
    for player in best11:
        print(f"{player['name']} ({player['team']}) - {player['position']}")

def start_scheduler():
    schedule.every(6).hours.do(job)
    job()  # Run immediately on start

    while True:
        schedule.run_pending()
        time.sleep(1)
