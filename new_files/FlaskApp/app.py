import os

import pandas as pd
import numpy as np
import math as math
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
from sqlalchemy.ext.declarative import declarative_base


#################################################
# Database Setup
#################################################
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@:5432/CTA"
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

#
# session = Session(engine)

# Save references to each table
Total_Data = Base.classes.total_ridership
Weekday_Data = Base.classes.weekday_data
Saturday_Data = Base.classes.saturday_data
Sunday_Data = Base.classes.sunday_holiday_data

# print(Station_Metadata)


# This is the first route
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/metadata/<station>")
def station_metadata(station):
    """Return the MetaData for a given sample."""
    sel = [
        Total_Data.Station_Name
    ]

    results = db.session.query(*sel).filter(Total_Data.Station_Name == station).all()

    station_metadata = {}
    for result in results:
        station_metadata["Station"] = result[0]

    
    print(station_metadata)
    return jsonify(station_metadata)


@app.route("/stations")
def stations():
    sel = [Total_Data.Station_Name]

    stations = [station[0] for station in db.session.query(*sel).all()]

    return jsonify(stations)

@app.route("/total/<station>")
def total_ridership(station):

    stmt = db.session.query(Total_Data).statement

    df = pd.read_sql_query(stmt, db.session.bind)

    ridership_data = df.loc[df['Station_Name'] == station]

    years = list(df.columns)[3:]
    
    ridership = ridership_data.values[0][3:]
    ridershipnona = [0 if math.isnan(x) else x for x in ridership]
   
    data = {
        'year': years,
        'ridership': ridershipnona
    }

    return jsonify(data)


@app.route("/station/<station>")
def daily_ridership(station):

    stmt_weekday = db.session.query(Weekday_Data).statement
    
    weekday_df = pd.read_sql_query(stmt_weekday, db.session.bind)

    weekday_ridership_data = weekday_df.loc[weekday_df['Station_Name'] == station]

    years = list(weekday_df.columns)[3:]

    weekday_ridership = weekday_ridership_data.values[0][3:]
    weekday_ridershipnona = [0 if math.isnan(x) else x for x in weekday_ridership]

    # Saturday Data 

    stmt_saturday = db.session.query(Saturday_Data).statement
    
    saturday_df = pd.read_sql_query(stmt_saturday, db.session.bind)

    saturday_ridership_data = saturday_df.loc[saturday_df['Station_Name'] == station]

    saturday_ridership = saturday_ridership_data.values[0][3:]
    saturday_ridershipnona = [0 if math.isnan(x) else x for x in saturday_ridership]
    print(saturday_ridershipnona)
    # Sunday Holiday Data 

    stmt_sunday = db.session.query(Sunday_Data).statement
    
    sunday_df = pd.read_sql_query(stmt_sunday, db.session.bind)

    sunday_ridership_data = sunday_df.loc[sunday_df['Station_Name'] == station]

    sunday_ridership = sunday_ridership_data.values[0][3:]
    sunday_ridershipnona = [0 if math.isnan(x) else x for x in sunday_ridership]

    data = {
        'year': years,
        'weekday_ridership': weekday_ridershipnona,
        'saturday_ridership': saturday_ridershipnona,
        'sunday_ridership': sunday_ridershipnona       
    }

    return jsonify(data)


@app.route("/sunday/<station>")
def sunday_ridership(station):

    stmt = db.session.query(Sunday_Data).statement

    df = pd.read_sql_query(stmt, db.session.bind)

    ridership_data = df.loc[df['Station_Name'] == station]

    years = list(df.columns)[3:]

    ridership = ridership_data.values[0][3:]

    data = {
        'year': years,
        'ridership': ridership.tolist()
    }

    return jsonify(data)

if __name__ == "__main__":
    app.run()