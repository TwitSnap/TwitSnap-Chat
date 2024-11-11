from config.settings import logger
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from config.settings import DB_URI, DB_NAME


class Database:
    def __init__(self, uri: str, db_name: str):
        self.uri = uri
        self.client = None
        self.db_name = db_name
        self.db = None

    def connect(self):
        self.client = MongoClient(DB_URI, server_api=ServerApi('1'))
        self.db = self.client[self.db_name]
        try:
            self.client.admin.command('ping')
            logger.info(f"Database connection established successfully at {self.uri}")
        except Exception as e:
            print(e)

    def get_db(self):
        return self.db

    async def disconnect(self):
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")

db = Database(DB_URI, DB_NAME)
