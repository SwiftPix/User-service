import pytest
from flask import Flask
from pymongo import MongoClient
from src.main import create_app


@pytest.fixture
def app():
    """Fixture para criar uma instância do aplicativo Flask para os testes."""
    app = create_app()

    app.config["TESTING"] = True
    app.config["MONGO_DATABASE_URI"] = "mongodb://localhost:27017"
    app.config["MONGO_DATABASE_NAME"] = "test_db"

    with app.app_context():
        client = MongoClient(app.config["MONGO_DATABASE_URI"])
        db = client[app.config["MONGO_DATABASE_NAME"]]
        db.users.delete_many({})

        yield app

        db.users.delete_many({})
        client.close()


@pytest.fixture
def client(app):
    """Fixture para criar um cliente de teste para o aplicativo Flask."""
    return app.test_client()