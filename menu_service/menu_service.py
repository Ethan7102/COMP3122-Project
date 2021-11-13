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

from common.utils import check_rsp_code
from lib.event_store import EventStore


app = Flask(__name__)
store = EventStore()


def connect_db():
    pool = redis.ConnectionPool(host='redis', port=6379, decode_responses=True)
    db = redis.Redis(connection_pool=pool)
    return db

@app.route('/<store_id>/menus', methods=['PUT'])#receive a order 
def upload_menu(store_id):
    db=connect_db()
    values = request.get_json()
    try:
        db.hset("menus",store_id,json.dumps(values))
        return values, 200
    except Exception as e:
        return {"message":str(e)},200


# @app.route('/menus', methods=['GET'])
# def get_all_menu():
#     try:
#         db=connect_db()
#         return json.loads(db.hgetall("menus")), 200
#         # return {"key": "value"}, 200
#     except Exception as e:
#         return {"message":str(e)},200
#     # db=connect_db()
#     # return json.loads(db.hgetall("menus")), 200

@app.route('/<store_id>/menus', methods=['GET'])
def get_menu(store_id):
    db=connect_db()
    if db.hexists("menus", store_id):
        return json.loads(db.hget("menus",store_id)), 200
    else:
        return {"Error": "store's menu not found"},404

@app.route('/<store_id>/menus/items', methods=['POST'])
def update_menu(store_id):
    db=connect_db()
    values = request.get_json()
    try:
        db.hset("menus",store_id,json.dumps(values))
        return values, 200
    except Exception as e:
        return {"message":str(e)},200