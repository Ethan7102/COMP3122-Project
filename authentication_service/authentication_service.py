import atexit
import json
import os
import re
import requests
import uuid
import time
import redis
import uuid
import secrets

from flask import request
from flask import Flask, jsonify

from common.utils import check_rsp_code
from lib.event_store import EventStore

app = Flask(__name__)

initialization = 1

def initialize():
    db = connect_db()
    db.hset("user", "comp3122", "comp3122")
    initialization = 0
    #set a token for testing
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
