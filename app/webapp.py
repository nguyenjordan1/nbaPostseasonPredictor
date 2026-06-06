from flask import Flask, request, jsonify, render_template
from app.metrics import metrics
from app.db import create_table, get_connection
from app.collector import fetch_and_store
from app.schedule_collector import fetch_games
import os

# imports functions from analyzer 
from app.analyzer import (
    home_vs_away_win_percentage,
    east_vs_west_win_percentage,
    overall_team_rankings,
    average_point_differential
)

# Using flask 
app = Flask(
    __name__,
    template_folder=os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "templates"
    ),
    static_folder=os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "static"
    )
)

# teams route for each team
@app.route("/team/<int:team_id>")
def team_page(team_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM teams
        WHERE id = ?
    """, (team_id,))

    team = cursor.fetchone()[0]

    cursor.execute("""
        SELECT *
        FROM games
        WHERE team = ?
    """, (team,))

    games = cursor.fetchall()

    conn.close()

    return render_template(
        "team.html",
        team=team,
        games=games
    )

# Home page 
@app.route("/")
def home():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name
        FROM teams
        ORDER BY name
    """)

    teams = cursor.fetchall()

    conn.close()

    return render_template(
        "index.html",
        teams=teams
    )

# analyzer functions
# returns the results of the runctions in a JSON
@app.route("/api/home-away")
def api_home_away():
    return jsonify(home_vs_away_win_percentage())
@app.route("/api/east-west")
def api_east_west():
    return jsonify(east_vs_west_win_percentage())
@app.route("/api/rankings")
def api_rankings():
    return jsonify(overall_team_rankings())
@app.route("/api/differential")
def api_differential():
    return jsonify(average_point_differential())

# Load data....
# I don't think I use this
@app.route("/load-data")
def load_data():

    create_table()
    fetch_and_store()
    fetch_games()

    metrics["teams_loaded"] = 30

    return "Data loaded!"

# Health
@app.route("/health")
def health():
    return "I'm healthy"

# Metrics
@app.route("/metrics")
def get_metrics():

    metrics["requests"] += 1

    return jsonify(metrics)


if __name__ == "__main__":
    app.run(debug=True)