import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
# from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

TEMPLATES_AUTO_RELOAD=True


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
    airlines_dict["Total_Number_of_Planes"] = all_planes
    airlines_dict["Total_Number_of_Fligths"] = all_flights
    airlines_dict["Delayed_Flights_(%)"] = delay_pct
    airlines_dict["Ontime_Flights_(%)"] = ontime_pct
    airlines_dict["Diverted_Flights_(%)"] = diverted_pct
    airlines_dict["Cancelled_Flights_(%)"] = cancelled_pct
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
    airlines_dict["Total_Number_of_Flights"] = flight_num
    airlines_dict["Observed_delay_flights(%)"] = pct
    airlines_dict["Total_arrival_Delay"] = total_delay
    airlines_dict["Avg_arrival_delay"] = avg_delay

    session.close()
    return jsonify(airlines_dict)

@app.route("/delayReasons/<airline>")
def get_delay_reasons(airline):

    results = session.query(delay_data).all()
    flights_num = []
    for a in results:
        if a.AIRLINE_NAME == airline:
            flights_num.append(a.CARRIER_DELAY)
            flights_num.append(a.WEATHER_DELAY)
            flights_num.append(a.NAS_DELAY)
            flights_num.append(a.SECURITY_DELAY)
            flights_num.append(a.LATE_AIRCRAFT_DELAY)
        if airline == "total":
            flights_num = [362343,56652,434559,2397,523166]


    airlines_dict = {}
    airlines_dict["delayFlightsNum"] = flights_num
    airlines_dict["delayType"] = ["Carrier_delay","Weather_delay","NAS_delay","Security_delay","Late_aircraft_delay"]
    session.close()
    return jsonify(airlines_dict)

@app.route("/cancelReasons")
def get_cancelled_reasons():
    results = []
    for row in session.query(cancelled_data).all():
        results.append({'Airline': row.AIRLINE_NAME, 'Total Number of Cancelled Flights':row.FLIGHT_NUMBER,
                        'Carrier cancel': row.CARRIER,'Weather Cancel':row.WEATHER,
                        'National air system cancel':row.NATIONAL_AIR_SYSTEM,'Security cancel':row.SECURITY})

    session.close()
    return jsonify(results)

@app.route("/delaySearch/<airline>/<destAirport>/<originAirport>/<month>")
def get_filter_data(airline,destAirport,originAirport,month):
    sel = [
        grouped_data.AIRLINE_NAME,
        grouped_data.DEST_AIRPORT_Name,
        grouped_data.ORIGIN_AIRPORT_Name,
        grouped_data.MONTH,
        grouped_data.PERFORMANCE,
        grouped_data.TOTAL_FLIGHTS_NUMBER,
    ]
    results = db.session.query(*sel).filter(grouped_data.AIRLINE_NAME == airline )\
                                        .filter(grouped_data.DEST_AIRPORT_Name == destAirport)\
                                        .filter(grouped_data.ORIGIN_AIRPORT_Name == originAirport )\
                                        .filter(grouped_data.MONTH == month).all()

    data = []
    for result in results:
        data.append({'Performance': result.PERFORMANCE, 'TotalFlights':result.TOTAL_FLIGHTS_NUMBER})

    session.close()
    return jsonify(data)

@app.route("/airport")
def get_airport_name():
    results = []
    for row in session.query(airport_data).all():
        results.append({'Airport': row.ORIGIN_AIRPORT, 'FullName':row.AIRPORT})
    session.close()
    return jsonify(results)

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    search = request.args.get('q')
    query = session.query(airport_data.AIRPORT).filter(airport_data.AIRPORT.like('%' + str(search) + '%'))
    results = [mv[0] for mv in query.all()]
    session.close()
    return jsonify(matching_results=results) 

    
if __name__ == "__main__":
    app.run(debug=True)


 
