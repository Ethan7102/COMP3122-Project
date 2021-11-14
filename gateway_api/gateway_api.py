import json
from os import terminal_size

import requests
import redis

from flask import request
from flask import Flask

from common.utils import check_rsp_code

initialization = 1

app = Flask(__name__)

def proxy_command_request(_base_url):
    """
    Helper function to proxy POST, PUT and DELETE requests to the according service.

    :param _base_url: The URL of the service.
    """
    # handle GET
    if request.method == 'GET':
        rsp = requests.get(_base_url.format(request.full_path))
        return rsp.json(),rsp.status_code

    # handle POST
    if request.method == 'POST':
        rsp = requests.post(_base_url.format(request.full_path), json=json.loads(request.data))
        if rsp.status_code==204:
            return '',204
        else:    
            return rsp.json(), rsp.status_code

    # handle PUT
    if request.method == 'PUT':
        rsp = requests.put(_base_url.format(request.full_path), json=json.loads(request.data))
        if rsp.status_code==204:
            return '',204
        else:    
            return rsp.json(), rsp.status_code

    # handle DELETE
    if request.method == 'DELETE':
        rsp = requests.delete(_base_url.format(request.full_path))
        return check_rsp_code(rsp)


def initialize():
    pool = redis.ConnectionPool(host='redis-authentication-service', port=6379, decode_responses=True)
    db = redis.Redis(connection_pool=pool)
    db.hset("user", "comp3122", "comp3122")
    initialization = 0
    #set a token for testing
    db.hset("tokens", "test", "740becc4b623786cc812c956a5afb30e")


def authenticating_by_token(token):
    if token is None:
        return False
    if initialization:
        initialize()
    pool = redis.ConnectionPool(host='redis-authentication-service', port=6379, decode_responses=True)
    db = redis.Redis(connection_pool=pool)
    tokens = db.hvals('tokens')
    if token in tokens:
        return True
    else:
        return False

def get_token():
    try:
        token = request.headers['authorization']
    except:
        token = None
    return token

@app.route('/stores', methods=['GET'])
@app.route('/store/<store_id>', methods=['GET'])
@app.route('/store/<store_id>/status', methods=['GET'])
@app.route('/store/<store_id>/setStatus', methods=['POST', 'GET'])
@app.route('/store/<store_id>/holiday-hours', methods=['GET'])
@app.route('/store/<store_id>/setHoliday-hours', methods=['POST', 'GET'])
def store_command(store_id=None):
    if authenticating_by_token(get_token()):
        return proxy_command_request('http://store-service:5000{}')
    else:
        return {"error": "permission denied. your token is incorrect miss. if you don't have it, please register a token by http://localhost:5000/authentication/get_token."}, 403

@app.route('/order', methods=['POST'])
@app.route('/order/<order_id>', methods=['GET'])
@app.route('/stores/<store_id>/created-orders', methods=['GET'])
@app.route('/stores/<store_id>/canceled-orders', methods=['GET'])
@app.route('/orders/<order_id>/accept_pos_order', methods=['POST'])
@app.route('/orders/<order_id>/deny_pos_order', methods=['POST'])
@app.route('/orders/<order_id>/cancel', methods=['POST'])
@app.route('/orders/<order_id>/restaurantdelivery/status', methods=['POST'])
def order_command(order_id=None, store_id=None):
    if authenticating_by_token(get_token()):
        return proxy_command_request('http://order-service:5000{}')
    else:
        return {"error": "permission denied. your token is incorrect miss. if you don't have it, please register a token by http://localhost:5000/authentication/get_token."}, 403


@app.route('/<store_id>/menus', methods=['GET'])
@app.route('/<store_id>/menus', methods=['PUT'])
@app.route('/<store_id>/menus/items', methods=['POST'])
def menu_command(store_id=None):
    if authenticating_by_token(get_token()):
        return proxy_command_request('http://menu-service:5000{}')
    else:
        return {"error": "permission denied. your token is incorrect miss. if you don't have it, please register a token by http://localhost:5000/authentication/get_token."}, 403

@app.route('/menu-metrics', methods=['GET'])
def menu_metrics():
    rsp = requests.get("http://menu-service:5000/menu-metrics")
    return rsp.text,rsp.status_code

@app.route("/store-metrics",methods=['GET'])
def store_metrics():
    rsp = requests.get("http://store-service:5000/store-metrics")
    return rsp.text,rsp.status_code

@app.route("/order-metrics",methods=['GET'])
def order_metrics():
    rsp = requests.get("http://order-service:5000/order-metrics")
    return rsp.text,rsp.status_code


@app.route('/authentication/get_token', methods=['POST'])
def authentication_command():
    return proxy_command_request('http://authentication-service:5000{}')

@app.route("/authentication-metrics",methods=['GET'])
def authentication_metrics():
    rsp = requests.get("http://authentication-service:5000/authentication-metrics")
    return rsp.text,rsp.status_code