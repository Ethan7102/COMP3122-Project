import redis
import json

pool = redis.ConnectionPool(host='localhost', port=6381, decode_responses=True)
db = redis.Redis(connection_pool=pool)


BASE_URL = 'http://localhost:5000'

temp={"name": "East Coast Sushi", "store_id": "7e973b58-40b7-4bd8-b01c-c7d1cbd194f6", "location": { "address": "636 W 28th Street", "address_2": "Floor 3", "city": "New York", "country": "US", "postal_code": "10001", "state": "NY", "latitude": 40.7527198, "longitude": -74.00635 }, "contact_emails": [ "owner@example.com", "announcements+uber@example.com", "store-east@example.com" ], "raw_hero_url": "https://www.example.com/hero_url_east.png", "price_bucket": "$$$", "avg_prep_time": 5,"status": "active","partner_store_id": "541324","timezone": "America/New_York"}
db.hset("stores", "7e973b58-40b7-4bd8-b01c-c7d1cbd194f6",json.dumps(temp))
db.hset("stores", "sdfsdfsdfsdfsdfsdfsdfsdfsdfsdfsdfsdf",json.dumps(temp))



temp2={ "holiday_hours": { "2019-12-10": { "open_time_periods": [ { "start_time": "00:00", "end_time": "16:00" }, { "start_time": "18:00", "end_time": "23:30" } ] }, "2019-12-11": { "open_time_periods": [ { "start_time": "00:00", "end_time": "23:59" } ] } } }
db.hset("holidayHours", "7e973b58-40b7-4bd8-b01c-c7d1cbd194f6",json.dumps(temp2))
db.hset("holidayHours", "sdfsdfsdfsdfsdfsdfsdfsdfsdfsdfsdfsdf",json.dumps(temp2))





print(db.hget("stores", "7e973b58-40b7-4bd8-b01c-c7d1cbd194f6"))
print("\n")
print(db.hget("holidayHours", "7e973b58-40b7-4bd8-b01c-c7d1cbd194f6"))


print("\n")
print("\n")
print("\n")


print(db.hgetall("stores"))