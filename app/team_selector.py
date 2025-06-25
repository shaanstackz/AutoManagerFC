def select_best_players(players, max_players=11):
    sorted_players = sorted(players, key=lambda p: p['goals'], reverse=True)
    return sorted_players[:max_players]
