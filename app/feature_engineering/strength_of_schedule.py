"""
This funcion calculates a teams strength of schedule by measuring
the average win percentage of all opponents faced during the season
If a team has a higher strength of scheule then it plays stronger
opponents

strength_of_schedule = (sum of opp win %) / (number of opp)

opp win % = opp wins / opp games
strength_of_schedule = average win percentage
"""
from app.db import get_connection


def calculate_strength_of_schedule():

    conn = get_connection()
    cursor = conn.cursor()

    # Get every team's win %
    cursor.execute("""
        SELECT team_name, win_pct
        FROM team_stats
    """)

    win_pcts = {
        team: win_pct
        for team, win_pct in cursor.fetchall()
    }

    # Get schedule data
    cursor.execute("""
        SELECT team, opponent
        FROM games
    """)

    games = cursor.fetchall()

    opponents = {}

    for team, opponent in games:

        if team not in opponents:
            opponents[team] = []

        if opponent in win_pcts:
            opponents[team].append(win_pcts[opponent])

    # Calculate average opponent win %
    for team, opp_win_pcts in opponents.items():

        if len(opp_win_pcts) == 0:
            sos = 0
        else:
            sos = sum(opp_win_pcts) / len(opp_win_pcts)

        cursor.execute("""
            UPDATE team_stats
            SET strength_of_schedule = ?
            WHERE team_name = ?
        """,
        (
            round(sos, 3),
            team
        ))

    conn.commit()
    conn.close()

    print("Strength of schedule updated")


if __name__ == "__main__":
    calculate_strength_of_schedule()