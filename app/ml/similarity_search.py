from app.db import get_connection

import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity



def load_team_features():

    conn = get_connection()

    query = """
    SELECT

        team_name,

        win_pct,
        home_win_pct,
        away_win_pct,

        avg_points_for,
        avg_points_against,
        avg_point_diff,

        elo_rating,

        recent_form,
        strength_of_schedule

    FROM team_stats
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df



def find_similar_teams(team_name, count=5):

    df = load_team_features()


    names = df["team_name"]


    X = df.drop(columns=["team_name"])



    # scale features
    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)



    # cosine similarity matrix

    similarity = cosine_similarity(X_scaled)



    # find requested team index

    team_index = (
        df.index[
            df["team_name"] == team_name
        ][0]
    )


    scores = list(
        enumerate(similarity[team_index])
    )


    # highest first
    scores = sorted(
        scores,
        key=lambda x: x[1],
        reverse=True
    )


    results = []


    for index, score in scores:

        # skip itself
        if index == team_index:
            continue
        
        results.append(
            (
                names[index],
                round(score,3)
            )
        )

        if len(results) == count:
            break


    return results



if __name__ == "__main__":

    team = "Denver Nuggets"
    print(
        f"Teams similar to {team}"
    )
    results = find_similar_teams(team)

    for name, score in results:

        print(
            name,
            score
        )