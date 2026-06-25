"""
This function calculates Elo ratings for teams.
It processes games in chronological order.

Every team starts with the same rating (1500) and
after each game the probability of winning is calculated
from difference in rating, teams gain mor points when
unexpectedly winning and vice versa, rating evolve 
throughout season

expected = 1 / (1 + 10^((opponent_elo - team_elo) / 400))

Updated on results:
new_elo = old_elo + K * (actual - expected)

actual = 1 (win), 0 (loss)
expected = predicted prob of winning 
K = max rating adjustment

The equation used comes from standard elo rating system 
developed by Arpad Elo for chess and is now used for analytics

"""


from app.db import get_connection

"""
parse scores to seperate W column, home score, and away score

@score - scorea unparsed 
return result, team_score, opp_score
"""
def parse_score(score):
    """
    W120-110 -> ("W",120,110)
    L105-112 -> ("L",105,112)
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

"""
This function calculates Elo ratings for every team based on historical data
"""
def calculate_elo():

    conn = get_connection()
    cursor = conn.cursor()

    # Get every game from the the games table and order chronologically by date
    cursor.execute("""
        SELECT team, opponent, game_date, score
        FROM games
        ORDER BY game_date
    """)

    games = cursor.fetchall()


    # Starting Elo
    elo = {}

    STARTING_ELO = 1500
    K = 32

    
    for team, opponent, date, score in games:

        parsed = parse_score(score)

        if not parsed:
            continue


        result, team_score, opp_score = parsed


        if team not in elo:
            elo[team] = STARTING_ELO

        if opponent not in elo:
            elo[opponent] = STARTING_ELO



        team_elo = elo[team]
        opp_elo = elo[opponent]


        # expected win probability
        expected_team = (
            1 /
            (1 + 10 ** ((opp_elo - team_elo) / 400))
        )


        if result == "W":
            actual = 1
        else:
            actual = 0



        # update ratings

        elo[team] = (
            team_elo +
            K * (actual - expected_team)
        )


        elo[opponent] = (
            opp_elo +
            K * ((1-actual) - (1-expected_team))
        )

    # store into team_stats
    for team, rating in elo.items():

        cursor.execute("""
            UPDATE team_stats
            SET elo_rating = ?
            WHERE team_name = ?
        """,
        (
            round(rating,2),
            team
        ))


    conn.commit()
    conn.close()


    print("Elo ratings updated")

if __name__ == "__main__":
    calculate_elo()