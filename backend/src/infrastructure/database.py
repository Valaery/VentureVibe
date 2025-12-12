from motor.motor_asyncio import AsyncIOMotorClient
from src.config.settings import settings

class Database:
    client: AsyncIOMotorClient = None
    db = None

    def connect(self):
        self.client = AsyncIOMotorClient(settings.MONGODB_URL)
        self.db = self.client[settings.MONGODB_DB]
        print(f"Connected to MongoDB at {settings.MONGODB_URL}")

    def close(self):
        self.client.close()
        print("Closed MongoDB connection")

db = Database()

def get_database():
    return db.db
