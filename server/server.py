from flask import Flask, request, jsonify
from sqlalchemy import Column, Integer, Text, Float, DateTime, create_engine, ForeignKey, func, and_
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import func
from flask_restful import Resource, Api
from dataclasses import dataclass
# import json
import simplejson as j
import pandas as pd
from flask_cors import CORS, cross_origin

Base = declarative_base()  # Basisklasse aller in SQLAlchemy verwendeten Klassen
metadata = Base.metadata

engine = create_engine('sqlite:///olympics.db', echo=True)

db_session = scoped_session(sessionmaker(
    autocommit=True, autoflush=True, bind=engine))
# Dadurch hat jedes Base - Objekt (also auch ein GeoInfo) ein Attribut query für Abfragen
Base.query = db_session.query_property()
app = Flask(__name__)  # Die Flask-Anwendung
cors = CORS(app)  # Ohne dieser Anweisung
# darf man von Webseiten aus nicht zugrfeifen
api = Api(app)  # Die Flask API


@dataclass
class NocRegions(Base):
    noc: str
    region: str
    notes: str

    __tablename__ = 'noc_regions'
    noc = Column('NOC', Text, primary_key=True)
    region = Column('region', Text)
    notes = Column('notes', Text)


@dataclass  # Diese ermoeglicht das Schreiben als JSON mit jsonify
class AthleteEvents(Base):
    __tablename__ = 'athlete_events'

    id: int
    name: str
    sex: str
    age: int
    height: int
    weight: int
    noc: NocRegions

    id = Column('ID', Integer, primary_key=True)
    name = Column('Name', Text)
    sex = Column('Sex', Text)
    age = Column('Age', Integer)
    height = Column('Height', Integer)
    weight = Column('Weight', Integer)
    team = Column('Team', Text)
    noc = Column('NOC', Text, ForeignKey(NocRegions.noc))
    games = Column('Games', Text)
    year = Column('Year', Integer)
    season = Column('Season', Text)
    city = Column('City', Text)
    sport = Column('Sport', Text)
    event = Column('Event', Text)
    medal = Column('Medal', Text)


@app.route('/event_by_noc/<string:noc>')
def event_by_noc(noc):
    infos = AthleteEvents.query.filter(AthleteEvents.noc == noc).all()
    return jsonify(infos)


@app.route('/regions')
def regions():
    infos = NocRegions.query.all()
    return jsonify(infos)




def medals_by_noc(noc):
    m = db_session.query(AthleteEvents.medal, func.count(AthleteEvents.medal)).filter(and_(
        AthleteEvents.medal != 'NA', AthleteEvents.noc == noc)).group_by(AthleteEvents.medal).all()
    m = pd.DataFrame.from_records(m, columns=['medal', 'cnt'])
    m['medal'] = pd.Categorical(m['medal'], ["Gold", "Silver", "Bronze"])
    m = m.sort_values("medal")
    return m.values.tolist()


@app.route('/medals/<string:noc>')
def medals(noc):
    m = medals_by_noc(noc)

    return jsonify(m)

@app.route('/get_Athletes/<string:noc>/<string:event>')
def get_atheles(noc, event):
    res = engine.execute(
        "Select name, sex, age, height, weight, games from athlete_events WHERE NOC = '{0}' and event = :eve".format(noc), eve=event)

    res = [(row[0], row[1], row[2], row[3], row[4], row[5]) for row in res]

    return j.dumps(res)

@app.route('/medals2/<string:noc>')
def medals2(noc):
    m = medals_by_noc(noc)
    key = []
    val = []
    for i in m:
        key.append(i[0])
        val.append(i[1])
    res = [{'x': key, 'y': val, 'type': 'bar'}]
    return j.dumps(res)

@app.route('/winner/<string:noc>')
def medals3(noc):
    res = engine.execute("SELECT count(*), Season from athlete_events  where Medal = 'Gold' and NOC = '{0}' GROUP by Season ".format(noc))
    key = []
    val = []
    for r in res:
        key.append(r[1])
        val.append(r[0])
    res = [{'x': key, 'y': val,'type':'bar'}]
    print(res)
    return j.dumps(res)

@app.route('/events')
def events():
    infos = db_session.query(AthleteEvents.event).distinct(
        AthleteEvents.event).order_by(AthleteEvents.event).all()
    return j.dumps(infos)


@app.route('/get_events_by_NOC/<string:noc>')
def eventsByNoc(noc):
    res = engine.execute(
        "SELECT distinct event FROM athlete_events where NOC = '{0}'".format(noc))
    res = [row[0] for row in res]
    return j.dumps(res)



@app.route('/count_by_sex')
def group_by_sex():
    res = engine.execute(
        "SELECT sex, medal, count(*) FROM athlete_events WHERE medal != 'NA' GROUP BY sex, medal")
    res = [(row[0], row[1], row[2]) for row in res]
    return j.dumps(res)


@app.route('/count_by_sex2')
def group_by_sex2():
    res = engine.execute(
        "SELECT sex, medal, count(*) FROM athlete_events WHERE medal != 'NA' GROUP BY sex, medal")
    keyM = []
    valM = []
    keyF = []
    valF = []
    for r in res:
        if r[0] == 'M':
            keyM.append(r[1])
            valM.append(r[2])
        else:
            keyF.append(r[1])
            valF.append(r[2])

    res = [(row[0], row[1], row[2]) for row in res]
    res = [{'x': keyM, 'y': valM, 'name': 'Male', 'type': 'bar'},
           {'x': keyF, 'y': valF, 'name': 'Female', 'type': 'bar'}]
    return j.dumps(res)


@app.route('/medals_per_country')
def medals_per_country():
    res = engine.execute(
        "SELECT NOC, Team, Medal from athlete_events GROUP by NOC")
    res = [(row[0], row[1], row[2]) for row in res]
    return j.dumps(res)
 

@app.teardown_appcontext
def shutdown_session(exception=None):
    print("Shutdown Session")
    db_session.remove()


if __name__ == '__main__':
    app.run(debug=True)
