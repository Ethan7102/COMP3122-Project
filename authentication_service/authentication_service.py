import atexit
import json
import os
import re
import requests
import uuid
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
from common.utils import check_rsp_code
from lib.event_store import EventStore

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
    if initialization:
        initialize()
    values = request.get_json()
    db = connect_db()
    if db.hexists("user", values["username"]):
        password = db.hget("user", values["username"])
        if password == values["password"]:
            token = secrets.token_hex(16)
            db.hset("tokens", values["username"], token)
            return {"Your token": token}, 200
    return {"error": "username or password is incorrect."}, 400
