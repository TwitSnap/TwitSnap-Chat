from dotenv import load_dotenv
from utils.logger import Logger
import os


load_dotenv()
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DB_URI = os.getenv("DB_URI")
LOG_LEVEL = os.getenv("LOG_LEVEL")
LOG_PATH = os.getenv("LOG_PATH")
DB_NAME = os.getenv("DB_NAME")
USER_API_URI = os.getenv("USER_API_URI")
USER_API_GET_USER_PATH = os.getenv("USER_API_GET_USER_PATH")
NOTIFICATION_API_URI = os.getenv("NOTIFICATION_API_URI")
NOTIFICATION_API_SEND_PATH = os.getenv("NOTIFICATION_API_SEND_PATH")
API_KEY = os.getenv("API_KEY")
logger = Logger(level=LOG_LEVEL, log_file=LOG_PATH)
