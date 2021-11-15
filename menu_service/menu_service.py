import atexit
import json
import os
import re
import requests
import uuid
import time
import redis

from flask import request
from flask import request, Response
from flask import Flask, jsonify

import prometheus_client
from prometheus_client.core import CollectorRegistry
from prometheus_client import Summary, Counter, Histogram, Gauge


app = Flask(__name__)
_INF = float("inf")

graphs = {}
graphs['c'] = Counter('python_request_operations_total', 'The total number of processed requests')
graphs['h'] = Histogram('python_request_duration_seconds', 'Histogram for the duration in seconds.', buckets=(1, 2, 5, 6, 10, _INF))



def connect_db():
    pool = redis.ConnectionPool(host='redis-menu-service', port=6379, decode_responses=True)
    db = redis.Redis(connection_pool=pool)
    return db

#Upload menu
@app.route('/<store_id>/menus', methods=['PUT'])
def upload_menu(store_id):
    start = time.time()
    graphs['c'].inc()
    db=connect_db()
    values = request.get_json()
    try:
        end = time.time()
        graphs['h'].observe(end - start)
        db.hset("menus",store_id,json.dumps(values))
        return values, 200
    except Exception as e:
        end = time.time()
        graphs['h'].observe(end - start)
        return {"message":str(e)},200

@app.route('/<store_id>/menus', methods=['GET'])
def get_menu(store_id):
    start = time.time()
    graphs['c'].inc()
    db=connect_db()
    if db.hexists("menus", store_id):
        end = time.time()
        graphs['h'].observe(end - start)
        return json.loads(db.hget("menus",store_id)), 200
    else:
        end = time.time()
        graphs['h'].observe(end - start)
        return {"Error": "store's menu not found"},404

@app.route('/<store_id>/menus/items', methods=['POST'])
def update_menu(store_id):
    start = time.time()
    graphs['c'].inc()
    db=connect_db()
    values = request.get_json()
    try:
        end = time.time()
        graphs['h'].observe(end - start)
        db.hset("menus",store_id,json.dumps(values))
        return values, 200
    except Exception as e:
        end = time.time()
        graphs['h'].observe(end - start)
        return {"message":str(e)},200

@app.route("/menu-metrics", methods=['GET'])
def menu_requests_count():
    res = []
    for k,v in graphs.items():
        res.append(prometheus_client.generate_latest(v))
    return Response(res, mimetype="text/plain") 