from app.db import get_connection

import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity



def load_team_features():

    conn = get_connection()

    query = """
    SELECT

        t.id,

        ts.team_name,

        ts.win_pct,
        ts.home_win_pct,
        ts.away_win_pct,

        ts.avg_points_for,
        ts.avg_points_against,
        ts.avg_point_diff,

        ts.elo_rating,

        ts.recent_form,
        ts.strength_of_schedule

    FROM team_stats ts
    JOIN teams t
    ON ts.team_name = t.name
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df



def find_similar_teams(team_name, count=5):

    df = load_team_features()


    names = df["team_name"]


    X = df.drop(columns=["id", "team_name"])



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

        if index == team_index:
            continue
        team = df.iloc[index]
        results.append({
            "id": team["id"],
            "team": team["team_name"],
            "similarity": round(score, 3),
            "win_pct": team["win_pct"],
            "elo_rating": team["elo_rating"],
            "recent_form": team["recent_form"],
            "avg_point_diff": team["avg_point_diff"]
        })

        if len(results) == count:
            break

    return results

if __name__ == "__main__":

    team = "Denver Nuggets"
    print(
        f"Teams similar to {team}"
    )
    results = find_similar_teams(team)

    for team in results:
        print(
            team["team"],
            team["similarity"]
        )