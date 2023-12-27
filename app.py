# Import the dependencies.
import numpy as np
import requests
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, request


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement=Base.classes.measurement
station=Base.classes.station

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
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Perform a query to retrieve the dates and precipitation 
    # measurements from the last 12 months
    results=session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= '2016-08-23').all()

    session.close()

    # Create a dictionary from the row data and append to a 
    # list of all_dates
    all_dates = []
    for date, prcp in results:
        measurement_dict = {}
        measurement_dict["date"] = date
        measurement_dict["prcp"] = prcp
        all_dates.append(measurement_dict)

    return jsonify(all_dates)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query all stations
    results = session.query(station.station).all()

    session.close()

    # Convert list of tuples into normal list
    station_names = list(np.ravel(results))

    return jsonify(station_names)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Perform a query of the most active station for temperature 
    # observations from the last 12 months
    results=session.query(measurement.tobs).\
            filter(measurement.station == 'USC00519281').\
            filter(measurement.date >= '2016-08-23').all()

    session.close()

    # Convert list of tuples into normal list
    all_tobs = list(np.ravel(results))

    return jsonify(all_tobs)


@app.route("/api/v1.0/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session=Session(engine)

    #Remove any dashes from start date and convert to isoformat
    start = start.replace('-','')
    start = dt.datetime.strptime(start, "%m%d%Y").date().isoformat()

    #Perform a query of the min, max, and avg temps for all 
    # dates greater than or equal to a given start date
    sel=[func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)]
  
    results=session.query(*sel).\
            filter(measurement.date >= start).all()

    session.close()

    # Convert list of tuples into normal list
    start_stats = list(np.ravel(results))

    return jsonify(start_stats)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # Create our session (link) from Python to the DB
    session=Session(engine)

    #Remove any dashes from start/end dates and convert to isoformat
    start = start.replace('-','')
    start = dt.datetime.strptime(start, "%m%d%Y").date().isoformat()
    end = end.replace('-','')
    end = dt.datetime.strptime(end, "%m%d%Y").date().isoformat()

    #Perform a query of the min, max, and avg temps for all 
    # dates greater than or equal to a given start date
    sel=[func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)]
  
    results=session.query(*sel).\
            filter(measurement.date >= start).\
            filter(measurement.date <= end).all()

    session.close()

    # Convert list of tuples into normal list
    start_end_stats = list(np.ravel(results))

    return jsonify(start_end_stats)



if __name__ == '__main__':
    app.run(debug=True)