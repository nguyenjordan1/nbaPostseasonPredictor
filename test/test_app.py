import sys
import os

from unittest.mock import patch, MagicMock

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from app.webapp import app

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

def test_health():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.data == b"I'm healthy"


def test_metrics():
    client = app.test_client()

    response = client.get("/metrics")

    assert response.status_code == 200

    data = response.get_json()

    assert "requests" in data
    assert "teams_loaded" in data

    from unittest.mock import patch, MagicMock


@patch("app.webapp.get_connection")
def test_home_page(mock_get_connection):

    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_get_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [
        (1, "Denver Nuggets"),
        (2, "Boston Celtics")
    ]

    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200

@patch("app.webapp.home_vs_away_win_percentage")
def test_api_home_away(mock_func):

    mock_func.return_value = {
        "home_wins": 60,
        "away_wins": 40
    }

    client = app.test_client()

    response = client.get("/api/home-away")

    assert response.status_code == 200

    data = response.get_json()

    assert data["home_wins"] == 60
    assert data["away_wins"] == 40