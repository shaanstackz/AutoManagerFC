# app/team_selector.py

def select_best_players(players, formation="4-3-3"):
    """
    Pick the best 11 players based on goals scored.
    Args:
        players (list[dict]): List of player data (must include "name", "position", "goals").
        formation (str): Formation to use (default = 4-3-3).
    Returns:
        list[dict]: Best 11 players.
    """

    if not players:
        return []

    # Sort players by goals scored (descending)
    players_sorted = sorted(players, key=lambda p: p.get("goals", 0), reverse=True)

    # Formation breakdown
    formation_map = {
        "4-3-3": {"DEF": 4, "MID": 3, "ATT": 3, "GK": 1},
        "4-4-2": {"DEF": 4, "MID": 4, "ATT": 2, "GK": 1},
        "3-5-2": {"DEF": 3, "MID": 5, "ATT": 2, "GK": 1},
    }

    slots = formation_map.get(formation, formation_map["4-3-3"])

    lineup = []

    # Pick players by position
    for pos, count in slots.items():
        chosen = [p for p in players_sorted if p.get("position") == pos][:count]
        lineup.extend(chosen)

    return lineup

