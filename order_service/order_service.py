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

@app.route('/stores/<store_id>/created-orders', methods=['GET']) # get orders of a specific store with status "CREATED"
def get_created_orders(store_id):
    db=connect_db()
    orders_keys=db.hkeys("orders")
    created_orders= {"orders":[]}
    for orders_key in orders_keys:    
        order = json.loads(db.hget("orders",orders_key))
        if order["current_state"] == "CREATED" and order["store"]["id"] == store_id:
            created_orders["orders"].append({"id":orders_key, "current_state":order["current_state"], "placed_at":order["placed_at"]})
    return created_orders,200

@app.route('/stores/<store_id>/canceled-orders', methods=['GET']) # get orders of a specific store with status "CREATED"
def get_canceled_orders(store_id):
    db=connect_db()
    orders_keys=db.hkeys("orders")
    canceled_orders= {"orders":[]}
    for orders_key in orders_keys:    
        order = json.loads(db.hget("orders",orders_key))
        if order["current_state"] == "CANCELED" and order["store"]["id"] == store_id:
            canceled_orders["orders"].append({"id":orders_key, "current_state":order["current_state"], "placed_at":order["placed_at"]})
    return canceled_orders,200

@app.route('/orders/<order_id>/accept_pos_order', methods=['POST'])#accept order
def accept_order(order_id):
    db=connect_db()
    if db.hexists("orders", order_id):
        order = json.loads(db.hget("orders",order_id))
        if order["current_state"]=="CREATED" or order["current_state"]=="DENIED":
            order["current_state"]="ACCEPTED"
            db.hset("orders",order_id,json.dumps(order))
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
        if order["current_state"]=="CREATED" or order["current_state"]=="ACCEPTED":
            order["current_state"]="DENIED"
            db.hset("orders",order_id,json.dumps(order))
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
            #store.publish('order', 'ACCEPTED', **accept_order)
            return '',204
        else:
            return {"error":"The order state is "+order["current_state"]+". It cannot be canceled."},409
    else:
        return {"error": "not found"},404

@app.route('/orders/<order_id>/restaurantdelivery/status', methods=['POST'])#update delivery status of an order
def update_delivery_status(order_id):
    db=connect_db()
    if db.hexists("orders", order_id):
        order = json.loads(db.hget("orders",order_id))
        if order["current_state"]=="ACCEPTED":
            values = request.get_json()
            if values["status"]=="started" or values["status"]=="arriving" or values["status"]=="delivered":
                delivery={"id":str(uuid.uuid4()), "current_state":values["status"].upper()}
                order["deliveries"].append(delivery)
                db.hset("orders",order_id,json.dumps(order))
                return '',204
            else:
                return {"error":"The delivery status '"+values["status"]+"' is not accepted. Allowed values: started, arriving, delivered"},400
        else:
            return {"error":"The order state is "+order["current_state"]+". It cannot be updated the delivery status."},409
    else:
        return {"error": "not found"},404


