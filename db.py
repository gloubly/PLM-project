import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
if "db_plm" not in client.list_database_names():
    client["db_plm"]

if "projects" not in client["db_plm"].list_collection_names():
    client["db_plm"]["projects"]

project = {
    "users": [
        {
            "username": "admin",
            "password": "root"
        },

    ],
    "content": {
        "a": "test"
    }
}

client["db_plm"]["projects"].insert_one(project)

project = client["db_plm"]["projects"].find_one({"users":{"$elemMatch":{"username":"admin", "password":"root"}}})

if project:
    print('yay')
else:
    print("loser")