import os

from cs50 import SQL

from flask import Flask, redirect, render_template, request, session, redirect, url_for
from flask_session import Session
from helpers import add_table, get_all_data, get_options, get_results, get_encounter

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///tables.db")

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/tables", methods=["GET", "POST"])
def tables():
    data = get_all_data()
    options = get_options()
    results = None
    rolled = 0

    if request.method == "POST":
        selectedTypes = request.form.getlist("checkbox-type")
        selectedActions = request.form.getlist("checkbox-action")
        rolled = request.form.get("dice")
        results = get_results(rolled, selectedTypes, selectedActions)

    return render_template("tables.html", data=data, options=options, rolled=rolled, results=results)

@app.route("/add_table", methods=["GET", "POST"])
def add():

    if request.method == "GET":
        return render_template("add_table.html")
    else:
        if 'file' not in request.files:
            return "No file part", 400

        file = request.files['file']

        if file.filename == '':
            return "No selected file", 400

        add_table(file)
        return redirect(url_for('tables'))

@app.route("/encounters", methods=["GET", "POST"])
def encounters():

    if request.method == "GET":
        return render_template("encounters.html", encounter=None)

    if request.method == "POST":
        party_level = int(request.form.get("party_level"))
        party_size = int(request.form.get("party_size"))
        difficulty = int(request.form.get("difficulty"))

        type = ""

        if difficulty == 1:
            type = "Easy"
        elif difficulty == 2:
            type = "Medium"
        elif difficulty == 3:
            type = "Hard"
        elif difficulty == 4:
            type = "Deadly"
        else:
            abort(500)

        encounter, total_xp = get_encounter(party_level, party_size, difficulty)

        return render_template("encounters.html", encounter=encounter, total_xp=total_xp, type=type)
