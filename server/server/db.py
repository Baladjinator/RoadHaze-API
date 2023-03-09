from pymongo import MongoClient

mongo = 'mongodb://localhost:27017/rh-db'
client = MongoClient(mongo)
db = client['rh-db']

cameras = db['cameras']
users = db['users']

