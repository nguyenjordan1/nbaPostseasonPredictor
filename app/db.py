import sqlite3
# These shoudl only be run once to initialize the tables and not run again

DB_NAME = "data.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

# Creates table for teams if it doesn't already exist
def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teams (
        id INTEGER PRIMARY KEY,
        name TEXT,
        conference TEXT
    )
    """)

    conn.commit()
    conn.close()

# Creates the games table if it doesnt already exist
def create_games_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS games (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        team TEXT,
        opponent TEXT,
        game_date TEXT,
        score TEXT,
        location TEXT
    )
    """)

    conn.commit()
    conn.close()