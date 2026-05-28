from app.db import create_table, create_games_table
from app.collector import fetch_and_store
from app.schedule_collector import fetch_games

def main():
    print("Creating tables...")
    create_table()
    create_games_table()

    print("Fetching teams...")
    fetch_and_store()

    print("Fetching games...")
    fetch_games()

    print("DONE: Pipeline complete")

if __name__ == "__main__":
    main()