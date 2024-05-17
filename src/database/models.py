from datetime import datetime, timezone
import bcrypt
import pymongo

from settings import settings
from utils.index import default_datetime

db_client = pymongo.MongoClient(settings.MONGO_DATABASE_URI)
db = db_client.get_database(settings.MONGO_DATABASE_NAME)

class User:
    def __init__(self, name, email, cellphone, password, salt):
        self.name = name
        self.email = email
        self.cellphone = cellphone
        self.password = password
        self.salt = salt

    @staticmethod
    def create_hash_password(password):
        salt = bcrypt.gensalt()
        hash_password = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hash_password, salt
    
    @staticmethod
    def default_datetime():
        return datetime.now().astimezone(timezone.utc)

    def save(self):
        user = {
            "name": self.name,
            "email": self.email,
            "cellphone": self.cellphone,
            "password": self.password,
            "salt": self.salt,
            "created_at": default_datetime(),
            "updated_at": default_datetime(),
        }
        result = db.users.insert_one(user)
        return result.inserted_id
    
    def find_by_email(email):
        result = db.users.find_one({"email": email})
        return result
