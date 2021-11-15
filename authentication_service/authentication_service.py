import atexit
import json
import os
import re
import requests
import redis
import uuid
import secrets

from flask import request
from flask import Flask, jsonify
from flask import Response
import prometheus_client
from prometheus_client.core import CollectorRegistry
from prometheus_client import Summary, Counter, Histogram, Gauge
import time

app = Flask(__name__)
_INF = float("inf")

graphs = {}
graphs['c'] = Counter('python_request_operations_total',
                      'The total number of processed requests')
graphs['h'] = Histogram('python_request_duration_seconds',
                        'Histogram for the duration in seconds.', buckets=(1, 2, 5, 6, 10, _INF))
initialization = 1


def initialize():
    db = connect_db()
    db.hset("user", "comp3122", "comp3122")
    initialization = 0
    # set a token for testing
    db.hset("tokens", "test", "740becc4b623786cc812c956a5afb30e")


def connect_db():
    pool = redis.ConnectionPool(
        host='redis-authentication-service', port=6379, decode_responses=True)
    db = redis.Redis(connection_pool=pool)
    return db


@app.route('/authentication/get_token', methods=['POST'])
def get_token():
    start = time.time()
    graphs['c'].inc()
    if initialization:
        initialize()
    values = request.get_json()
    db = connect_db()
    if db.hexists("user", values["username"]):
        password = db.hget("user", values["username"])
        if password == values["password"]:
            token = secrets.token_hex(16)
            db.hset("tokens", values["username"], token)
            end = time.time()
            graphs['h'].observe(end - start)
            return {"token": token}, 200
    end = time.time()
    graphs['h'].observe(end - start)
    return {"error": "username or password is incorrect."}, 400

@app.route("/authentication-metrics", methods=['GET'])
def requests_count():
    res = []
    for k,v in graphs.items():
        res.append(prometheus_client.generate_latest(v))
    return Response(res, mimetype="text/plain") 
