#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from sqlalchemy import func

from models import db, Earthquake  # Import the Earthquake model

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# New route to get an earthquake by ID
@app.route('/earthquakes/<int:id>')
def get_earthquake(id):
    earthquake = Earthquake.query.get(id)  # Use .get() for by-primary-key lookup

    if earthquake:
        results = {
            "id": earthquake.id,
            "magnitude": earthquake.magnitude,
            "location": earthquake.location,
            "year": earthquake.year
        }
        return jsonify(results), 200  # Explicit 200 OK status
    else:
        return jsonify({"message": f"Earthquake {id} not found."}), 404  # Explicit 404 Not Found status

# New route to get earthquakes by magnitude
@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()

    results = [
        {
            "id": quake.id,
            "magnitude": quake.magnitude,
            "location": quake.location,
            "year": quake.year
        } for quake in earthquakes
    ]
    count = len(results)  # Get the count

    return jsonify({"count": count, "quakes": results}), 200
