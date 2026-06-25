"""
This function performs feature engineering by transofrorming
raw game results into team statistics that cna be used. 
Some of the function aggregates include:

Win percentage, Home win percentage, Away win percentage
Average points scored, Average points allowed, average point diff

"""
from app.db import get_connection


def parse_score(score):
    """
    Converts:
        W120-110 -> ("W",120,110)
        L105-112 -> ("L",105,112)
    """

    if not score or len(score) < 4:
        return None

    try:
        result = score[0]
        scores = score[1:]

        team_score, opp_score = scores.split("-")

        return result, int(team_score), int(opp_score)

    except:
        return None



def build_team_features():

    conn = get_connection()
    cursor = conn.cursor()

    # get all games
    cursor.execute("""
        SELECT team, score, location
        FROM games
    """)

    games = cursor.fetchall()


    # store temporary stats
    stats = {}


    for team, score, location in games:

        parsed = parse_score(score)

        if not parsed:
            continue


        result, team_points, opp_points = parsed


        # create team entry if missing
        if team not in stats:
            stats[team] = {

                "games_played": 0,
                "wins": 0,
                "losses": 0,

                "home_wins": 0,
                "home_losses": 0,

                "away_wins": 0,
                "away_losses": 0,

                "points_for": 0,
                "points_against": 0
            }



        team_stats = stats[team]


        # overall
        team_stats["games_played"] += 1


        if result == "W":
            team_stats["wins"] += 1
        else:
            team_stats["losses"] += 1



        # location
        if location == "Home":

            if result == "W":
                team_stats["home_wins"] += 1
            else:
                team_stats["home_losses"] += 1


        elif location == "Away":

            if result == "W":
                team_stats["away_wins"] += 1
            else:
                team_stats["away_losses"] += 1



        # scoring
        team_stats["points_for"] += team_points
        team_stats["points_against"] += opp_points



    # remove previous feature data
    cursor.execute("""
        DELETE FROM team_stats
    """)



    # insert engineered features
    for team, data in stats.items():


        games_played = data["games_played"]

        home_games = (
            data["home_wins"] +
            data["home_losses"]
        )

        away_games = (
            data["away_wins"] +
            data["away_losses"]
        )


        win_pct = (
            data["wins"] / games_played
            if games_played else 0
        )


        home_win_pct = (
            data["home_wins"] / home_games
            if home_games else 0
        )


        away_win_pct = (
            data["away_wins"] / away_games
            if away_games else 0
        )


        avg_points_for = (
            data["points_for"] / games_played
        )


        avg_points_against = (
            data["points_against"] / games_played
        )


        avg_point_diff = (
            avg_points_for -
            avg_points_against
        )



        cursor.execute("""
        INSERT INTO team_stats
        (
            team_name,

            games_played,
            wins,
            losses,
            win_pct,

            home_wins,
            home_losses,
            home_win_pct,

            away_wins,
            away_losses,
            away_win_pct,

            points_for,
            points_against,

            avg_points_for,
            avg_points_against,

            avg_point_diff
        )

        VALUES
        (
            ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
        )

        """, (

            team,

            games_played,
            data["wins"],
            data["losses"],
            round(win_pct,3),

            data["home_wins"],
            data["home_losses"],
            round(home_win_pct,3),

            data["away_wins"],
            data["away_losses"],
            round(away_win_pct,3),

            data["points_for"],
            data["points_against"],

            round(avg_points_for,2),
            round(avg_points_against,2),

            round(avg_point_diff,2)

        ))


    conn.commit()
    conn.close()



if __name__ == "__main__":

    build_team_features()

    print("Team feature table created!")