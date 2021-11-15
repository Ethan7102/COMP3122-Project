# 3.1 Test case of store service

The test case of store service contains four test cases.

1. List All Stores response code 200
2. List All Stores check return json
3. Get Store with id response code 200
4. Get Store with id check return json
5. Get Store status with id response code 200
6. Get Store status with id check return json
7. Set Store status with id response code 200
8. Set Store status with id check return json
9. Test listener service response code 200
10. Get Store holiday_hours response code 200
11. Get Store holiday_hours check return json
12. Set Store holiday_hours response code 200
13. Set Store holiday_hours check return json

To run the test, we need to install pytest & redis, Execute

python3 -m pip install pytest

python3 -m pip install redis

After installed the pytest, Execute

python3 -m pytest -v test_store_service.py



# 3.2 supporting services by store microservice

The store microservice support various functions as follows:


1. Show the list of all stores

'/stores'

curl -v http://localhost:5000/stores -H 'authorization: 740becc4b623786cc812c956a5afb30e'


2. Show the store info with specific store id

'/store/< store_id >' 

curl -v http://localhost:5000/store/7e973b58-40b7-4bd8-b01c-c7d1cbd194f6 -H 'authorization: 740becc4b623786cc812c956a5afb30e'



3. show the store status with specific store id

'/store/< store_id >/status'

curl -v http://localhost:5000/store/7e973b58-40b7-4bd8-b01c-c7d1cbd194f6/status -H 'authorization: 740becc4b623786cc812c956a5afb30e'


4. set store restaurant status with specific store id at this example, set to PAUSED

'/store/< store_id >/setStatus'

curl -v -H 'authorization: 740becc4b623786cc812c956a5afb30e' http://localhost:5000/store/7e973b58-40b7-4bd8-b01c-c7d1cbd194f6/setStatus?newStatus=PAUSED&reason=NA


5. show the holiday_hours with specific store id

'/store/< store_id >/holiday-hours'

curl -v http://localhost:5000/store/7e973b58-40b7-4bd8-b01c-c7d1cbd194f6/holiday-hours -H 'authorization: 740becc4b623786cc812c956a5afb30e'

6. set store restaurant status with specific store id

'/store/< store_id >/setHoliday-hours'

curl -v http://localhost:5000/store/7e973b58-40b7-4bd8-b01c-c7d1cbd194f6/setHoliday-hours?jsonInputString=%7B%20%22holiday_hours%22%3A%20%7B%20%222020-12-24%22%3A%20%7B%20%22open_time_periods%22%3A%20%5B%20%7B%20%22start_time%22%3A%20%2200%3A00%22%2C%20%22end_time%22%3A%20%2200%3A00%22%20%7D%20%5D%20%7D%20%7D%20%7D -H 'authorization: 740becc4b623786cc812c956a5afb30e'

7. see metrics of store api

'/store-metrics'

curl -v http://localhost:5000/store-metrics -H 'authorization: 740becc4b623786cc812c956a5afb30e'

