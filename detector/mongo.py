from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
db = client["spamshield"]
users_collection = db["users"]
history_collection = db["history"]