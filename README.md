# OrderShop
Redis as an event store in a microservices architecture.

See https://redislabs.com/blog/use-redis-event-store-communication-microservices for a detailed description.

## Start
- `docker-compose up`

## Test menu, order and store microservices

- `pytest -v test_order_service.py`
- `pytest -v test_menu_service.py`
- `pytest -v test-store-api.py`

## Stop
- `docker-compose down`
