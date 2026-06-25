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

# Creates table for each team  
def create_team_stats_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS team_stats (

        team_name TEXT PRIMARY KEY,

        games_played INTEGER,
        wins INTEGER,
        losses INTEGER,
        win_pct REAL,

        home_wins INTEGER,
        home_losses INTEGER,
        home_win_pct REAL,

        away_wins INTEGER,
        away_losses INTEGER,
        away_win_pct REAL,

        points_for INTEGER,
        points_against INTEGER,

        avg_points_for REAL,
        avg_points_against REAL,

        avg_point_diff REAL,
        elo_rating REAL,
        
        recent_wins INTEGER,
        recent_games INTEGER,
        recent_form REAL,
                   
        strength_of_schedule REAL
    )
    """)

    conn.commit()
    conn.close()