from app.db import create_table, create_games_table, create_team_stats_table
from app.collector import fetch_and_store
from app.schedule_collector import fetch_games
from app.feature_engineering.team_stats import build_team_features
from app.feature_engineering.elo import calculate_elo
from app.feature_engineering.recent_games import calculate_recent_form
from app.feature_engineering.strength_of_schedule import calculate_strength_of_schedule

# Run this once to scrape the data and store into the tables
# This should only be run once to initialize tables
def main():
    print("Creating tables...")
    create_table()
    create_games_table()
    create_team_stats_table()

    print("Fetching teams...")
    fetch_and_store()

    print("Fetching games...")
    fetch_games()

    print("DONE: Pipeline complete")

    print("Doing feature Engineering")

    print("Feature Engineering...")
    build_team_features()

    print("Calculating Elo...")
    calculate_elo()

    print("Calculating Recent Games...")
    calculate_recent_form()

    print("Calculating Stength of Schedule...")
    calculate_strength_of_schedule()


if __name__ == "__main__":
    main()