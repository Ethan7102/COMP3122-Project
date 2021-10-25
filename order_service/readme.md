* /order/<order_id>: get order
```
curl localhost:15000/order/f9f363d1-e1c2-4595-b477-c649845bc953
```

* /stores/<store_id>/created-orders: get active created orders
```
curl localhost:15000/stores/c7f1dc2f-fabe-4997-845c-cad26fdcb894/created-orders
curl localhost:15000/stores/c7f1dc2f-fabe-4997-845c-cad26fdcb894/created-orders?=2
```


```
curl localhost:15000/stores/c7f1dc2f-fabe-4997-845c-cad26fdcb894/canceled-orders
```