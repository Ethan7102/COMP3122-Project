import json
import requests
import uuid
import time
import redis
from flask import request
from flask import Flask, jsonify
from urllib.parse import unquote
from flask import Response
import prometheus_client
from prometheus_client.core import CollectorRegistry
from prometheus_client import Summary, Counter, Histogram, Gauge

app = Flask(__name__)
_INF = float("inf")
graphs = {}
graphs['c'] = Counter('python_request_operations_total', 'The total number of processed requests')
graphs['h'] = Histogram('python_request_duration_seconds', 'Histogram for the duration in seconds.', buckets=(1, 2, 5, 6, 10, _INF))

def connect_db():
    pool = redis.ConnectionPool(host='redis-order-service', port=6379, decode_responses=True)
    db = redis.Redis(connection_pool=pool)
    return db


@app.route('/order', methods=['POST'])#receive a order 
def handle_order():
    graphs['c'].inc()
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
        
        #check the event bus whether store is active
        if db.hexists("storeStatus", values["store"]["id"]):
            return {"Error": "Store not available"},409
        
        db.hset("orders",values["id"],json.dumps(values))
        return {"message":"order is created"}, 200

@app.route('/order/<order_id>', methods=['GET'])
def get_order(order_id):
    graphs['c'].inc()
    db=connect_db()
    
    if db.hexists("orders", order_id):
        return json.loads(db.hget("orders",order_id)), 200
    else:
        return {"error": "not found"},404

@app.route('/stores/<store_id>/created-orders', methods=['GET']) # get orders of a specific store with status "CREATED"
def get_created_orders(store_id):
    # get data from query parameters
    graphs['c'].inc()
    limit = -1
    if 'limit' in request.args:
        limit = int(request.args['limit'])
    db=connect_db()
    orders_keys=db.hkeys("orders")
    created_orders= {"orders":[]}
    count=0
    for orders_key in orders_keys:    
        order = json.loads(db.hget("orders",orders_key))
        if order["current_state"] == "CREATED" and order["store"]["id"] == store_id:
            created_orders["orders"].append({"id":orders_key, "current_state":order["current_state"], "placed_at":order["placed_at"]})
            count+=1
        if limit >= 0:
            if limit == count:
                break
    return created_orders,200

@app.route('/stores/<store_id>/canceled-orders', methods=['GET']) # get orders of a specific store with status "CREATED"
def get_canceled_orders(store_id):
    graphs['c'].inc()
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
    graphs['c'].inc()
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
    graphs['c'].inc()
    db=connect_db()
    if db.hexists("orders", order_id):
        order = json.loads(db.hget("orders",order_id))
        if order["current_state"]=="CREATED" or order["current_state"]=="ACCEPTED":
            order["current_state"]="DENIED"
            db.hset("orders",order_id,json.dumps(order))
            return '',204
        else:
            return {"error":"The order state is "+order["current_state"]+". Only the order with order state CREATED can be denied."},409
    else:
        return {"error": "not found"},404

@app.route('/orders/<order_id>/cancel', methods=['POST'])#cancel order
def cancel_order(order_id):
    graphs['c'].inc()
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
    graphs['c'].inc()
    db=connect_db()
    if db.hexists("orders", order_id):
        order = json.loads(db.hget("orders",order_id))
        if order["current_state"]!="CREATED":
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
    
@app.route("/order-metrics", methods=['GET'])
def order_requests_count():
    res = []
    for k,v in graphs.items():
        res.append(prometheus_client.generate_latest(v))
    return Response(res, mimetype="text/plain")


