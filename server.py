#!/usr/bin/env python2.7

import copy
import urllib
import argparse

from pymongo import MongoClient

from flask import Flask
from flask import jsonify
from flask import request

import geocoder

db = ''
app = Flask(__name__)

MAX_DISTANCE = 250 # max distance running for 3 minutes to and fro'

alerts = []
user_alerts = {}

search_dict = {
  "loc": {
    "$near": {
      "$geometry": {
        "type": "Point",
        "coordinates": [
          0,
          0
        ]
      },
      "$minDistance":0,
      "$maxDistance": MAX_DISTANCE
    }
  }
}

@app.route('/aed/<lat>/<lon>/', methods=['GET'])
def get_aed(lat, lon):
    """ Get nearest AED to a location """
    lat = float(lat)
    lon = float(lon) # no negative floats in flask :(
    search = copy.deepcopy(search_dict)
    search["loc"]["$near"]["$geometry"]["coordinates"] = [lon, lat]
    print search
    curs = db.aed.find(search)
    #curs = db.aed.find()
    print "COUNT!"
    print "lel"
    print curs.count()
    for c in curs:
        c["_id"] = ""
        return jsonify(c)
    
    return jsonify({})

@app.route('/update/<lat>/<lon>/<uid>/', methods=['POST'])
def post_update(lat, lon, uid):
    """ Update watch location """
    lat = float(lat)
    lon = float(lon)
    curs = db.watches.find({"_id" : uid})
    elem = None
    for c in curs:
        elem = c
        break

    updated_val = {"_id":uid, "loc":{"type":"Point", "coordinates":[lon, lat]}}
    if elem is not None:
        db.watches.update({"_id":uid},updated_val)
    else:
        db.watches.insert(updated_val)

    return '{}'

@app.route('/report/<lat>/<lon>/<uid>/', methods=['POST'])
def post_report(lat, lon, uid):
    """ Report incident, send info and request of aed to others """
    lat = float(lat)
    lon = float(lon)
    aed = get_aed(lat,lon)
    addr = geocoder.google([lat,lon], method='reverse')
    addr = addr.address

    # alert nearby users
    alert_nearest(lat, lon, aed, addr)

    return '{}'

@app.route('/poll/<user>/', methods=['GET'])
def poll_alert(user):
    if user in user_alerts:
        return jsonify(alerts[user_alerts[user]])
    return jsonify({})

def set_alert(user, index):
    global user_alerts
    user_alerts[user] = index

def alert_nearest(lat, lon, aed, addr, distance=200):
    """ gets nearest users to lat lon pair and set distance """
    global alerts
    search = copy.deepcopy(search_dict)
    search["loc"]["$near"]["$geometry"]["coordinates"] = [lon, lat]
    curs = db.watches.find(search)
    alerts += {"aed":aed, "addr":addr}
    for user in curs:
        set_alert(user, len(alerts) - 1) # race condition much?



def setup():
    global db
    client = MongoClient()
    db = client.lifesaber

if __name__=="__main__":
    parser = argparse.ArgumentParser();

    args = parser.parse_args()
    setup()
    app.run(debug=True)
