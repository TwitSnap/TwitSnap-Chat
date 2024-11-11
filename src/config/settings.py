from dotenv import load_dotenv
from utils.logger import Logger
import os


load_dotenv()
DB_URI = os.getenv("DB_URI")
LOG_LEVEL = os.getenv("LOG_LEVEL")
LOG_PATH = os.getenv("LOG_PATH")
DB_NAME = os.getenv("DB_NAME")

logger = Logger(level=LOG_LEVEL, log_file=LOG_PATH)
