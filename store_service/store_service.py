import atexit
import json
import os
import re
import requests
import uuid
import time
import redis
from flask import request
from flask import Flask, jsonify
from urllib.parse import unquote
from common.utils import check_rsp_code
from prometheus_flask_exporter import PrometheusMetrics


app = Flask(__name__)



#create connection with redis-store-service
def connect_db():
    pool = redis.ConnectionPool(host='redis-store-service', port=6379, decode_responses=True)
    db = redis.Redis(connection_pool=pool)
    return db


#show the list of all stores
@app.route('/stores', methods=['GET'])
def get_store_list():
    db=connect_db()
    if len(db.hgetall('stores'))==0:

        return {"error": "Empty list"},204
        
    else:

        #remove all backslash in data
        json_data = json.dumps(db.hgetall('stores'))
        json_without_slash = json.loads(json_data)

        return json.dumps(json_without_slash), 200
        

#show the store info with specific store id
@app.route('/store/<store_id>', methods=['GET'])
def get_store(store_id):
    db=connect_db()
    if db.hexists("stores", store_id):
        return json.loads(db.hget("stores",store_id)), 200
    else:
        return {"Error": "Store not found"},404




#show the store status with specific store id
@app.route('/store/<store_id>/status', methods=['GET'])
def get_status(store_id):
    db=connect_db()

    if db.hexists("stores", store_id):

        #get json data from redis first and turn into dictionary
        json_data = json.loads(db.hget("stores",store_id))

        result = '{ "status" : ' + '"'+ json_data["status"] +'"' + ',' + '"offlineReason"'+' : ' +  '"N/A"' +'}'
        

        return result, 200

    else:
        return {"Error": "store not found"},404





#set store restaurant status with specific store id
@app.route('/store/<store_id>/setStatus', methods=['POST', 'GET'])
def set_status(store_id):
    db=connect_db()


    newStatus = request.args.get('newStatus')

    #why edit the status
    reason = request.args.get('reason')

    if db.hexists("stores", store_id):

        #get json data from redis first and turn into dictionary
        json_data = json.loads(db.hget("stores",store_id))

        json_data["status"] = newStatus

        #update the value in db
        db.hset("stores",store_id, json.dumps(json_data))
        

        return {"Success": "status updated"}, 200

    else:
        return {"Error": "Store not found"},404




#show the holiday_hours with specific store id
@app.route('/store/<store_id>/holiday-hours', methods=['GET'])
def get_holiday_hours(store_id):
    db=connect_db()


    if db.hexists("holidayHours", store_id):

        return json.loads(db.hget("holidayHours",store_id)), 200

    else:
        return {"Error": "store not found"},404





#set store restaurant status with specific store id
@app.route('/store/<store_id>/setHoliday-hours', methods=['POST', 'GET'])
def set_holiday_hours(store_id):
    db=connect_db()

    #get the url Input String from http
    url = request.args.get('jsonInputString')

    #decode the url encoded string
    jsonInputString = unquote(url)

   
    if db.hexists("holidayHours", store_id):

        #update the json in db
        db.hset("holidayHours",store_id, json.dumps(jsonInputString))
        

        return {"Success": "Holiday-hours updated"}, 200

    else:

        return {"Error": "Store not found"},404












