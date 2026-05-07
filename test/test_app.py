import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.webapp import app

def test_home_page():
    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert b"Sports Predictor" in response.data


def test_echo():
    client = app.test_client()
    response = client.post("/echo", data={"msg": "hello"})

    assert response.status_code == 200
    assert b"You said: hello" in response.data