from app.db import get_connection
import networkx as nx


# Load all games from the database
def load_games():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            team,
            opponent,
            score
        FROM games
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows


# Build a directed graph
# Loser -> Winner
# Multiple wins increase edge weight
def build_graph():

    games = load_games()
    G = nx.DiGraph()

    for team, opponent, score in games:
        if score.startswith("W"):
            winner = team
            loser = opponent
        elif score.startswith("L"):
            winner = opponent
            loser = team
        else:
            continue

        # Add weight for repeated wins
        if G.has_edge(loser, winner):
            G[loser][winner]["weight"] += 1
        else:
            G.add_edge(loser, winner, weight=1)
    return G


# Calculate PageRank scores
def calculate_pagerank():

    G = build_graph()

    rankings = nx.pagerank(
        G,
        weight="weight"
    )

    rankings = sorted(
        rankings.items(),
        key=lambda x: x[1],
        reverse=True
    )
    return rankings


if __name__ == "__main__":

    rankings = calculate_pagerank()

    print("\n===================")
    print("NBA PageRank")
    print("===================\n")

    for team, score in rankings:
        print(f"{team:30} {score:.4f}")