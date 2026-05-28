import requests
from bs4 import BeautifulSoup
from app.db import get_connection


URL = "https://www.espn.com/nba/teams"

# Conference mapping
EAST_TEAMS = {
    "Boston Celtics", "Brooklyn Nets", "New York Knicks",
    "Philadelphia 76ers", "Toronto Raptors", "Chicago Bulls",
    "Cleveland Cavaliers", "Detroit Pistons", "Indiana Pacers",
    "Milwaukee Bucks", "Atlanta Hawks", "Charlotte Hornets",
    "Miami Heat", "Orlando Magic", "Washington Wizards"
}

WEST_TEAMS = {
    "Dallas Mavericks", "Denver Nuggets", "Golden State Warriors",
    "Houston Rockets", "LA Clippers", "Los Angeles Lakers",
    "Memphis Grizzlies", "Minnesota Timberwolves", "New Orleans Pelicans",
    "Oklahoma City Thunder", "Phoenix Suns", "Portland Trail Blazers",
    "Sacramento Kings", "San Antonio Spurs", "Utah Jazz"
}

# normalizing names
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


def get_conference(name):
    if name in EAST_TEAMS:
        return "East"
    elif name in WEST_TEAMS:
        return "West"
    return "Unknown"

# Get teams and store in teams table 
def fetch_and_store():

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM teams")

    teams = soup.select("h2.di.clr-gray-01.h5")

    for i, team in enumerate(teams):
        raw_name = team.text.strip()

        if not raw_name:
            continue

        name = NAME_FIX.get(raw_name, raw_name)
        conference = get_conference(name)

        cursor.execute(
            "INSERT OR REPLACE INTO teams (id, name, conference) VALUES (?, ?, ?)",
            (i, name, conference)
        )

    conn.commit()
    conn.close()