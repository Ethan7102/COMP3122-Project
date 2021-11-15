import atexit
import json
import os
import re
import requests
import uuid
import time
import redis
import uuid
import time
from flask import request
from flask import Flask, jsonify


app = Flask(__name__)

#listening to event bus, when there is new not active store, print msg
r = redis.Redis(host='redis-event-bus', port=6379, db=0)
sub = r.pubsub()
sub.subscribe('store_status_change_channel')


#db that store the not Available store  
pool = redis.ConnectionPool(host='redis-order-service', port=6379, decode_responses=True)
db = redis.Redis(connection_pool=pool)



#update "storeAvailable" in db
for message in sub.listen():
    if (isinstance(message.get('data'), bytes)):
        storeID = message['data'].decode()
        db.hset("storeStatus", storeID,"notActive" ) 