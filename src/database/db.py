from pymongo import MongoClient
from src.settings import settings
from flask import current_app

def initialize_mongo(app):
    mongo_uri = settings.MONGO_DATABASE_URI
    db_name = settings.MONGO_DATABASE_NAME

    client = MongoClient(mongo_uri)
    db = client[db_name]

    return db

def get_db():
    with current_app.app_context():
        db = getattr(current_app, 'mongo_db', None)
        if db is None:
            raise RuntimeError('Banco de dados não inicializado.')
        return db