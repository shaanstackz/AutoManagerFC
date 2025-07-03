from config import API_URL, TEAMS_API_URL, TEAM_API_URL, HEADERS
import requests
from collections import Counter
import random

def fetch_top_scorers():
    response = requests.get(API_URL, headers=HEADERS)
    print(response.status_code, response.text)
    data = response.json()
    return data["scorers"]

def select_best_lineup(players):
    # Normalize position names for filtering
    def is_goalkeeper(pos): return 'goalkeeper' in pos.lower()
    def is_defender(pos): return 'defend' in pos.lower() or 'back' in pos.lower()
    def is_midfielder(pos): return 'midfield' in pos.lower()
    def is_forward(pos): return any(x in pos.lower() for x in ['forward', 'striker', 'winger', 'attack'])

    random.shuffle(players)

    goalkeepers = [p for p in players if is_goalkeeper(p['position'])]
    defenders = [p for p in players if is_defender(p['position'])]
    midfielders = [p for p in players if is_midfielder(p['position'])]
    forwards = [p for p in players if is_forward(p['position'])]

    print(f"Goalkeepers: {len(goalkeepers)}")
    print(f"Defenders: {len(defenders)}")
    print(f"Midfielders: {len(midfielders)}")
    print(f"Forwards: {len(forwards)}")

    best_gk = goalkeepers[:1]
    best_df = defenders[:4]
    best_mf = midfielders[:4]
    best_fw = forwards[:2]

    return best_gk + best_df + best_mf + best_fw

    if not defenders:
        print("No defenders found!")
    if not midfielders:
        print("No midfielders found!")
    if not forwards:
        print("No forwards found!")

def fetch_all_players():
    teams_response = requests.get(TEAMS_API_URL, headers=HEADERS)
    teams = teams_response.json().get("teams", [])
    all_players = []
    for team in teams:
        team_id = team["id"]
        team_name = team["name"]
        team_data = requests.get(TEAM_API_URL.format(team_id), headers=HEADERS).json()
        squad = team_data.get("squad", [])
        for player in squad:
            player_dict = {
                "name": player.get("name"),
                "team": team_name,
                "position": player.get("position"),
                # Placeholder stats (API does not provide goals/assists/clean sheets here)
                "goals": 0,
                "assists": 0,
                "clean_sheets": 0
            }
            all_players.append(player_dict)
    for player in all_players:
        print(player["name"], player["position"])
    positions = set(p['position'] for p in all_players)
    print("Unique positions in all_players:", positions)
    team_counts = Counter(p['team'] for p in all_players)
    print("Players per team:", team_counts)
    return all_players
