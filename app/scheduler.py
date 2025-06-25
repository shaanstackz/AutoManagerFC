import schedule
import time
from data_fetcher import fetch_top_scorers
from team_selector import select_best_players

def job():
    print("🕒 Running AutoManager...")
    players = fetch_top_scorers()
    best11 = select_best_players([{
        "name": p["player"]["name"],
        "team": p["team"]["name"],
        "goals": p["goals"]
    } for p in players])
    print("Raw players fetched:")
    print(players)
    print("\n🔝 Starting 11:")
    for player in best11:
        print(f"{player['name']} ({player['team']}) - {player['goals']} goals")

def start_scheduler():
    schedule.every(6).hours.do(job)
    job()  # Run immediately on start

    while True:
        schedule.run_pending()
        time.sleep(1)
