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

engine = create_engine('sqlite:///countries.db', echo=True)

db_session = scoped_session(sessionmaker(
    autocommit=True, autoflush=True, bind=engine))
# Dadurch hat jedes Base - Objekt (also auch ein GeoInfo) ein Attribut query für Abfragen
Base.query = db_session.query_property()
app = Flask(__name__)  # Die Flask-Anwendung
cors = CORS(app)  # Ohne dieser Anweisung
# darf man von Webseiten aus nicht zugrfeifen
api = Api(app)  # Die Flask API





@dataclass  # Diese ermoeglicht das Schreiben als JSON mit jsonify
class Country(Base):
    __tablename__ = 'country'

    id: int
    country: str
    iso3: str
    iso2: str
    ioc: str
    fifa: str
    latitude: float
    longitude: float
    wiki_label: str
    wiki_description: str

    id = Column('ID', Integer, primary_key=True)
    country = Column('Country', Text)
    iso3 = Column('ISO-ALPHA-3', Text)
    iso2 = Column('ISO-ALPHA-2', Text)
    ioc = Column('IOC', Text)
    fifa = Column('FIFA', Text)
    latitude = Column('Latitude', Float)
    longitude = Column('Longitude', Float)
    wiki_label = Column('WikiData_Label', Text)
    wiki_description = Column('WikiData_Description', Text)


@app.route('/country_by_id/<int:id>')
def get_country_by_id(id):
    infos = Country.query.filter(Country.id == id).all()
    return jsonify(infos)



# @app.route('/regions')
# def regions():
#     infos = NocRegions.query.all()
#     return jsonify(infos)




# def medals_by_noc(noc):
#     m = db_session.query(AthleteEvents.medal, func.count(AthleteEvents.medal)).filter(and_(
#         AthleteEvents.medal != 'NA', AthleteEvents.noc == noc)).group_by(AthleteEvents.medal).all()
#     m = pd.DataFrame.from_records(m, columns=['medal', 'cnt'])
#     m['medal'] = pd.Categorical(m['medal'], ["Gold", "Silver", "Bronze"])
#     m = m.sort_values("medal")
#     return m.values.tolist()


# @app.route('/medals/<string:noc>')
# def medals(noc):
#     m = medals_by_noc(noc)

#     return jsonify(m)

# @app.route('/get_Athletes/<string:noc>/<string:event>')
# def get_atheles(noc, event):
#     res = engine.execute(
#         "Select name, sex, age, height, weight, games from athlete_events WHERE NOC = '{0}' and event = :eve".format(noc), eve=event)

#     res = [(row[0], row[1], row[2], row[3], row[4], row[5]) for row in res]

#     return j.dumps(res)

# @app.route('/medals2/<string:noc>')
# def medals2(noc):
#     m = medals_by_noc(noc)
#     key = []
#     val = []
#     for i in m:
#         key.append(i[0])
#         val.append(i[1])
#     res = [{'x': key, 'y': val, 'type': 'bar'}]
#     return j.dumps(res)

# @app.route('/winner/<string:noc>')
# def medals3(noc):
#     res = engine.execute("SELECT count(*), Season from athlete_events  where Medal = 'Gold' and NOC = '{0}' GROUP by Season ".format(noc))
#     key = []
#     val = []
#     for r in res:
#         key.append(r[1])
#         val.append(r[0])
#     res = [{'x': key, 'y': val,'type':'bar'}]
#     print(res)
#     return j.dumps(res)

# @app.route('/events')
# def events():
#     infos = db_session.query(AthleteEvents.event).distinct(
#         AthleteEvents.event).order_by(AthleteEvents.event).all()
#     return j.dumps(infos)


# @app.route('/get_events_by_NOC/<string:noc>')
# def eventsByNoc(noc):
#     res = engine.execute(
#         "SELECT distinct event FROM athlete_events where NOC = '{0}'".format(noc))
#     res = [row[0] for row in res]
#     return j.dumps(res)



# @app.route('/count_by_sex')
# def group_by_sex():
#     res = engine.execute(
#         "SELECT sex, medal, count(*) FROM athlete_events WHERE medal != 'NA' GROUP BY sex, medal")
#     res = [(row[0], row[1], row[2]) for row in res]
#     return j.dumps(res)


# @app.route('/count_by_sex2')
# def group_by_sex2():
#     res = engine.execute(
#         "SELECT sex, medal, count(*) FROM athlete_events WHERE medal != 'NA' GROUP BY sex, medal")
#     keyM = []
#     valM = []
#     keyF = []
#     valF = []
#     for r in res:
#         if r[0] == 'M':
#             keyM.append(r[1])
#             valM.append(r[2])
#         else:
#             keyF.append(r[1])
#             valF.append(r[2])

#     res = [(row[0], row[1], row[2]) for row in res]
#     res = [{'x': keyM, 'y': valM, 'name': 'Male', 'type': 'bar'},
#            {'x': keyF, 'y': valF, 'name': 'Female', 'type': 'bar'}]
#     return j.dumps(res)


# @app.route('/medals_per_country')
# def medals_per_country():
#     res = engine.execute(
#         "SELECT NOC, Team, Medal from athlete_events GROUP by NOC")
#     res = [(row[0], row[1], row[2]) for row in res]
#     return j.dumps(res)
 

# @app.teardown_appcontext
# def shutdown_session(exception=None):
#     print("Shutdown Session")
#     db_session.remove()


if __name__ == '__main__':
    app.run(debug=True)
