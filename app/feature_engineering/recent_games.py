"""
This fucntion calculates the teams current play based on the 
last 10 games. Each team computes win percentage, and stores
in the team_stats table. Just shows how the team has been doing
recently.

recent_form = wins / recent_games

wins = number of wins in last 10 games
recent_games = number of games (10)

"""

from app.db import get_connection


def calculate_recent_form():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT team, score
        FROM games
    """)

    rows = cursor.fetchall()

    team_games = {}

    for team, score in rows:

        if team not in team_games:
            team_games[team] = []

        team_games[team].append(score)

    for team, scores in team_games.items():

        last_10 = scores[-10:]

        wins = 0

        for score in last_10:

            if score.startswith("W"):
                wins += 1

        recent_games = len(last_10)

        recent_form = (
            wins / recent_games
            if recent_games else 0
        )

        cursor.execute("""
            UPDATE team_stats
            SET
                recent_wins = ?,
                recent_games = ?,
                recent_form = ?
            WHERE team_name = ?
        """,
        (
            wins,
            recent_games,
            round(recent_form, 3),
            team
        ))

    conn.commit()
    conn.close()

    print("Recent form updated")


if __name__ == "__main__":
    calculate_recent_form()