import os
from flask import Flask, jsonify, request
from pymongo import MongoClient
import json
from bson import ObjectId

app = Flask(__name__)

#connect flask to mongodb
def get_db():
    # user = 'project'
    # password = '12345'
    # host = 'mongo'
    # port = 27017
    # client = MongoClient("mongodb://project:12345@mongo:27017")

    client = MongoClient(port=27017,
                         username='project',
                         password='pass')
    db = client['menu_db']
    return db

@app.route("/")
def home_page():
    return 'hi!'

@app.route("/stores/<store_id>/menus", methods=['GET','PUT'])
def get_menu(store_id):

    if(request.method == 'GET'):
        db = get_db()
        menu = db.menu.find({'store_id': {'$eq': store_id}}, {'_id': 0})
        dicts = [doc for doc in menu]
        if len(dicts):  # return order details if it is not empty
            return jsonify(dicts), 200
        else:  # print error message if no order with the specified order ID is found
            return jsonify({'error': 'not found'}), 404
    elif(request.method == 'PUT'):
        db = get_db()
        #convert json data from request body to python dict
        data = request.json
        db.menu.insert_one(data)
        return jsonify({"message: success "}),200


@app.route("/stores/<store_id>/menus/items/<item_id>",methods=['GET','POST'])
def update_menu(store_id,item_id):
    db = get_db()
    #convert json data from request body to python dict
    # 'store_id': {'$eq': store_id},
    if(request.method == 'GET'):
        menu = db.menu.find({'_id': 0}, {'items' :{'$slice' : [1, 5]}})

        dicts = [doc for doc in menu]
        if len(dicts):  # return order details if it is not empty
            return jsonify(dicts), 200
    elif(request.method == 'POST'):
        data = request.json
        db.menu.insert_one(data)
        return jsonify({"message: success "}),200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=15000, debug=True, use_reloader=True)