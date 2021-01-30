from flask import Flask, json, jsonify
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import inspect

engine = create_engine("sqlite:///hawaii.sqlite", connect_args={'check_same_thread': False})
# reflect an existing database into a new model
base = automap_base()
# reflect the tables
base.prepare(engine, reflect=True)

# Save references to each table
measurement = base.classes.measurement
station = base.classes.station
session = Session(engine)

app = Flask(__name__)  # the name of the file & the object (double usage)


# List all routes that are available.
@app.route("/")
def home():
    print("In & Out of Home section.")
    return (
        "Welcome to the Climate API!<br/><br/><br/>"
        "Available Routes:<br/>"
        "<ul>"
        "<li>/api/v1.0/precipitation</li>"
        "<li>/api/v1.0/stations</li>"
        "<li>/api/v1.0/tobs</li>"
        "<li>/api/v1.0/2016-01-01/</li>"
        "<li>/api/v1.0/2016-01-01/2016-12-31/</li>"
        "</ul>"
    )



@app.route('/api/v1.0/precipitation/')
def precipitation():

    last_date = session.query(measurement.date).order_by(measurement.date.desc()).first().date
    last_year = dt.datetime.strptime(last_date, '%Y-%m-%d') - dt.timedelta(days=365)

    rain_results = session.query(measurement.date, measurement.prcp). \
        filter(measurement.date >= last_year). \
        order_by(measurement.date).all()

    p_dict = dict(rain_results)
    print(f"Results for Precipitation - {p_dict}")
    return jsonify(p_dict)



@app.route('/api/v1.0/stations/')
def stations():

    station_list = session.query(station.station).order_by(station.station).all()
    print()
    print("station List:")
    station_list_final=[]
    for row in station_list:
        station_list_final.append(row[0])

    result_dict={"Stations":station_list_final}
    return jsonify(result_dict)



@app.route('/api/v1.0/tobs/')
def tobs():
    print("In TOBS section.")

    last_date = session.query(measurement.date).order_by(measurement.date.desc()).first().date
    last_year = dt.datetime.strptime(last_date, '%Y-%m-%d') - dt.timedelta(days=365)

    temp_obs = session.query(measurement.date, measurement.tobs).filter(measurement.date >= last_year).order_by(measurement.date).all()
    result_dict={}
    for each in temp_obs:
        result_dict[each[0]]=each[1]
    print()
    print("Temperature Results for All stations")
    print(temp_obs)
    print("Out of TOBS section.")
    return jsonify(result_dict)


@app.route('/api/v1.0/<start_date>/')
def calc_temps_start(start_date):
    print("In start date section.")
    print(start_date)

    select = [func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)]
    result_temp = session.query(*select).filter(measurement.date >= start_date).all()
    result_dict = {"min":result_temp[0][0],"avg":round(result_temp[0][1],2),"max":result_temp[0][2]}
    print()
    print(f"Calculated temp for start date {start_date}")
    print(result_temp)
    print("Out of start date section.")
    return jsonify(result_dict)


@app.route('/api/v1.0/<start_date>/<end_date>/')
def calc_temps_start_end(start_date, end_date):
    print("In start & end date section.")

    select = [func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)]
    result_temp = session.query(*select).filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()
    result_dict = {"min":result_temp[0][0],"avg":round(result_temp[0][1],2),"max":result_temp[0][2]}
    print()
    print(f"Calculated temp for start date {start_date} & end date {end_date}")
    print(result_temp)
    print("Out of start & end date section.")
    return jsonify(result_dict)


if __name__ == "__main__":
    app.run(debug=True)