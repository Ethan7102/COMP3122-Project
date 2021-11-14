## Start
- `docker-compose up`

## Test
- `python3 -m unittest client/client.py`

## Stop
- `docker-compose down`

## Create menu, <store_id>/menus
```
curl -X PUT -v http://localhost:5000/c124/menus -H 'Content-Type: application/json' -d @./menu_service/menu_data.json
```
## Update menu, <store_id>/menus/items
```
curl -X POST -v http://localhost:5000/c124/menus/items -H 'Content-Type: application/json' -d @./menu_service/update_menu.json
```
## get menu, /<store_id>/menus
```
curl -v http://localhost:5000/c124/menus
```
