# app/app.py
from flask import Flask, request
from flask import Flask, request, jsonify

from app.metrics import metrics
from app.db import create_table
from app.collector import fetch_and_store

app = Flask(__name__)

@app.route("/")
def home():
    return '''
    <h2>Sports Predictor</h2>
    <form action="/echo" method="POST">
        <input name="msg">
        <button>Submit</button>
    </form>
    '''

@app.route("/echo", methods=["POST"])
def echo():
    msg = request.form.get("msg")
    return f"You said: {msg}"

@app.route("/load-data")
def load_data():
    create_table()
    fetch_and_store()
    fetch_games()
    metrics["teams_loaded"] = 30
    metrics["games_loaded"] = 2460
    return "Data loaded!"

@app.route("/health")
def health():
    return "I'm healthy"

@app.route("/metrics")
def get_metrics():

    metrics["requests"] += 1

    return jsonify(metrics)

if __name__ == "__main__":
    app.run(debug=True)