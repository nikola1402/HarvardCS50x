import requests

from cs50 import SQL
from flask import redirect, render_template, session, jsonify
from functools import wraps
import json
import math, random

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///tables.db")

def add_table(file):
    # Load the JSON file
    data = json.load(file)

    for entry in data:
        # Insert data into the SQLite table
       db.execute("INSERT INTO hit_fumble (type, action, min, max, description, effect) VALUES ( ?, ?, ?, ?, ?, ?)",
               entry['type'], entry['action'], entry['rollMin'], entry['rollMax'], entry['description'], entry['effect'])

def get_all_data():
    return db.execute("SELECT * FROM hit_fumble")

def get_options():
    types = db.execute("SELECT DISTINCT type FROM hit_fumble")
    actions = db.execute("SELECT DISTINCT action FROM hit_fumble")
    return types + actions

def get_results(rolled, selectedTypes, selectedActions):
    query = "SELECT * FROM hit_fumble WHERE ? BETWEEN min AND max"

    # Adjust query if there are any types selected
    if len(selectedTypes) > 0:
        query = query + " AND ("

        for index, type in enumerate(selectedTypes):
            query = query + "type = '" + type + "'"
            if index < len(selectedTypes)-1:
                query = query + " OR "

        query = query + ")"

    # Adjust query if there are any actions selected
    if len(selectedActions) > 0:
        query = query + " AND ("

        for index, action in enumerate(selectedActions):
            query = query + "action = '" + action + "'"
            if index < len(selectedActions)-1:
                query = query + " OR "

        query = query + ")"

    results = db.execute(query, rolled)
    return results

# Key contains monster CR, value contains base XP for that CR
MONSTER_CR = {
    0: 10,
    1/8: 25,
    1/4: 50,
    1/2: 100,
    1: 200,
    2: 450,
    3: 700,
    4: 1100,
    5: 1800,
    6: 2300
}

# Multipliers based on number of monsters
MULTIPLIERS = {
    1: 1,
    2: 1.5,
    3: 2,
    7: 2.5,
    11: 3,
    15: 4
}


def get_encounter(party_level, party_size, difficulty):
    xp_threshold = calculate_xp_threshold(party_level, party_size, difficulty)
    cr_to_fight = calculate_number_of_monsters(xp_threshold)
    monsters = get_monsters(cr_to_fight)
    monsters_per_cr = filter_monsters(monsters, cr_to_fight)
    encounter, total_xp = generate_encounter(monsters_per_cr, cr_to_fight, xp_threshold)
    return encounter, total_xp

def generate_encounter(monsters_per_cr, cr_to_fight, xp_threshold):

    encounter = []
    cr_list = []
    for cr, number in cr_to_fight.items():
        if number > 0:
            cr_list.append(float(cr))

    cr_list.sort()

    new_threshold = 0

    # Add 1 strongest CR monster
    monster = random.choice(monsters_per_cr[cr_list[len(cr_list)-1]])
    encounter.append(monster)
    total_xp = MONSTER_CR[cr_list[len(cr_list)-1]]

    # Keep adding monsters of different CR until we reach the threshold
    for i in range(0, 10):

        if i > len(cr_list)-1:
            i = 0

        cr = cr_list[i]
        monsters = monsters_per_cr[cr]
        monster = random.choice(monsters)
        monster_xp = MONSTER_CR[cr]
        num_monsters = len(encounter)
        multiplier = get_multiplier(num_monsters)
        new_threshold = math.ceil(xp_threshold / multiplier)

        new_xp = total_xp + monster_xp

        if new_xp > new_threshold:
            break

        total_xp = new_xp
        encounter.append(monster)

    return encounter, total_xp

def get_monsters(cr_to_fight):

    # Get highest and lowest CR which contains mosnters
    cr_list = []
    for cr, number in cr_to_fight.items():
        if number > 0:
            cr_list.append(float(cr))

    # Get monsters in the CR range
    monsters = get_monsters_by_cr(cr_list)
    return monsters

def filter_monsters(monsters, cr_to_fight):

    monsters_per_cr = {}

    for cr,number in cr_to_fight.items():
        monster_list = [monster for monster in monsters if monster.get("cr") == float(cr)]
        monsters_per_cr[cr] = monster_list

    return monsters_per_cr

def get_monsters_by_cr(cr_list):

    lowest_cr = min(cr_list)
    highest_cr = max(cr_list)
    url = f"https://api.open5e.com/monsters/?limit=250&cr__range=" + str(lowest_cr) + "%2C" + str(highest_cr)

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data["results"]
    except requests.RequestException as e:
        return jsonify({"error": str(e)})

def get_multiplier(num_monsters):
    # set highest value as default
    multiplier = 4

    for key, value in MULTIPLIERS.items():
        if num_monsters >= key:
            multiplier = value

    return multiplier

def calculate_number_of_monsters(xp_threshold):
    cr_to_fight = {}

    for cr, base_xp in MONSTER_CR.items():
        max = 0

        for num_monsters in range(1, 10):
            multiplier = get_multiplier(num_monsters)
            new_threshold = math.ceil(xp_threshold / multiplier)
            new_xp = num_monsters * base_xp

            if new_xp > new_threshold:
                break

            max = num_monsters

        if max > 0:
            cr_to_fight[cr] = max

    cr_to_fight = dict(sorted(cr_to_fight.items(), key=lambda item: item[0]))
    return cr_to_fight

def calculate_xp_threshold(party_level, party_size, difficulty):
    base_xp = 25
    char_threshold = base_xp * party_level * difficulty
    xp_threshold = char_threshold * party_size
    return xp_threshold
