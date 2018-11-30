import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement 
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

def convertToDict(query_result, label):
    data = []
    for record in query_result:
        data.append({'date': record[0], label: record[1]})
    return data

def mostRecentDate():
    recentDate = session.query(Measurement).order_by(Measurement.date.desc()).limit(1)
    for date in recentDate:
        mostRecent = date.date
    return dt.datetime.strptime(mostRecent, "%Y-%m-%d")

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"Enter Start Date in format below:<br/>"
        f"/api/v1.0/yyyy-mm-dd/<br/>"
        f"Enter Start Date and End Date in format below:<br/>"
        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd/<br/>"
    )

@app.route('/api/v1.0/precipitation')
def return_precipitation():
    mostRecent = mostRecent2()
    oneYearAgo = mostRecent -dt.timedelta(days=365)

    RecentPrecipData = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= oneYearAgo).\
        order_by(Measurement.date).all()
    return jsonify(convertToDict(RecentPrecipData, label='prcp'))

@app.route('/api/v1.0/stations')
def return_stations():
    stationList = session.query(Measurement.station).distinct()

    return jsonify([station[0] for station in stationList])

@app.route('/api/v1.0/tobs')
def return_tobs():
    mostRecent = mostRecent2()
    oneYearAgo = mostRecent - dt.timedelta(days=365)
    recent_tobs = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= oneYearAgo).\
        order_by(Measurement.date).all()
    return jsonify(convertToDict(recent_tobs, label='tobs'))

#@app.route('/api/v1.0/<date>')
#def givenDate(date):


if __name__ == '__main__':
    app.run(debug=True)