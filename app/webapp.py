# app/app.py
from flask import Flask, request

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
    return "ESPN NBA teams scraped and stored!"