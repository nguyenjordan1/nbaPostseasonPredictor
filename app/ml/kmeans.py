from app.db import get_connection

import pandas as pd

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler



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



def run_kmeans():

    df = load_team_features()


    # keep names separate
    teams = df["team_name"]


    # ML features only
    X = df.drop(columns=["team_name"])



    # IMPORTANT:
    # Elo is ~1700
    # win pct is ~0.7
    #
    # Scaling puts them on equal footing

    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)



    # Try 4 groups
    kmeans = KMeans(
        n_clusters=4,
        random_state=42,
        n_init=10
    )


    clusters = kmeans.fit_predict(X_scaled)



    df["cluster"] = clusters



    return df



if __name__ == "__main__":

    results = run_kmeans()


    for cluster in sorted(results.cluster.unique()):

        print("\n")
        print("===================")
        print(f"Cluster {cluster}")
        print("===================")


        teams = results[
            results.cluster == cluster
        ]

        print(
            teams[
                [
                    "team_name",
                    "win_pct",
                    "elo_rating",
                    "recent_form",
                    "avg_point_diff"
                ]
            ]
        )

        print("\nCluster averages:")
        print(
            teams[
                [
                    "win_pct",
                    "elo_rating",
                    "recent_form",
                    "avg_point_diff"
                ]
            ].mean()
        )