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

* /orders/<order_id>/deny_pos_order: deny an order
```
curl -X POST -v http://localhost:5000/orders/f9f363d1-e1c2-4595-b477-c649845bc953/deny_pos_order -H 'Content-Type: application/json' -d '{ "reason": { "explanation":"failed to submit order", "code":"ITEM_AVAILABILITY", "out_of_stock_items":[ "540cb880-0286-417b-9c6c-be586fd50f76", "094f3308-4389-4ce5-bf30-ce9e09c6ed1c" ], "invalid_items":[ "1cd26db9-6be3-4b0a-9216-e4868c5d79ec" ] } }'
```

* /orders/<order_id>/cancel: cancel an order
```
curl -X POST -v http://localhost:5000/orders/f9f363d1-e1c2-4595-b477-c649845bc953/cancel -H 'Content-Type: application/json' -d '{"reason":"CANNOT_COMPLETE_CUSTOMER_NOTE","details":"note is impossible"}'
```

* /orders/<order_id>/restaurantdelivery/status
```
curl -X POST -v http://localhost:5000/orders/f9f363d1-e1c2-4595-b477-c649845bc953/restaurantdelivery/status -H 'Content-Type: application/json' -d '{"status": "delivered"}'
```