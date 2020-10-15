import numpy as np
import os

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func

from flask import Flask, jsonify
import datetime as dt




#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station= Base.classes.station


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
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    # Open a communication session with the database
    session = Session(engine)

    twelve_months_prcp = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > '2016-08-22').order_by(Measurement.date).all()

    # close the session to end the communication with the database
    session.close()

    precip = {date: prcp for date, prcp in twelve_months_prcp}
    return jsonify(precip)


@app.route("/api/v1.0/stations")
def stations():
     # Open a communication session with the database
    session = Session(engine)

    results = session.query(Station.station).all()

    # close the session to end the communication with the database
    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))
    print(all_stations)
    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
     # Open a communication session with the database
    session = Session(engine)

    temps_most_active_station = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date > '2016-08-22').order_by(Measurement.date).all()

 


    # close the session to end the communication with the database
    session.close()

    


    # Convert list of tuples into normal list
    all_temps = list(np.ravel(temps_most_active_station))
    print(all_temps)
    return jsonify(all_temps)

@app.route("/api/v1.0/<start_date>")
def calc_temps_start(start_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    # Open a communication session with the database
    session = Session(engine)

    calculated_temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()


    # close the session to end the communication with the database
    session.close()

    # Convert list of tuples into normal list
    temps_list = list(np.ravel(calculated_temps))
    print(temps_list)
    return jsonify(temps_list)

@app.route("/api/v1.0/<start_date>/<end_date>")
def calc_temps_end(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    # Open a communication session with the database
    session = Session(engine)

    calculated_temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()


    # close the session to end the communication with the database
    session.close()

    # Convert list of tuples into normal list
    temps_list = list(np.ravel(calculated_temps))
    print(temps_list)
    return jsonify(temps_list)
    



if __name__ == '__main__':
    app.run(debug=True)
