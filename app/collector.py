import requests
from bs4 import BeautifulSoup
from app.db import get_connection

URL = "https://www.espn.com/nba/teams"

def fetch_and_store():

    # fake normal user id so espn dont block me lol
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM teams")

    teams = soup.select("h2.di.clr-gray-01.h5")

    # print("DEBUG TEAMS:", teams)

    for i, team in enumerate(teams):
        name = team.text.strip()

        if name:
            cursor.execute(
                "INSERT OR REPLACE INTO teams (id, name) VALUES (?, ?)",
                (i, name)
            )

    conn.commit()
    conn.close()