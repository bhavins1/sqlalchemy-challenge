import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    return (
        f"Welcome to the Exploratory Climate Analysis!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start1>/<end><br/>"
    )


# 4. Define what to do when a user hits the /about route
@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)
    
    precip = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-24').all()

    session.close()

    all_precip = []
    for date, prcp in precip:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        all_precip.append(precip_dict)


    return jsonify(all_precip)


@app.route("/api/v1.0/stations")
def stations():
    
    session = Session(engine)
    
    results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station. elevation).all()

    session.close()

    
    return jsonify(results)


@app.route("/api/v1.0/tobs")
def tobs():
    
    session = Session(engine)
    
    temp = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= '2016-08-24', Measurement.station == 'USC00519281' ).all()

    session.close()

    all_temp = []
    for date, tobs in temp:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["tobs"] = tobs
        all_temp.append(temp_dict)


    return jsonify(all_temp)


@app.route("/api/v1.0/<start>")
def input(start):
    session = Session(engine)

    start_date = start

    query = session.query(Measurement.station, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
                group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).filter(Measurement.date >= start_date).all()

    session.close()

    all_query = []
    for station, min, max, avg in query:
        query_dict = {}
        query_dict["station"] = station
        query_dict["min"] = min
        query_dict["max"] = max
        query_dict["avg"] = avg
        all_query.append(query_dict)


    return jsonify(all_query)

    return jsonify({"error": f"Character with {start_date} not found."}), 404


@app.route("/api/v1.0/<start>/<end>")
def input1(start,end):
    session = Session(engine)

    start_date = start
    end_date = end

    query1 = session.query(Measurement.station, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
                group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).\
                    filter(Measurement.date >= start_date, Measurement.date <= end_date).all()

    session.close()
    
    all_query = []
    for station, min, max, avg in query1:
        query_dict = {}
        query_dict["station"] = station
        query_dict["min"] = min
        query_dict["max"] = max
        query_dict["avg"] = avg
        all_query.append(query_dict)


    return jsonify(all_query)

    return jsonify({"error": f"Character with {end_date} not found."}), 404


if __name__ == "__main__":
    app.run(debug=True)