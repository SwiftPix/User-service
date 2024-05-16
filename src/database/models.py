import bcrypt
from main import create_app

app = create_app()

db = app.mongo_db


class User:
    def __init__(self, name, email, cellphone, hash_password, salt):
        self.name = name
        self.email = email
        self.cellphone = cellphone
        self.hash_password = hash_password
        self.salt = salt

    @staticmethod
    def create_hash_password(password):
        salt = bcrypt.gensalt()
        hash_password = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hash_password, salt

    def save(self):
        user = {
           "name": self.name,
           "email": self.email,
           "cellphone": self.cellphone,
           "hash_password": self.hash_password,
           "salt": self.salt
        }
        result = db.users.insert_one(user)

        return result._id
    
    def find_by_email(email):
        result = db.users.find_one({"email": email})
        return result
