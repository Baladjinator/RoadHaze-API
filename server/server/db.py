from pymongo import mongo_client
from .settings import settings
client = mongo_client.MongoClient(settings.DATABASE_URL)

db = client[settings.MONGO_INITDB_DATABASE]
User = db.users
Camera = db.posts

User.create_index("email", unique=True)
Camera.create_index("id", unique=True)