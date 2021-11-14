# OrderShop
Redis as an event store in a microservices architecture.

See https://redislabs.com/blog/use-redis-event-store-communication-microservices for a detailed description.

## Start
- `docker-compose up`

## Test
- `python3 -m unittest client/client.py`
- `pytest -v test_order_service.py`

## Stop
- `docker-compose down`
