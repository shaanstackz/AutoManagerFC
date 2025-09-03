from app.config import API_URL, TEAMS_API_URL, TEAM_API_URL, HEADERS, API_FOOTBALL_KEY, API_FOOTBALL_HOST, API_FOOTBALL_BASE_URL
import requests
from collections import Counter
import random
from difflib import get_close_matches

def fetch_player_goals():
    response = requests.get(API_URL, headers=HEADERS)
    data = response.json()
    print("Scorers API response:", data)  # DEBUG: print full API response
    # Build a dict: {player_name: goals}
    goals_dict = {p['player']['name']: p['goals'] for p in data.get('scorers', [])}
    print("Goals dict keys:", list(goals_dict.keys()))  # DEBUG: print keys
    return goals_dict

# --- API-FOOTBALL (RapidAPI) CLEAN SHEETS FETCHING ---
def fetch_clean_sheets_for_team(team_id, season=2023, league=39):
    """
    Fetches all players and their clean sheets for a given team from API-Football.
    Returns a dict: {player_name: clean_sheets}
    """
    url = f"{API_FOOTBALL_BASE_URL}/players?team={team_id}&season={season}&league={league}"
    headers = {
        "x-rapidapi-key": API_FOOTBALL_KEY,
        "x-rapidapi-host": API_FOOTBALL_HOST
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    clean_sheets = {}
    for player_info in data.get("response", []):
        player = player_info.get("player", {})
        stats = player_info.get("statistics", [{}])[0]
        name = player.get("name")
        cs = stats.get("games", {}).get("clean_sheets", {}).get("total", 0)
        if name:
            clean_sheets[name] = cs
    return clean_sheets

def fetch_all_clean_sheets(team_ids, season=2023, league=39):
    """
    Fetches clean sheets for all teams in team_ids.
    Returns a dict: {player_name: clean_sheets}
    """
    all_clean_sheets = {}
    for team_id in team_ids:
        team_clean_sheets = fetch_clean_sheets_for_team(team_id, season, league)
        all_clean_sheets.update(team_clean_sheets)
    return all_clean_sheets

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

# Fetch all players from all teams in the PL, and merge in real goal and clean sheet stats using fuzzy matching
def fetch_all_players():
    teams_response = requests.get(TEAMS_API_URL, headers=HEADERS)
    teams = teams_response.json().get("teams", [])
    all_players = []
    team_ids = []  # For API-Football
    for team in teams:
        team_id = team["id"]
        team_name = team["name"]
        team_ids.append(team_id)  # Note: these are football-data.org IDs, not API-Football IDs
        team_data = requests.get(TEAM_API_URL.format(team_id), headers=HEADERS).json()
        squad = team_data.get("squad", [])
        for player in squad:
            player_dict = {
                "name": player.get("name"),
                "team": team_name,
                "position": player.get("position"),
                "goals": 0,  # will be updated
                "assists": 0,
                "clean_sheets": 0  # will be updated
            }
            all_players.append(player_dict)
    print("Sample player names:", [p['name'] for p in all_players[:10]])  # DEBUG: print sample names
    # Merge in real goals using fuzzy matching
    goals_dict = fetch_player_goals()
    for player in all_players:
        matches = get_close_matches(player['name'], goals_dict.keys(), n=1, cutoff=0.8)
        print(f"Player: {player['name']} | Match: {matches}")  # DEBUG: print fuzzy match
        goals = goals_dict.get(player['name'])
        if goals is None and matches:
            goals = goals_dict[matches[0]]
        if goals is None:
            goals = 0
        player['goals'] = goals
    # --- Merge in clean sheets using fuzzy matching (requires correct API-Football team IDs) ---
    # clean_sheets_dict = fetch_all_clean_sheets(api_football_team_ids)
    # for player in all_players:
    #     cs = clean_sheets_dict.get(player['name'])
    #     if cs is None:
    #         matches = get_close_matches(player['name'], clean_sheets_dict.keys(), n=1, cutoff=0.8)
    #         print(f"Player: {player['name']} | Clean Sheet Match: {matches}")  # DEBUG: print fuzzy match
    #         if matches:
    #             cs = clean_sheets_dict[matches[0]]
    #         else:
    #             cs = 0
    #     player['clean_sheets'] = cs
    return all_players
