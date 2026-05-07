import requests
from bs4 import BeautifulSoup
from app.db import get_connection

BASE_URL = "https://www.espn.com/nba/team/schedule/_/name/{}/seasontype/2"

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

def fetch_games():
    conn = get_connection()
    cursor = conn.cursor()

    for code, team_name in TEAM_CODES.items():
        url = BASE_URL.format(code)

        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")

        rows = soup.select("tr.Table__TR")

        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 5:
                continue

            game_date = cols[0].text.strip()
            opponent = cols[1].text.strip()
            score = cols[2].text.strip()

            cursor.execute("""
                INSERT INTO games (team, opponent, game_date, score)
                VALUES (?, ?, ?, ?)
            """, (team_name, opponent, game_date, score))

    conn.commit()
    conn.close()