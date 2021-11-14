import json

import requests

from flask import request
from flask import Flask

from common.utils import check_rsp_code



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

@app.route("/store-metrics",methods=['GET'])
@app.route('/stores', methods=['GET'])
@app.route('/store/<store_id>', methods=['GET'])
@app.route('/store/<store_id>/status', methods=['GET'])
@app.route('/store/<store_id>/setStatus', methods=['POST', 'GET'])
@app.route('/store/<store_id>/holiday-hours', methods=['GET'])
@app.route('/store/<store_id>/setHoliday-hours', methods=['POST', 'GET'])
def store_command(store_id=None):
    return proxy_command_request('http://store-service:5000{}')


@app.route('/order', methods=['POST'])
@app.route('/order/<order_id>', methods=['GET'])
@app.route('/stores/<store_id>/created-orders', methods=['GET'])
@app.route('/stores/<store_id>/canceled-orders', methods=['GET'])
@app.route('/orders/<order_id>/accept_pos_order', methods=['POST'])
@app.route('/orders/<order_id>/deny_pos_order', methods=['POST'])
@app.route('/orders/<order_id>/cancel', methods=['POST'])
@app.route('/orders/<order_id>/restaurantdelivery/status', methods=['POST'])
def order_command(order_id=None, store_id=None):
    return proxy_command_request('http://order-service:5000{}')

@app.route('/<store_id>/menus', methods=['GET'])
@app.route('/<store_id>/menus', methods=['PUT'])
@app.route('/<store_id>/menus/items', methods=['POST'])
def menu_command(store_id=None):
    return proxy_command_request('http://menu-service:5000{}')

@app.route('/authentication/get_token', methods=['POST'])
def authentication_command():
    return '',204
    return proxy_command_request('http://authentication-service:5000{}')
