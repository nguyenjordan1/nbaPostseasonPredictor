from app.db import get_connection

# Conferences
CONFERENCE = {
    "Boston Celtics": "East",
    "Brooklyn Nets": "East",
    "New York Knicks": "East",
    "Philadelphia 76ers": "East",
    "Toronto Raptors": "East",
    "Chicago Bulls": "East",
    "Cleveland Cavaliers": "East",
    "Detroit Pistons": "East",
    "Indiana Pacers": "East",
    "Milwaukee Bucks": "East",
    "Atlanta Hawks": "East",
    "Charlotte Hornets": "East",
    "Miami Heat": "East",
    "Orlando Magic": "East",
    "Washington Wizards": "East",

    "Dallas Mavericks": "West",
    "Denver Nuggets": "West",
    "Golden State Warriors": "West",
    "Houston Rockets": "West",
    "LA Clippers": "West",
    "Los Angeles Lakers": "West",
    "Memphis Grizzlies": "West",
    "Minnesota Timberwolves": "West",
    "New Orleans Pelicans": "West",
    "Oklahoma City Thunder": "West",
    "Phoenix Suns": "West",
    "Portland Trail Blazers": "West",
    "Sacramento Kings": "West",
    "San Antonio Spurs": "West",
    "Utah Jazz": "West"
}

# Parse Score 
# @score score from games table 
# return score parsed
def parse_score(score):
    """
    Converts:
        "L138-118" -> ("L", 138, 118)
        "W120-110" -> ("W", 120, 110)
    """
    if not score or len(score) < 4:
        return None

    try:
        result = score[0]
        nums = score[1:]
        team_score, opp_score = nums.split("-")
        return result, int(team_score), int(opp_score)
    except:
        return None


# Home Vs Away Win Percentage
# return the home and the away win percentage
def home_vs_away_win_percentage():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT location, score FROM games")
    rows = cursor.fetchall()

    home_wins = home_games = 0
    away_wins = away_games = 0

    for location, score in rows:
        parsed = parse_score(score)
        if not parsed:
            continue

        result, _, _ = parsed

        if location == "Home":
            home_games += 1
            if result == "W":
                home_wins += 1

        elif location == "Away":
            away_games += 1
            if result == "W":
                away_wins += 1

    conn.close()

    return {
        "home_win_pct": round((home_wins / home_games) * 100, 2) if home_games else 0,
        "away_win_pct": round((away_wins / away_games) * 100, 2) if away_games else 0
    }


# East Vs West Win Percentage
# return the percentages of east and west when playing each other
def east_vs_west_win_percentage():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT g.team, t1.conference, g.opponent, t2.conference, g.score
        FROM games g
        JOIN teams t1 ON g.team = t1.name
        JOIN teams t2 ON g.opponent = t2.name
    """)

    rows = cursor.fetchall()

    east_wins = east_games = 0
    west_wins = west_games = 0

    for _, team_conf, _, opp_conf, score in rows:
        parsed = parse_score(score)
        if not parsed:
            continue

        result, _, _ = parsed

        if team_conf == "East" and opp_conf == "West":
            east_games += 1
            if result == "W":
                east_wins += 1

        elif team_conf == "West" and opp_conf == "East":
            west_games += 1
            if result == "W":
                west_wins += 1

    conn.close()

    return {
        "east_win_pct": round((east_wins / east_games) * 100, 2) if east_games else 0,
        "west_win_pct": round((west_wins / west_games) * 100, 2) if west_games else 0
    }

# Overall team Rankings based on number of wins
# return rankings of teams based on wins
def overall_team_rankings():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT team, score FROM games")
    rows = cursor.fetchall()

    stats = {}

    for team, score in rows:
        parsed = parse_score(score)
        if not parsed:
            continue

        result, _, _ = parsed

        if team not in stats:
            stats[team] = {"wins": 0, "games": 0}

        stats[team]["games"] += 1
        if result == "W":
            stats[team]["wins"] += 1

    conn.close()

    rankings = []
    for team, data in stats.items():
        win_pct = (data["wins"] / data["games"]) * 100
        rankings.append({
            "team": team,
            "win_pct": round(win_pct, 2)
        })

    rankings.sort(key=lambda x: x["win_pct"], reverse=True)
    return rankings

# Average Point differential
# return the point differential of teams
def average_point_differential():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT team, score FROM games")
    rows = cursor.fetchall()

    stats = {}

    for team, score in rows:
        parsed = parse_score(score)
        if not parsed:
            continue

        result, team_score, opp_score = parsed

        margin = team_score - opp_score
        differential = margin if result == "W" else -margin

        if team not in stats:
            stats[team] = {"total_diff": 0, "games": 0}

        stats[team]["total_diff"] += differential
        stats[team]["games"] += 1

    conn.close()

    rankings = []
    for team, data in stats.items():
        avg = data["total_diff"] / data["games"]
        rankings.append({
            "team": team,
            "avg_diff": round(avg, 2)
        })

    rankings.sort(key=lambda x: x["avg_diff"], reverse=True)
    return rankings

if __name__ == "__main__":
    print(home_vs_away_win_percentage())
    print(east_vs_west_win_percentage())
    print(overall_team_rankings()[:10])
    print(average_point_differential()[:10])