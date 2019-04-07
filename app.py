 
import datetime as dt
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

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

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to Hawaii, where the weather is great and the waves are perfect!<br/><br/>"
        f"Is it raining in Hawaii? "
        f"/api/v1.0/precipitation<br/><br/>"
        f"Let's find the local weather stations on the island? "
        f"/api/v1.0/stations<br/><br/>"
        f"I want to go to the beach, what's the temperature like? "
        f"/api/v1.0/tobs<br/><br/>"
        f"My Hawaii vacation is almost here! What should I expect?<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

#################################################

# Precipitation api
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of all precipitation"""
    # query the date and precipitation from the table "measurement" for the past year
    querydt = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date.between('2016-08-23', '2017-08-23'))

    # Convert the query results to a Dictionary using date as the key and prcp as the value.
    precipitation = []
    for preci in querydt:
        preci_dict = {}
        preci_dict["Date"] = preci.date
        preci_dict["Precipitation"] = preci.prcp
        precipitation.append(preci_dict)
        
    # Return the JSON representation of your dictionary.
    return jsonify(precipitation)

#################################################

# Stations api
@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all stations and their names"""
    # query the stations table
    querystation = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation)

    # Convert the query results to a Dictionary using station as the key and name as the value.
    stations = []
    for st in querystation:
        st_dict = {}
        st_dict["Station"] = st.station
        st_dict["Name"] = st.name
        st_dict["Latitude"] = st.latitude
        st_dict["Longitude"] = st.longitude
        st_dict["Elevation"] = st.elevation
        stations.append(st_dict)
        
    # Return the JSON representation of your dictionary.
    return jsonify(stations)

#################################################

# Temperatures api
@app.route("/api/v1.0/tobs")
def temperatures():
    """Return a list of all temperatures"""
    # query the date and temperatures from the table "measurement" for the past year
    querytobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date.between('2016-08-23', '2017-08-23'))

    # query for the dates and temperature observations from a year from the last data point.
    temperatures = []
    for temp in querytobs:
        temp_dict = {}
        temp_dict["Date"] = temp.date
        temp_dict["Temperature"] = temp.tobs
        temperatures.append(temp_dict)
        
    # Return a JSON list of Temperature Observations (tobs) for the previous year.
    return jsonify(temperatures)

#################################################

# Average Temperatures api with start date only
@app.route("/api/v1.0/<start>")
def start(start):
    """Return a list of all tmin, tavg, tmax temperatures with a start date only"""

    trip_avg_temp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= '2016-02-28')

    # When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    avgtemp = []
    for tmin, tavg, tmax in trip_avg_temp:
        av_dict = {}
        av_dict["Lowest Temperature"] = tmin
        av_dict["Average Temperature"] = tavg
        av_dict["Highest Temperature"] = tmax
        avgtemp.append(av_dict)

    # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start range.
    return jsonify(avgtemp)

#################################################

# Average Temperatures api with a start and end dates
@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):
    """Return a list of all tmin, tavg, tmax temperatures with a start date only"""

    start = '2016-02-28'
    end = '2016-03-05'

    trip_temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end)

    # When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
    trip_start_end = []
    for tmin, tavg, tmax in trip_temps:
        tse_dict = {}
        tse_dict["Lowest Temperature"] = tmin
        tse_dict["Average Temperature"] = tavg
        tse_dict["Highest Temperature"] = tmax
        trip_start_end.append(tse_dict)

    # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start-end range.
    return jsonify(trip_start_end)

#################################################
if __name__ == '__main__':
    app.run(debug=True)
