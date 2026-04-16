from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    HOST = os.getenv('DB_HOST')
    PORT = int(os.getenv("DB_PORT"))
    DATABASE = os.getenv('DB_NAME')
    USER = os.getenv('DB_USER')
    PASSWORD = os.getenv('DB_PASSWORD')