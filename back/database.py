from pymongo import MongoClient
from dotenv import dotenv_values
config = dotenv_values(".env")

try:
    client = MongoClient(config["MONGO_CONNECT"])
    db = client[config["DB_NAME"]]
    collection = db[config["COLLECTION"]]
except Exception as ex:
    print(f"ERROR: connection to DB - {ex}")
