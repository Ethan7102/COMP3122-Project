* /order: create an order
```
curl -X POST -v http://localhost:5000/order -H 'Content-Type: application/json' -d @./order_service/sample_order_data.json
```

* /authentication/get_token: 
```
curl -X POST -v http://localhost:5000//authentication/get_token -H 'Content-Type: application/json' -d '{"username":"comp3122", "password": "comp3122"}'
```
