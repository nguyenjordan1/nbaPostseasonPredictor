from app.db import create_table, create_games_table
from app.collector import fetch_and_store
from app.schedule_collector import fetch_games

def main():
    create_table()
    create_games_table()

    fetch_and_store()   # teams
    fetch_games()       # games

    print("DONE")

if __name__ == "__main__":
    main()