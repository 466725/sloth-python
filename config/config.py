# Load .env file for environment variables.
from dotenv import load_dotenv
import os

load_dotenv()

# Access environment variables
DB_SERVER = os.getenv("DB_SERVER")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")  

class Config: 
    DB_SERVER = DB_SERVER
    DB_DATABASE = DB_DATABASE
    DB_USER = DB_USER
    DB_PASSWORD = DB_PASSWORD
    
    @staticmethod
    def get_connection():
        from utils.data_base import db_wrapper
        return db_wrapper.get_connection(Config)    
    