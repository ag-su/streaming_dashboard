import os
from pymongo import MongoClient

from dotenv import load_dotenv
load_dotenv()
# ========== db ==========

def get_db(db_name):
    connection_string = f"mongodb+srv://{os.getenv('DB_USER')}:{os.getenv('DB_PWD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    client = MongoClient(connection_string) # MongoClient 객체 생성

    db = client[db_name]

    return db


# ========== 백엔드 URI ========== 
uri = os.getenv('URI')