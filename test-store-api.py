import pytest
import requests
import json
import redis

pool = redis.ConnectionPool(host='localhost', port=6381, decode_responses=True)
db = redis.Redis(connection_pool=pool)

#insert store 1 for test
tempStore1={"name": "East Coast Sushi", "store_id": "7e973b58-40b7-4bd8-b01c-c7d1cbd194f6", "location": { "address": "636 W 28th Street", "address_2": "Floor 3", "city": "New York", "country": "US", "postal_code": "10001", "state": "NY", "latitude": 40.7527198, "longitude": -74.00635 }, "contact_emails": [ "owner@example.com", "announcements+uber@example.com", "store-east@example.com" ], "raw_hero_url": "https://www.example.com/hero_url_east.png", "price_bucket": "$$$", "avg_prep_time": 5,"status": "active","partner_store_id": "541324","timezone": "America/New_York"}
db.hset("stores", "7e973b58-40b7-4bd8-b01c-c7d1cbd194f6",json.dumps(tempStore1))


#insert store 2 for test
tempStore2={"name": "West Coast Sushi", "store_id": "15e652b8-40b5-4b58-b01d-c7d15bd114d6", "location": { "address": "898 E 25th Street", "address_2": "Floor 2", "city": "New York", "country": "US", "postal_code": "10001", "state": "NY", "latitude": 49.7527198, "longitude": -80.00635 }, "contact_emails": [ "owner@example.com", "announcements+uber@example.com", "store-east@example.com" ], "raw_hero_url": "https://www.example.com/hero_url_east.png", "price_bucket": "$$$", "avg_prep_time": 5,"status": "active","partner_store_id": "541325","timezone": "America/New_York"}
db.hset("stores", "85e652b8-40b5-4b58-b01d-c7d15bd114d6",json.dumps(tempStore2))


#insert holiday_hours of store 1 for test
holiday_hours={ "holiday_hours": { "2019-12-10": { "open_time_periods": [ { "start_time": "00:00", "end_time": "16:00" }, { "start_time": "18:00", "end_time": "23:30" } ] }, "2019-12-11": { "open_time_periods": [ { "start_time": "00:00", "end_time": "23:59" } ] } } }
db.hset("holidayHours", "7e973b58-40b7-4bd8-b01c-c7d1cbd194f6",json.dumps(holiday_hours))


# get token
response = requests.post('http://localhost:5000/authentication/get_token', json={"username":"comp3122", "password": "comp3122"})
token = {"authorization": response.json()['token']}


#print(db.hget("stores", "7e973b58-40b7-4bd8-b01c-c7d1cbd194f6"))
#print("\n")
#print(db.hget("holidayHours", "7e973b58-40b7-4bd8-b01c-c7d1cbd194f6"))
#print("\n")
#print(db.hgetall("stores"))



#-------------------------------------------Unit test for store API start-------------------------------------------------#
#List All Stores
#@app.route("/stores")
def test_store_list_5000_check_status_code_equals_200():
    response = requests.get("http://localhost:5000/stores", headers=token)
    assert response.status_code == 200

def test_store_list_5000_check_return_json():
    response = requests.get("http://localhost:5000/stores", headers=token)
    data = db.hgetall('stores')
    json_data = json.dumps(data)
    json_without_slash = json.loads(json_data)

    assert response.json() == json_without_slash
  

#get store with specific store id
#@app.route("/store/<store_id>")

store_id = "7e973b58-40b7-4bd8-b01c-c7d1cbd194f6"

def test_store_id_5000_check_status_code_equals_200():
    response = requests.get("http://localhost:5000/store/"+ store_id, headers=token)
    assert response.status_code == 200

def test_store_id_5000_check_return_json():
    response = requests.get("http://localhost:5000/store/"+ store_id, headers=token)


    assert response.json() == json.loads(db.hget("stores",store_id))

    



#get store status with specific store id
#@app.route('/store/<store_id>/status')
def test_get_status_5000_check_status_code_equals_200():
    response = requests.get("http://localhost:5000/store/"+ store_id+ "/status", headers=token)
    assert response.status_code == 200

def test_get_status_5000_check_return_json():
    response = requests.get("http://localhost:5000/store/"+ store_id + "/status", headers=token)
    json_data = json.loads(db.hget("stores","7e973b58-40b7-4bd8-b01c-c7d1cbd194f6"))
    result = '{ "status" : ' + '"'+ json_data["status"] +'"' + ',' + '"offlineReason"'+' : ' +  '"N/A"' +'}'
    assert response.json() == result




#set store status with specific store id
#@app.route('/store/<store_id>/setStatus')
def test_set_status_5000_check_status_code_equals_200():

    newStatus = "PAUSED"
    reason = 'NA'
    response = requests.get("http://localhost:5000/store/" +store_id+ "/setStatus?newStatus="+newStatus+"&reason="+reason, headers=token)

    assert response.status_code == 200

def test_set_status_5000_check_return_json():
    response = requests.get("http://localhost:5000/store/" +store_id+ "/status", headers=token)
    result = '{ "status" : ' + '"'+ '"PAUSED"' +'"' + ',' + '"offlineReason"'+' : ' +  '"NA"' +'}'
    
    assert response.json() == result


#get store holiday-hours with specific store id
#@app.route('/store/<store_id>/holiday-hours')
def test_get_holiday_hours_5000_check_status_code_equals_200():
    response = requests.get("http://localhost:5000/store/" +store_id+ "/holiday-hours", headers=token)
    assert response.status_code == 200

def test_get_status_5000_check_return_json():
    response = requests.get("http://localhost:5000/store/" +store_id+ "/holiday-hours", headers=token)
    json_data = json.loads(db.hget("holidayHours",store_id))

    assert response.json() == json_data



#set store holiday-hours with specific store id
#@app.route('store/<store_id>/setHoliday-hours')
def test_set_holiday_hours_5000_check_status_code_equals_200():


    response = requests.get("http://localhost:5000/store/" +store_id+ "/setHoliday-hours?jsonInputString=%7B%20%22holiday_hours%22%3A%20%7B%20%222020-12-24%22%3A%20%7B%20%22open_time_periods%22%3A%20%5B%20%7B%20%22start_time%22%3A%20%2200%3A00%22%2C%20%22end_time%22%3A%20%2200%3A00%22%20%7D%20%5D%20%7D%20%7D%20%7D", headers=token)

    assert response.status_code == 200

def test_set_status_5000_check_return_json():


    response = requests.get("http://localhost:5000/store/" +store_id+ "/holiday-hours", headers=token)
    json_data = json.loads(db.hget("holidayHours",store_id))


    jsonInputString={'holiday_hours': {'2020-12-24': {'open_time_periods': [{'end_time': '00:00', 'start_time': '00:00'}]}}}

    #remove backslash
    json_data = json.dumps(jsonInputString)
    json_without_slash = json.loads(json_data)

    assert response.json() == json_without_slash



    #-------------------------------------------Unit test for store API end-------------------------------------------------#