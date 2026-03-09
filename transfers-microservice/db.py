import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("MONGO_URI")
client = MongoClient(uri, serverSelectionTimeoutMS=3000)
db = client.get_default_database()
