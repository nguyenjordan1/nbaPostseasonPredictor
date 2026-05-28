from app.db import get_connection

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

def home_vs_away_win_percentage():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT location, score
        FROM games
    """)

    home_wins = home_games = 0
    away_wins = away_games = 0

    for location, score in cursor.fetchall():

        if not score:
            continue

        if location == "Home":
            home_games += 1
            if score.startswith("W"):
                home_wins += 1

        elif location == "Away":
            away_games += 1
            if score.startswith("W"):
                away_wins += 1

    print("🏠 Home Win %:", round((home_wins / home_games * 100), 2) if home_games else 0)
    print("✈️ Away Win %:", round((away_wins / away_games * 100), 2) if away_games else 0)

    conn.close()


def east_vs_west_win_percentage():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT g.team, t1.conference, g.opponent, t2.conference, g.score
        FROM games g
        JOIN teams t1 ON g.team = t1.name
        JOIN teams t2 ON g.opponent = t2.name
    """)

    east_wins = east_games = 0
    west_wins = west_games = 0

    for team, team_conf, opp, opp_conf, score in cursor.fetchall():

        if team_conf == "East" and opp_conf == "West":
            east_games += 1
            if score.startswith("W"):
                east_wins += 1

        elif team_conf == "West" and opp_conf == "East":
            west_games += 1
            if score.startswith("W"):
                west_wins += 1

    print("🟦 East vs West Win %:", round((east_wins / east_games * 100), 2) if east_games else 0)
    print("🟥 West vs East Win %:", round((west_wins / west_games * 100), 2) if west_games else 0)

def overall_team_rankings():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT team, score
        FROM games
    """)

    stats = {}

    for team, score in cursor.fetchall():

        if not score:
            continue

        if team not in stats:
            stats[team] = {
                "wins": 0,
                "games": 0
            }

        stats[team]["games"] += 1

        if score.startswith("W"):
            stats[team]["wins"] += 1

    rankings = []

    for team, data in stats.items():

        win_pct = (
            data["wins"] / data["games"] * 100
        )

        rankings.append((team, win_pct))

    rankings.sort(key=lambda x: x[1], reverse=True)

    print("\n🏆 Overall Team Rankings")

    for i, (team, pct) in enumerate(rankings[:10], start=1):
        print(f"{i}. {team} - {round(pct, 2)}%")

    conn.close()

def average_point_differential():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT team, score
        FROM games
    """)

    stats = {}

    for team, score in cursor.fetchall():

        if not score:
            continue

        try:
            result = score[0]
            numbers = score[1:]
            team_score, opp_score = numbers.split("-")
            team_score = int(team_score)
            opp_score = int(opp_score)
            margin = abs(team_score - opp_score)
            if result == "W":
                differential = margin
            else:
                differential = -margin
            if team not in stats:
                stats[team] = {
                    "total_diff": 0,
                    "games": 0
                }
            stats[team]["total_diff"] += differential
            stats[team]["games"] += 1

        except:
            continue

    rankings = []

    for team, data in stats.items():
        avg_diff = (
            data["total_diff"] / data["games"]
        )
        rankings.append((team, avg_diff))
    rankings.sort(key=lambda x: x[1], reverse=True)

    print("\n🏀 Average Point Differential")

    for i, (team, diff) in enumerate(rankings, start=1):
        print(f"{i}. {team} : {round(diff, 2)}")

    conn.close()

if __name__ == "__main__":
    home_vs_away_win_percentage()
    east_vs_west_win_percentage()
    overall_team_rankings()
    average_point_differential()