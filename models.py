from pymongo import MongoClient
from config import MONGO_DB, REDIS_HOST, REDIS_PORT
import redis

# Connect to MongoDB
client = MongoClient('mongodb://mongo_db:27017/')
db = client[MONGO_DB]

# Collection objects
users_collection = db['users']
products_collection = db['products']
# Add more collections as needed

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)