import pymongo
import json
from datetime import datetime

#setup the db
client = pymongo.MongoClient("mongodb://localhost:27017/")
if "db_plm" not in client.list_database_names():
    client["db_plm"]

database = client["db_plm"]

collections = ["users", "products", "productsHistory", "stock"]
for col in collections:
    if  col in client["db_plm"].list_collection_names():
        database[col].drop()
    database[col]

# TODO convert to datetime
with open('data/products.json', 'r') as f:
    products = json.load(f)
with open('data/productsHistory.json', 'r') as f:
    productsHistory = json.load(f)
with open('data/stock.json', 'r') as f:
    stock = json.load(f)
with open('data/users.json', 'r') as f:
    users = json.load(f)

for product in products:
    product["launching_date"] = datetime.strptime(product["launching_date"], "%Y-%m-%d")
for product in productsHistory:
    product["launching_date"] = datetime.strptime(product["launching_date"], "%Y-%m-%d")

database["products"].insert_many(products)
database["productsHistory"].insert_many(productsHistory)
database["stock"].insert_many(stock)
database["users"].insert_many(users)
print("loaded")
req = database["users"].find_one(users[0])

if req:
    print('yay')
else:
    print("loser")