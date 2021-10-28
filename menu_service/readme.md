# Execute following command to create a docker volume and connect to db (mongo database)
docker-compose up
# Execute following command to run app.py
python app.py

# The menu microservice contains three main functions
# 1. Read specific stores'menu
# To view the menu, type url 
# <store_id> based on which store's menu you want to see
http://localhost:15000/stores/<store_id>/menus

# 2. Upload specific stores'menu
# To add menu (here we use data.json) to database , execute the following command
# <store_id> based on which store you want to add menu e.g. C123
curl -X PUT -d @data.json \ 2 -H "Content-Type: application/json" -v http://localhost:15000/stores/<store_id>/menus

# 3. Update stores'menu item





