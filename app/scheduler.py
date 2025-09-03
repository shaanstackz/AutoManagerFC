import schedule
import time
from app.data_fetcher import fetch_top_scorers
from app.team_selector import select_best_players


def job():
    print("🕒 Running AutoManager...")

    # ✅ fetch players from API
    players = fetch_top_scorers()

    if not players:
        print("⚠️ No players fetched, using fallback lineup...")
        # fallback dummy lineup
        players = [
            {"name": f"Player{i}", "team": "Auto FC", "position": pos, "goals": i, "clean_sheets": i // 2}
            for i, pos in enumerate(
                ["GK", "DEF", "DEF", "DEF", "DEF", "MID", "MID", "MID", "ATT", "ATT", "ATT"], start=1
            )
        ]

    # ✅ pick best 11
    best11 = select_best_players(players)

    print("\n🔝 Starting 11:")
    for player in best11:
        print(
            f"{player['name']} ({player['team']}) - {player['position']} "
            f"| Goals: {player.get('goals', 0)}, Clean Sheets: {player.get('clean_sheets', 0)}"
        )


def start_scheduler():
    schedule.every(6).hours.do(job)
    job()  # run immediately on start

    while True:
        schedule.run_pending()
        time.sleep(1)
