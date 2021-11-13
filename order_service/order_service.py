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


def connect_db():
    pool = redis.ConnectionPool(host='redis-order-service', port=6379, decode_responses=True)
    db = redis.Redis(connection_pool=pool)
    return db


#@app.route('/orders', methods=['POST'])
@app.route('/order', methods=['POST'])#receive a order 
def handle_order():
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
        if order["current_state"]=="CREATED":
            order["current_state"]="ACCEPTED"
            db.hset("orders",order_id,json.dumps(order))
            accept_order=create_order(order_id, order["current_state"])
            store.publish('order', 'ACCEPTED', **accept_order)
            return '',204
        else:
            return {"error":"The order state is "+order["current_state"]+". Only the order with order state CREATED can be accepted."},409
    else:
        return {"error": "not found"},404


@app.route('/orders/<order_id>/deny_pos_order', methods=['POST'])#deny order
def deny_order(order_id):
    db=connect_db()
    if db.hexists("orders", order_id):
        order = json.loads(db.hget("orders",order_id))
        if order["current_state"]=="CREATED":
            order["current_state"]="DENIED"
            db.hset("orders",order_id,json.dumps(order))
            deny_order=create_order(order_id, order["current_state"])
            #store.publish('order', 'ACCEPTED', **accept_order)
            return '',204
        else:
            return {"error":"The order state is "+order["current_state"]+". Only the order with order state CREATED can be denied."},409
    else:
        return {"error": "not found"},404

@app.route('/orders/<order_id>/cancel', methods=['POST'])#cancel order
def cancel_order(order_id):
    db=connect_db()
    if db.hexists("orders", order_id):
        order = json.loads(db.hget("orders",order_id))
        if order["current_state"]!="DENIED" and order["current_state"]!="FINISHED" and order["current_state"]!="CANCELED":
            order = json.loads(db.hget("orders",order_id))
            order["current_state"]="CANCELED"
            db.hset("orders",order_id,json.dumps(order))
            cancel_order=create_order(order_id, order["current_state"])
            #store.publish('order', 'ACCEPTED', **accept_order)
            return '',204
        else:
            return {"error":"The order state is "+order["current_state"]+". It cannot be canceled."},409
    else:
        return {"error": "not found"},404

@app.route('/orders/<order_id>/restaurantdelivery/status', methods=['POST'])#accept order
def update_delivery_status(order_id):
    return {"Test":"Test"},200
    # db=connect_db()

    # if db.hexists("orders", order_id):

        # try:
        #     order = json.loads(db.hget("orders",order_id))
        # except Exception as e:
        #     return {"msg": e},200

        #values = request.get_json()
        # if values["status"]=="started" or values["status"]=="arriving" or values["status"]=="delivered":
        #     order["deliveries"]["current_state"]=values["status"]
        #     db.hset("orders",order_id,json.dumps(order))
        #     return '',204
        # else:
        #     return {"error":"The order state is "+order["current_state"]+". Only the order with order state CREATED can be accepted."},409
    # else:
    #     return {"error": "not found"},404


