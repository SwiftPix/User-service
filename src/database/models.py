from pymongo import MongoClient
from settings import settings

client = MongoClient(settings.MONGO_DATABASE_URI)
db = client[settings.MONGO_DATABASE_NAME]
users_collection = db[settings.USER_COLLECTION]

class User:
    def __init__(self, name, email, cpf=None, cnpj=None, cellphone=None, currency=None, balance=0.0, agency=None, institution=None, account=None, password=None, external_id=None):
        self.name = name
        self.email = email
        self.cpf = cpf
        self.cnpj = cnpj
        self.cellphone = cellphone
        self.currency = currency
        self.balance = balance
        self.agency = agency
        self.institution = institution
        self.account = account
        self.password = password
        self.external_id = external_id

    def save(self):
        user_data = self.__dict__
        result = users_collection.insert_one(user_data)
        return result.inserted_id

    @staticmethod
    def find():
        return list(users_collection.find())
