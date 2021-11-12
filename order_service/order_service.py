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


def create_order(_product_ids, _customer_id):
    """
    Create an order entity.

    :param _product_ids: The product IDs the order is for.
    :param _customer_id: The customer ID the order is made by.
    :return: A dict with the entity properties.
    """
    return {
        'id': str(uuid.uuid4()),
        'product_ids': _product_ids,
        'customer_id': _customer_id
    }


if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    store.activate_entity_cache('order')
    atexit.register(store.deactivate_entity_cache, 'order')

def connect_db():
    pool = redis.ConnectionPool(host='redis', port=6379, decode_responses=True)
    db = redis.Redis(connection_pool=pool)
    return db

#@app.route('/orders', methods=['POST'])
@app.route('/order', methods=['POST'])#receive a order 
def create_order():
    db=connect_db()
    values = request.get_json()
    if db.hexists("orders", values["id"]):
        return {'error': 'This order already exists'}, 409
    else:
        #notification
        webhook_url=""
        status_code=0
        time=0
        status_code=200 #assume the status_code 200 is returned
        while status_code!=200 and time<7:
            webhook_url="http://localhost:5000/parner"
            rsp = requests.post(webhook_url, json=values)
            status_code=rsp.status_code
            time+=1
        
        db.hset("orders",values["id"],json.dumps(values))
        return {"message":"order is created"}, 200

@app.route('/order/<order_id>', methods=['GET'])
def get_order(order_id):
    db=connect_db()
    if db.hexists("orders", order_id):
        return json.loads(db.hget("orders",order_id)), 200
    else:
        return {"error": "not found"},404

@app.route('/orders/<order_id>/accept_pos_order', methods=['POST'])#accept order
def accept_order(order_id):
    db=connect_db()
    if db.hexists("orders", order_id):
        order = json.loads(db.hget("orders",order_id))
        order["current_state"]="ACCEPTED"
        db.hset("orders",order_id,json.dumps(order))


        
        return '',204
    else:
        return {"error": "not found"},404