from pymongo import mongo_client, GEOSPHERE
from .settings import settings
client = mongo_client.MongoClient(settings.DATABASE_URL)

db = client[settings.MONGO_INITDB_DATABASE]
User = db.users
Camera = db.cameras

User.create_index("email", unique=True)
# Camera.create_index([("location", GEOSPHERE)])