from app.db import get_connection

import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA


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



def get_kmeans_visualization():

    df = load_team_features()

    # Keep names separate
    teams = df["team_name"]

    # Features only
    X = df.drop(columns=["team_name"])


    # Normalize features
    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)


    # Run KMeans
    kmeans = KMeans(
        n_clusters=4,
        random_state=42,
        n_init=10
    )

    clusters = kmeans.fit_predict(X_scaled)


    # PCA reduction to 2 dimensions
    pca = PCA(
        n_components=2
    )

    components = pca.fit_transform(X_scaled)


    results = []


    for i, team in enumerate(teams):

        results.append({

            "team": team,

            # PCA coordinates
            "x": round(float(components[i][0]), 3),
            "y": round(float(components[i][1]), 3),

            # cluster assignment
            "cluster": int(clusters[i]),


            # original features for hover
            "win_pct": float(df.iloc[i]["win_pct"]),

            "elo_rating": float(df.iloc[i]["elo_rating"]),

            "recent_form": float(df.iloc[i]["recent_form"]),

            "avg_point_diff": float(df.iloc[i]["avg_point_diff"])

        })


    return results



if __name__ == "__main__":

    results = get_kmeans_visualization()


    print("\n===================")
    print("K-Means Visualization Data")
    print("===================\n")


    for team in results:

        print(
            f"{team['team']:30} "
            f"x={team['x']:7} "
            f"y={team['y']:7} "
            f"cluster={team['cluster']}"
        )