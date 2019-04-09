import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
# from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#################################################
# Database Setup
#################################################

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/flightsCal.db"
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
flight_data = Base.classes.FlightTable
ariline_names = Base.classes.AirlinesTable
ontime_data = Base.classes.OntimeTable
delay_data = Base.classes.DelayTable
cancelled_data = Base.classes.CancelTable
grouped_data =  Base.classes.GroupedFlightData
airport_data = Base.classes.AirportTable

# Create our session (link) from Python to the DB
session = Session(db.engine)

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/airlineData")
def get_airlines():
    # Query all Airlines
    # results = session.query(flight_data).filter_by(AIRLINE="AA").all()
    results = session.query(flight_data).all()

    all_airlines = []
    all_flights = []
    all_planes = []
    delay_pct = []
    ontime_pct = []
    diverted_pct = []
    cancelled_pct = []

    for a in results:
        all_airlines.append(a.AIRLINE_NAME)
        all_flights.append(a.ROW_COUNT)
        all_planes.append(a.PLANE_COUNT)
        delay_pct.append(a.DELAY_PCT)
        ontime_pct.append(a.ONTIME_PCT)
        diverted_pct.append(a.DIVERTED_PCT)
        cancelled_pct.append(a.CANCELLED_PCT)

        
    airlines_dict = {}
    airlines_dict["Airline"] = all_airlines
    airlines_dict["Total Number of Planes"] = all_planes
    airlines_dict["Total Number of Fligths"] = all_flights
    airlines_dict["Delayed Flights (%)"] = delay_pct
    airlines_dict["Ontime Flights (%)"] = ontime_pct
    airlines_dict["Diverted Flights (%)"] = diverted_pct
    airlines_dict["Cancelled Flights (%)"] = cancelled_pct
    session.close()
    return jsonify(airlines_dict)

@app.route("/airlineName")
def get_airlines_names():
    results = session.query(ariline_names.AIRLINE_NAME).all()
    flattened_results =  [val for sublist in results for val in sublist]
    session.close()
    return jsonify(flattened_results)

@app.route("/ontimeFlights")
def get_ontime_flights():
    results = session.query(ontime_data).all()

    all_airlines = []
    flight_num = []
    pct = []

    for a in results:
        all_airlines.append(a.AIRLINE_NAME)
        flight_num.append(a.FLIGHT_NUMBER)
        pct.append(a.PERCENTAGE)
        
    airlines_dict = {}
    airlines_dict["Airline"] = all_airlines
    airlines_dict["Total Number of Flights"] = flight_num
    airlines_dict["Observed Ontime flights(%)"] = pct

    session.close()
    return jsonify(airlines_dict)

@app.route("/delayFlights")
def get_delay_flights():
    results = session.query(delay_data).all()

    all_airlines = []
    flight_num = []
    pct = []
    total_delay = []
    avg_delay = []

    for a in results:
        all_airlines.append(a.AIRLINE_NAME)
        flight_num.append(a.FLIGHT_NUMBER)
        pct.append(a.PERCENTAGE)
        total_delay.append(a.ARR_DELAY)
        avg_delay.append(a.AVG_MIN_DELAY)
        
    airlines_dict = {}
    airlines_dict["Airline"] = all_airlines
    airlines_dict["Total Number of Flights"] = flight_num
    airlines_dict["Observed delay flights(%)"] = pct
    airlines_dict["Total arrival Delay (min)"] = total_delay
    airlines_dict["Avg arrival delay (min)"] = avg_delay

    session.close()
    return jsonify(airlines_dict)

@app.route("/delayReasons")
def get_delay_reasons():
    results = []
    for row in session.query(delay_data).all():
        results.append({'Airline': row.AIRLINE, 'Total Number of Cancelled Flights':row.FLIGHT_NUMBER,
                        'Carrier delay': row.CARRIER_DELAY,'Weather delay':row.WEATHER_DELAY,
                        'NAS delay':row.NAS_DELAY,'Security delay':row.SECURITY_DELAY,
                        'Late aircraft delay': row.LATE_AIRCRAFT_DELAY})

    session.close()
    return jsonify(results)

@app.route("/cancelReasons")
def get_cancelled_reasons():
    results = []
    for row in session.query(cancelled_data).all():
        results.append({'Airline': row.AIRLINE_NAME, 'Total Number of Cancelled Flights':row.FLIGHT_NUMBER,
                        'Carrier cancel': row.CARRIER,'Weather Cancel':row.WEATHER,
                        'National air system cancel':row.NATIONAL_AIR_SYSTEM,'Security cancel':row.SECURITY})

    session.close()
    return jsonify(results)

@app.route("/delaySearch")
def get_grouped_data():
    results = []
    for row in session.query(grouped_data).all():
        results.append({'Airline': row.AIRLINE_NAME, 'Performance':row.PERFORMANCE,
                        'Month': row.MONTH,'Origin_Airport':row.ORIGIN_AIRPORT,
                        'Dest_Airport':row.DEST_AIRPORT,'TotalFlights':row.TOTAL_FLIGHTS_NUMBER})

    session.close()
    return jsonify(results)

@app.route("/airport")
def get_airport_name():
    results = []
    for row in session.query(airport_data).all():
        results.append({'Airport': row.ORIGIN_AIRPORT, 'FullName':row.AIRPORT})
    session.close()
    return jsonify(results)

    
if __name__ == "__main__":
    app.run(debug=True)


 