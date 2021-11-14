import json, uuid, redis
import re
from flask import jsonify 
from datetime import datetime
import requests
# data = '{"test":[{"1":"2","3":"4"}],"test2":"3"}'
# data = json.loads(data)
# print(data["test"][0])
# print(str(uuid.uuid4()))
# order_id = []
# order_id.append(str(uuid.uuid4()))
# order_id.append(str(uuid.uuid4()))
# order_id.append(str(uuid.uuid4()))
# print(order_id)

# pool = redis.ConnectionPool(host='localhost', port=6380, decode_responses=True)
# db = redis.Redis(connection_pool=pool)
# store_id = "c7f1dc2f-fabe-4997-845c-cad26fdcb894"
# orders_keys=db.hkeys("orders")
# created_orders= {"orders":[]}
# orders = []
# timestamps= []
# for orders_key in orders_keys:    
#     order = json.loads(db.hget("orders",orders_key))
#     if order["current_state"] == "CREATED" and order["store"]["id"] == store_id:
#         orders.append({"id":orders_key, "current_state":order["current_state"], "placed_at":order["placed_at"]})
# sorted_orders = sorted(orders, key = lambda x: datetime.strptime(x["placed_at"],'%yyyy-%mm-%ddT%HH:%mm:%ss'))
# print(orders)
# print(created_orders)
# # yyyy-mm-dd'T'HH:mm:ss


# pool = redis.ConnectionPool(
# host='localhost', port=6383, decode_responses=True)
# token = '740becc4b623786cc812c956a5afb30e'
# db = redis.Redis(connection_pool=pool)
# tokens = db.hvals('tokens')
# if token in tokens:
#     print(tokens)

response = requests.post('http://localhost:5000/authentication/get_token', json={"username":"comp3122", "password": "comp3122"})
token = {"authorization": response.json()['token']}