import atexit
import json
import os
import re
import requests
import uuid
import time
import redis
import uuid

from flask import request
from flask import Flask, jsonify

from common.utils import check_rsp_code
from lib.event_store import EventStore

app = Flask(__name__)


def connect_db():
    pool = redis.ConnectionPool(
        host='redis-authentication-service', port=6379, decode_responses=True)
    db = redis.Redis(connection_pool=pool)
    return db


@app.route('/authentication/get_token', methods=['POST'])
def get_token():
    db = connect_db()
    password = db.hget("user", "comp3122")
    return {"test": password}, 200
