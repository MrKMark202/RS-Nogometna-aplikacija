import os
from pymongo import MongoClient

uri = os.getenv("MONGO_URI")

client = MongoClient(uri, serverSelectionTimeoutMS=3000)
db = client.get_database()