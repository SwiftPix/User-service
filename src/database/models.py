import bcrypt
import pymongo

from bson.objectid import ObjectId
from settings import settings
from utils.index import default_datetime

db_client = pymongo.MongoClient(settings.MONGO_DATABASE_URI)
db = db_client.get_database(settings.MONGO_DATABASE_NAME)

class User:
    def __init__(self, name, email, cpf, cnpj, cellphone, password, salt):
        self.name = name
        self.email = email
        self.cpf = cpf
        self.cnpj = cnpj
        self.cellphone = cellphone
        self.password = password
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
            "cpf": self.cpf,
            "cnpj": self.cnpj,
            "cellphone": self.cellphone,
            "password": self.password,
            "salt": self.salt,
            "created_at": default_datetime(),
            "updated_at": default_datetime(),
        }
        result = db.users.insert_one(user)
        return result.inserted_id
    
    def find():
        result = db.users.find({})
        return result
    
    def find_by_id(user_id):
        result = db.users.find({"_id": ObjectId(user_id)})
        user = next(result, None)
        return user
    
    def find_by_email(email):
        result = db.users.find_one({"email": email})
        return result

    def find_by_cpf(cpf):
        result = db.users.find_one({"cpf": cpf})
        return result
    
    def find_by_cnpj(cnpj):
        result = db.users.find_one({"cnpj": cnpj})
        return result
    
class Biometric:
    def __init__(self, file, user_id):
        self.file = file
        self.user_id = user_id
    
    def find_by_user_id(user_id):
        result = db.users.find_one({"_id": ObjectId(user_id)})
        if result:
            return result.get("biometrics")
        else:
            return None

    def save(self):
        add_value = {
            "$set": {
                "biometrics": {
                    "file": {
                        "file_b64": self.file["file_b64"],
                        "content_type": self.file["content_type"],
                        "created_at": default_datetime(),
                        "updated_at": default_datetime(),
                    }
                }
            }
        }

        filter = {"_id": ObjectId(self.user_id)}

        result = db.users.update_one(filter, add_value)

        if result.modified_count > 0:
            return self.user_id
        else:
            return None
    
class Document:
    def __init__(self, document_type, file, user_id):
        self.document_type = document_type
        self.file = file
        self.user_id = user_id

    def save(self):
        add_value = {
            "$addToSet": {
                "documents":[
                    {
                        "document_type": self.document_type,
                        "file": {
                            "file_b64": self.file["file_b64"],
                            "content_type": self.file["content_type"],
                            "created_at": default_datetime(),
                            "updated_at": default_datetime(),
                        }
                    }
                ]
            }
        }

        filter = {"_id": ObjectId(self.user_id)}

        result = db.users.update_one(filter, add_value)

        if result.modified_count > 0:
            return self.user_id
        else:
            return None