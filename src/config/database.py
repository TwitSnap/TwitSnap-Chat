from config.settings import logger
from motor.motor_asyncio import AsyncIOMotorClient
from config.settings import DB_URI, DB_NAME


class Database:
    def __init__(self, uri: str, db_name: str):
        self.uri = uri
        self.client = None
        self.db_name = db_name
        self.db = None

    def connect(self):
        self.client = AsyncIOMotorClient(DB_URI)
        self.db = self.client.get_database(DB_NAME)
        try:
            self.client.admin.command("ping")
            logger.info(f"Database connection established successfully at {self.uri}")
            return self.db
        except Exception as e:
            print(e)

    def get_db(self):
        if self.db is None:
            logger.error("Database is not connected")
            return None
        return self.db

    def disconnect(self):
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")


db = Database(DB_URI, DB_NAME)
db = db.connect()
