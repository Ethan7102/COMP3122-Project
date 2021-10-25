from flask import Flask, jsonify, request
from flask.wrappers import Request
from pymongo import MongoClient
from bson.json_util import dumps
from bson.json_util import loads
import os
import pymongo
from urllib.parse import quote_plus

# get mongodb's username, pwd, host name and port number from environment variables
username = os.getenv('MONGO_USERNAME')
password = os.getenv('MONGO_PASSWORD')
host = os.getenv('MONGO_SERVER_HOST')
port = os.getenv('MONGO_SERVER_PORT')

# The flask API will print an error message and exit if the environment variables about MongoDB are not provided
if username is None or password is None or host is None or port is None:
    print('The environment variables about MongoDB are not provided.')
    exit()

# set url
uri = "mongodb://%s:%s@%s:%s" % (quote_plus(username),
                                 quote_plus(password), quote_plus(host), quote_plus(port))

# connect mongodb
try:
    client = MongoClient(uri)
    client.server_info()  # connect to mongoDB to get the server info
# MongoDB will be accessed unsuccessfully if the environment variables about MongoDB are incorrect.
except pymongo.errors.ServerSelectionTimeoutError:
    print('Access failed. The environment variables about MongoDB are incorrect or the MongoDB server is not available.')
    exit()

# get the University DB
db = client['order']
orders = db['order']

app = Flask(__name__)

# Return a JSON object with my Student ID and Name.
@app.route('/me', methods=['GET'])
def get_me():
    # return my student information by JSON format
    return jsonify({"student_id": "20035673D", "name": "Wong Ming Yuen"}), 200
    
# start flask server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=15000, debug=True)