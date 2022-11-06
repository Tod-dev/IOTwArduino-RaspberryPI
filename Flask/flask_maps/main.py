# google maps
# persistent objects
#pip install flask-sqlalchemy
#pip install -U googlemaps



from flask import Flask
from config import Config
from flask import render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests
import json
import googlemaps
from geopy import distance

appname = "IOT - sample map"
app = Flask(appname)
myconfig = Config
app.config.from_object(myconfig)

# db creation
db = SQLAlchemy(app)


gmaps = googlemaps.Client(key=Config.GOOGLEMAPS_APIKEY)


def distanceLatLong(p0, p1, p2): # p0 is the point
    x0, y0 = p0
    x1, y1 = p1
    x2, y2 = p2
    dx = x2 - x1
    dy = y2 - y1
    d2 = dx*dx + dy*dy

    nx = ((x0-x1)*dx + (y0-y1)*dy) / d2
    if nx >= 0 and nx <= 1:
        nearest = (dx*nx + x1, dy*nx + y1)
        result = distance.distance(p0, nearest).km
    else:
        if distance.distance(p0, p1)<distance.distance(p0,p2):
            nearest = p1
            result = distance.distance(p0, p1).km
        else:
            nearest = p2
            result = distance.distance(p0, p2).km

    return result, nearest

class Sensorfeed(db.Model):
    id = db.Column('feed_id', db.Integer, primary_key = True)
    description = db.Column('description', db.String)
    value = db.Column('value', db.Integer)
    lat = db.Column('lat', db.Integer)
    long = db.Column('long', db.Integer)
    timestamp = db.Column(db.DateTime(timezone=True), nullable=False,  default=datetime.utcnow)
    def __init__(self, description, value, lat, long):
        self.value = value
        self.lat = lat
        self.long = long
        self.description = description

@app.route('/initDB')
def initDB():
    db.drop_all()
    db.create_all()
    sampleval1=Sensorfeed(description='sample 1', value=23, lat=44.629830759178724, long=10.965659602854137)
    sampleval2=Sensorfeed(description='sample 2', value=12, lat=44.6285174748942, long=10.97673176083943)
    sampleval3=Sensorfeed(description='sample 3', value=45, lat=44.6237222078703, long=10.958492740902416)
    db.session.add(sampleval1)
    db.session.add(sampleval2)
    db.session.add(sampleval3)
    db.session.commit()
    return "ok"
		
@app.route('/')
def mappaHTML():
    elenco=Sensorfeed.query.all()
    return render_template('mappa.html', lista=elenco, APIKEY=Config.GOOGLEMAPS_APIKEY, fzjavascript='myMap')


@app.route ('/route')
def getroute():
    now = datetime.now()
    routefrom="Disneyland"
    routeto ="Universal Studios Hollywood"
    routefrom='44.63757242419685, 10.94673393566677'
    routeto = '44.62306550033823, 10.98149536630288'
    directions_result = gmaps.directions(routefrom,routeto,
                                     mode="transit",
                                     departure_time=now)

    bestdirection=directions_result[0]
    polyline_encoded=bestdirection['overview_polyline']
    polyline_decoded = googlemaps.convert.decode_polyline(polyline_encoded['points'])
    polyline_decoded = str(polyline_decoded).replace('"','').replace("'",'')
    return render_template('mappa.html', param=polyline_decoded, APIKEY=Config.GOOGLEMAPS_APIKEY, fzjavascript='myRoute')


@app.route ('/points_onaroute')
def pointsonaroute():
    now = datetime.now()
    routefrom="Disneyland"
    routeto ="Universal Studios Hollywood"
    routefrom='44.63757242419685, 10.94673393566677'
    routeto = '44.62306550033823, 10.98149536630288'

    directions_result = gmaps.directions(routefrom,routeto,
                                         mode="transit",
                                         departure_time=now)

    bestdirection=directions_result[0]
    polyline_encoded=bestdirection['overview_polyline']
    polyline_decoded = googlemaps.convert.decode_polyline(polyline_encoded['points'])


    elenco=Sensorfeed.query.all()
    mioelenco=[]
    elenconearest=[]
    for curpoint in elenco:
        #check if val is in polyline
        pointpos = (curpoint.lat, curpoint.long)
        mindist=-1
        nearestpp=None

        for i in range(len(polyline_decoded)-1):
            dist, nearestpoint = distanceLatLong(pointpos,
                            (polyline_decoded[i]['lat'],polyline_decoded[i]['lng']),
                            (polyline_decoded[i+1]['lat'],polyline_decoded[i+1]['lng'])
                            )
            if mindist==-1 or mindist>dist:
                mindist=dist
                nearestpp=nearestpoint
        if mindist<Config.DISTTH:
            mioelenco.append(curpoint)
            elenconearest.append(nearestpp)
    polyline_decoded = str(polyline_decoded).replace('"','').replace("'",'')
    mioelencojs = "["
    for val in mioelenco:
        elem = "title: '{title}',description:'{descr}', lat:{lat},lng:{lng}".format(
            title=val.description, descr=val.value, lat=val.lat, lng=val.long)
        mioelencojs=mioelencojs+"{"+elem+"}"
    mioelencojson=mioelencojs+"]"
    return render_template('mappa.html', param={'points':mioelencojson, 'nearest':elenconearest, 'route':polyline_decoded}, APIKEY=Config.GOOGLEMAPS_APIKEY, fzjavascript='myPointOnaRoute')


@app.route('/points')
def points():
    elenco=Sensorfeed.query.all()
    mioelenco=[]
    for val in elenco:
        elem = {
            'title': val.description,
            'description' : str(val.value),
            'lat' : val.lat,
            'lng' : val.long
        }
        mioelenco.append(elem)
    outval = {'listaPunti': mioelenco}

    return jsonify(outval)

if __name__ == '__main__':

    port = 80
    interface = '0.0.0.0'
    app.run(host=interface,port=port)

