import pymongo

#setup the db
client = pymongo.MongoClient("mongodb://localhost:27017/")
if "db_plm" not in client.list_database_names():
    client["db_plm"]

collections = ["users", "products"]


for col in collections:
    if  col in client["db_plm"].list_collection_names():
        client.drop(col)
    client["db_plm"][col]

users = [
    {
        "username": "admin",
        "password": "root",
    },
    {
        "username": "username",
        "password": "password",
    },
]

client["db_plm"]["users"].insert_many(users)

products = [
    { "name": "Milk", "category": "Dairy","launching_date": "2024-01-01","conservation_date": "2024-03-01","milk_type_used": "Perishable","ingredients": "Milk","properties": "Rich in calcium"    },
    { "name": "Shampoo1", "category": "Personal Care","launching_date": "2022-05-01","conservation_date": "2025-05-01","milk_type_used": "Non-perishable","ingredients": "Aqua, Sodium Laureth Sulfate","properties": "Cleans hair"    },
    { "name": "Shampoo2", "category": "Personal Care", "launching_date": "2022-05-01","conservation_date": "2025-05-01","milk_type_used": "Non-perishable","ingredients": "Aqua, Sodium Laureth Sulfate","properties": "Cleans hair"}, 
    { "name": "Shampoo3", "category": "Personal Care", "launching_date": "2022-05-01","conservation_date": "2025-05-01","milk_type_used": "Non-perishable","ingredients": "Aqua, Sodium Laureth Sulfate","properties": "Cleans hair"}, 
    { "name": "Shampoo4", "category": "Personal Care", "launching_date": "2022-05-01","conservation_date": "2025-05-01","milk_type_used": "Non-perishable","ingredients": "Aqua, Sodium Laureth Sulfate","properties": "Cleans hair"    }, 
    { "name": "Shampoo5", "category": "Personal Care", "launching_date": "2022-05-01","conservation_date": "2025-05-01","milk_type_used": "Non-perishable","ingredients": "Aqua, Sodium Laureth Sulfate","properties": "Cleans hair"    },
    { "name": "Shampoo", "category": "Personal Care", "launching_date": "2022-05-01","conservation_date": "2025-05-01","milk_type_used": "Non-perishable","ingredients": "Aqua, Sodium Laureth Sulfate","properties": "Cleans hair"    }, 
    { "name": "Shampo5o", "category": "Personal Care", "launching_date": "2022-05-01","conservation_date": "2025-05-01","milk_type_used": "Non-perishable","ingredients": "Aqua, Sodium Laureth Sulfate","properties": "Cleans hair"    }, 
    { "name": "Shampo1o", "category": "Personal Care", "launching_date": "2022-05-01","conservation_date": "2025-05-01","milk_type_used": "Non-perishable","ingredients": "Aqua, Sodium Laureth Sulfate","properties": "Cleans hair"    }, 
    { "name": "Shampo1o", "category": "Personal Care", "launching_date": "2022-05-01","conservation_date": "2025-05-01","milk_type_used": "Non-perishable","ingredients": "Aqua, Sodium Laureth Sulfate","properties": "Cleans hair"    }, 
    { "name": "Shampoo", "category": "Personal Care", "launching_date": "2022-05-01","conservation_date": "2025-05-01","milk_type_used": "Non-perishable","ingredients": "Aqua, Sodium Laureth Sulfate","properties": "Cleans hair"    }, 
    { "name": "Shampoo", "category": "Personal Care", "launching_date": "2022-05-01","conservation_date": "2025-05-01","milk_type_used": "Non-perishable","ingredients": "Aqua, Sodium Laureth Sulfate","properties": "Cleans hair"    }, 
    { "name": "Shamp1oo", "category": "Personal Care", "launching_date": "2022-05-01","conservation_date": "2025-05-01","milk_type_used": "Non-perishable","ingredients": "Aqua, Sodium Laureth Sulfate","properties": "Cleans hair"    }, 
    { "name": "Shampoo", "category": "Personal Care", "launching_date": "2022-05-01","conservation_date": "2025-05-01","milk_type_used": "Non-perishable","ingredients": "Aqua, Sodium Laureth Sulfate","properties": "Cleans hair"    }, 
    { "name": "Shampoo", "category": "Personal Care", "launching_date": "2022-05-01","conservation_date": "2025-05-01","milk_type_used": "Non-perishable","ingredients": "Aqua, Sodium Laureth Sulfate","properties": "Cleans hair"    }, 
    { "name": "Sham52poo", "category": "Personal Care", "launching_date": "2022-05-01","conservation_date": "2025-05-01","milk_type_used": "Non-perishable","ingredients": "Aqua, Sodium Laureth Sulfate","properties": "Cleans hair"    }, 
    { "name": "Shampoo", "category": "Personal Care", "launching_date": "2022-05-01","conservation_date": "2025-05-01","milk_type_used": "Non-perishable","ingredients": "Aqua, Sodium Laureth Sulfate","properties": "Cleans hair"    }, 
    { "name": "Sham48poo", "category": "Personal Care", "launching_date": "2022-05-01","conservation_date": "2025-05-01","milk_type_used": "Non-perishable","ingredients": "Aqua, Sodium Laureth Sulfate","properties": "Cleans hair"    }, 
    { "name": "Shampoo", "category": "Personal Care", "launching_date": "2022-05-01","conservation_date": "2025-05-01","milk_type_used": "Non-perishable","ingredients": "Aqua, Sodium Laureth Sulfate","properties": "Cleans hair"    }, 
    { "name": "Sham84poo", "category": "Personal Care", "launching_date": "2022-05-01","conservation_date": "2025-05-01","milk_type_used": "Non-perishable","ingredients": "Aqua, Sodium Laureth Sulfate","properties": "Cleans hair"    },
    { "name": "Shampoo", "category": "Personal Care", "launching_date": "2022-05-01","conservation_date": "2025-05-01","milk_type_used": "Non-perishable","ingredients": "Aqua, Sodium Laureth Sulfate","properties": "Cleans hair"    }, 
    { "name": "Shampoo", "category": "Personal Care", "launching_date": "2022-05-01","conservation_date": "2025-05-01","milk_type_used": "Non-perishable","ingredients": "Aqua, Sodium Laureth Sulfate","properties": "Cleans hair"    }, 
    { "name": "Sham84poo", "category": "Personal Care", "launching_date": "2022-05-01","conservation_date": "2025-05-01","milk_type_used": "Non-perishable","ingredients": "Aqua, Sodium Laureth Sulfate","properties": "Cleans hair"    }, 
    { "name": "Shamp84oo", "category": "Personal Care", "launching_date": "2022-05-01","conservation_date": "2025-05-01","milk_type_used": "Non-perishable","ingredients": "Aqua, Sodium Laureth Sulfate","properties": "Cleans hair"    }, 
    { "name": "Shampoo", "category": "Personal Care", "launching_date": "2022-05-01","conservation_date": "2025-05-01","milk_type_used": "Non-perishable","ingredients": "Aqua, Sodium Laureth Sulfate","properties": "Cleans hair"    }, 
    { "name": "Sham8poo", "category": "Personal Care", "launching_date": "2022-05-01","conservation_date": "2025-05-01","milk_type_used": "Non-perishable","ingredients": "Aqua, Sodium Laureth Sulfate","properties": "Cleans hair"    }, 
    { "name": "Shampoo", "category": "Personal Care", "launching_date": "2022-05-01","conservation_date": "2025-05-01","milk_type_used": "Non-perishable","ingredients": "Aqua, Sodium Laureth Sulfate","properties": "Cleans hair"    }, 
    { "name": "Sha7mpoo", "category": "Personal Care", "launching_date": "2022-05-01","conservation_date": "2025-05-01","milk_type_used": "Non-perishable","ingredients": "Aqua, Sodium Laureth Sulfate","properties": "Cleans hair"    }, 
    { "name": "Shampoo", "category": "Personal Care", "launching_date": "2022-05-01","conservation_date": "2025-05-01","milk_type_used": "Non-perishable","ingredients": "Aqua, Sodium Laureth Sulfate","properties": "Cleans hair"    }, 
    { "name": "Sham8poo", "category": "Personal Care", "launching_date": "2022-05-01","conservation_date": "2025-05-01","milk_type_used": "Non-perishable","ingredients": "Aqua, Sodium Laureth Sulfate","properties": "Cleans hair"    }, 
    { "name": "Shampoo", "category": "Personal Care", "launching_date": "2022-05-01","conservation_date": "2025-05-01","milk_type_used": "Non-perishable","ingredients": "Aqua, Sodium Laureth Sulfate","properties": "Cleans hair"    }, 
    { "name": "Sham7poo", "category": "Personal Care", "launching_date": "2022-05-01","conservation_date": "2025-05-01","milk_type_used": "Non-perishable","ingredients": "Aqua, Sodium Laureth Sulfate","properties": "Cleans hair"    }, 
    { "name": "Shamp4oo", "category": "Personal Care", "launching_date": "2022-05-01","conservation_date": "2025-05-01","milk_type_used": "Non-perishable","ingredients": "Aqua, Sodium Laureth Sulfate","properties": "Cleans hair"    }, 
    { "name": "Shamp4oo", "category": "Personal Care", "launching_date": "2022-05-01","conservation_date": "2025-05-01","milk_type_used": "Non-perishable","ingredients": "Aqua, Sodium Laureth Sulfate","properties": "Cleans hair"    }, 
    { "name": "Shampo2o", "category": "Personal Care", "launching_date": "2022-05-01","conservation_date": "2025-05-01","milk_type_used": "Non-perishable","ingredients": "Aqua, Sodium Laureth Sulfate","properties": "Cleans hair"    }, 
    { "name": "Shamp23oo", "category": "Personal Care", "launching_date": "2022-05-01","conservation_date": "2025-05-01","milk_type_used": "Non-perishable","ingredients": "Aqua, Sodium Laureth Sulfate","properties": "Cleans hair"    }, 
    { "name": "Shampoo", "category": "Personal Care", "launching_date": "2022-05-01","conservation_date": "2025-05-01","milk_type_used": "Non-perishable","ingredients": "Aqua, Sodium Laureth Sulfate","properties": "Cleans hair"    }, 
    { "name": "Shampo2o", "category": "Personal Care", "launching_date": "2022-05-01","conservation_date": "2025-05-01","milk_type_used": "Non-perishable","ingredients": "Aqua, Sodium Laureth Sulfate","properties": "Cleans hair"    }, 
    { "name": "Shamp2oo", "category": "Personal Care", "launching_date": "2022-05-01","conservation_date": "2025-05-01","milk_type_used": "Non-perishable","ingredients": "Aqua, Sodium Laureth Sulfate","properties": "Cleans hair"    }, 
    { "name": "Shampoo", "category": "Personal Care", "launching_date": "2022-05-01","conservation_date": "2025-05-01","milk_type_used": "Non-perishable","ingredients": "Aqua, Sodium Laureth Sulfate","properties": "Cleans hair"    }, 
    { "name": "Shamp1oo", "category": "Personal Care", "launching_date": "2022-05-01","conservation_date": "2025-05-01","milk_type_used": "Non-perishable","ingredients": "Aqua, Sodium Laureth Sulfate","properties": "Cleans hair"    }, 
    { "name": "Shamp48oo", "category": "Personal Care", "launching_date": "2022-05-01","conservation_date": "2025-05-01","milk_type_used": "Non-perishable","ingredients": "Aqua, Sodium Laureth Sulfate","properties": "Cleans hair"    }, 
    { "name": "Shamp8oo", "category": "Personal Care", "launching_date": "2022-05-01","conservation_date": "2025-05-01","milk_type_used": "Non-perishable","ingredients": "Aqua, Sodium Laureth Sulfate","properties": "Cleans hair"    }, 
    { "name": "Shamp9oo", "category": "Personal Care", "launching_date": "2022-05-01","conservation_date": "2025-05-01","milk_type_used": "Non-perishable","ingredients": "Aqua, Sodium Laureth Sulfate","properties": "Cleans hair"    }, 
    { "name": "Shamp6oo", "category": "Personal Care", "launching_date": "2022-05-01","conservation_date": "2025-05-01","milk_type_used": "Non-perishable","ingredients": "Aqua, Sodium Laureth Sulfate","properties": "Cleans hair"    },
]


req = client["db_plm"]["users"].find_one({"username":"admin", "password":"root"})

if req:
    print('yay')
else:
    print("loser")