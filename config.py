import os

# MongoDB Configuration
MONGO_URI = 'mongodb://mongo_db:27017/'
MONGO_DB = 'mydatabase'

# Redis Configuration
REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))

# JWT Configuration
JWT_SECRET_KEY = 'super-secret'
