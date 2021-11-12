* /order: create an order
```
curl -X POST -v http://localhost:5000/order -H 'Content-Type: application/json' -d @./order_service/sample_order_data.json
```

* /order/<order_id>: get an order
```
curl -v http://localhost:5000/order/f9f363d1-e1c2-4595-b477-c649845bc953
```

* /orders/<order_id>/accept_pos_order: accept an order
```
curl -X POST -v http://localhost:5000/orders/f9f363d1-e1c2-4595-b477-c649845bc953/accept_pos_order -H 'Content-Type: application/json' -d '{"reason": "accepted"}'
```