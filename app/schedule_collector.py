import requests
from bs4 import BeautifulSoup
from app.db import get_connection
from app.metrics import metrics

BASE_URL = "https://www.espn.com/nba/team/schedule/_/name/{}/seasontype/2"

# Normalize Names
TEAM_CODES = {
    "atl": "Atlanta Hawks",
    "bos": "Boston Celtics",
    "bkn": "Brooklyn Nets",
    "cha": "Charlotte Hornets",
    "chi": "Chicago Bulls",
    "cle": "Cleveland Cavaliers",
    "dal": "Dallas Mavericks",
    "den": "Denver Nuggets",
    "det": "Detroit Pistons",
    "gs": "Golden State Warriors",
    "hou": "Houston Rockets",
    "ind": "Indiana Pacers",
    "lac": "LA Clippers",
    "lal": "Los Angeles Lakers",
    "mem": "Memphis Grizzlies",
    "mia": "Miami Heat",
    "mil": "Milwaukee Bucks",
    "min": "Minnesota Timberwolves",
    "no": "New Orleans Pelicans",
    "ny": "New York Knicks",
    "okc": "Oklahoma City Thunder",
    "orl": "Orlando Magic",
    "phi": "Philadelphia 76ers",
    "phx": "Phoenix Suns",
    "por": "Portland Trail Blazers",
    "sac": "Sacramento Kings",
    "sa": "San Antonio Spurs",
    "tor": "Toronto Raptors",
    "uta": "Utah Jazz",
    "wsh": "Washington Wizards"
}

NAME_FIX = {
    "Toronto": "Toronto Raptors",
    "Boston": "Boston Celtics",
    "Los Angeles": "Los Angeles Lakers",
    "LA": "Los Angeles Lakers",
    "Golden State": "Golden State Warriors",
    "GS": "Golden State Warriors",
    "Brooklyn": "Brooklyn Nets",
    "Chicago": "Chicago Bulls",
    "Miami": "Miami Heat",
    "Denver": "Denver Nuggets",
    "Phoenix": "Phoenix Suns",
    "Utah": "Utah Jazz",
    "Dallas": "Dallas Mavericks",
    "Houston": "Houston Rockets",
    "Memphis": "Memphis Grizzlies",
    "Orlando": "Orlando Magic",
    "Atlanta": "Atlanta Hawks",
    "Milwaukee": "Milwaukee Bucks",
    "Indiana": "Indiana Pacers",
    "Detroit": "Detroit Pistons",
    "Cleveland": "Cleveland Cavaliers",
    "Philadelphia": "Philadelphia 76ers",
    "Portland": "Portland Trail Blazers",
    "Sacramento": "Sacramento Kings",
    "San Antonio": "San Antonio Spurs",
    "Washington": "Washington Wizards",
    "Minnesota": "Minnesota Timberwolves",
    "New Orleans": "New Orleans Pelicans",
    "Oklahoma City": "Oklahoma City Thunder",
    "Charlotte": "Charlotte Hornets",
    "New York": "New York Knicks"
}

def clean_opponent(raw):

    raw = raw.replace("@", "")
    raw = raw.replace("vs", "")
    raw = raw.replace("*", "")
    raw = raw.strip()

    return NAME_FIX.get(raw, raw)

# Get Locations of Games
# @raw
def get_location(raw):
    if "@" in raw:
        return "Away"
    elif "vs" in raw:
        return "Home"
    return "Unknown"

# Get Games
def fetch_games():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM games")
    
    game_count = 0

    headers = {"User-Agent": "Mozilla/5.0"}

    for code, team_name in TEAM_CODES.items():
        url = BASE_URL.format(code)

        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")

        rows = soup.select("tr.Table__TR")

        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 5:
                continue

            game_date = cols[0].text.strip()
            raw_opponent = cols[1].text.strip()
            score = cols[2].text.strip()

            opponent = clean_opponent(raw_opponent)
            location = get_location(raw_opponent)

            cursor.execute("""
                INSERT INTO games (team, opponent, game_date, score, location)
                VALUES (?, ?, ?, ?, ?)
            """, (team_name, opponent, game_date, score, location))
            game_count += 1

    metrics["games_loaded"] = game_count
    conn.commit()
    conn.close()