import pytest
from flask import Flask
from pymongo import MongoClient
from main import create_app
from settings import settings

@pytest.fixture
def app():
    """Fixture para criar uma instância do aplicativo Flask para os testes."""
    app = create_app()

    app.config["TESTING"] = True
    app.config["MONGO_DATABASE_URI"] = settings.MONGO_DATABASE_URI
    app.config["MONGO_DATABASE_NAME"] = settings.MONGO_DATABASE_NAME

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


@pytest.fixture
def mock_encrypt(mocker):
    mock_encrypt = mocker.patch(
        "controllers.crypt_controller.CryptController.encrypt", 
        side_effect=[
            "email",
            "cpf",
            "cnpj",
            "password",
            "email",
            "cpf",
            "cnpj",
            "password"
        ]
    )
    return mock_encrypt


@pytest.fixture
def mock_decrypt(mocker):
    mock_decrypt = mocker.patch(
        "controllers.crypt_controller.CryptController.decrypt", 
        side_effect=[
            "fulano@example.com",
            "912.815.100-33",
            "35.830.173/0001-11",
            "Senha123!",
            "fulano@example.com",
            "912.815.100-33",
            "35.830.173/0001-11",
            "Senha123!"
        ]
    )
    return mock_decrypt


@pytest.fixture
def mock_expenses_auth(mocker):
    mock_expenses_auth = mocker.patch(
        "controllers.expenses_controller.ExpensesController.auth", 
        return_value={}
    )
    return mock_expenses_auth


@pytest.fixture
def mock_expenses_register(mocker):
    mock_expenses_register = mocker.patch(
        "controllers.expenses_controller.ExpensesController.register", 
        return_value={}
    )
    return mock_expenses_register


@pytest.fixture
def mock_expenses_create(mocker):
    mock_expenses_create = mocker.patch(
        "controllers.expenses_controller.ExpensesController.create_expense", 
        return_value={
            "amount": 500.0,
            "category": {
                "id": "adb59d31-d222-44af-b24c-c3cfbd658b4c",
                "name": "Alimentação"
            },
            "description": None,
            "expiration_date": "2024-06-25",
            "id": "123",
            "name": "Compras do mês",
            "paid": True,
            "payment_date": "2024-06-25",
            "user_id": 11
        }
    )
    return mock_expenses_create


@pytest.fixture
def mock_expenses_list(mocker):
    mock_expenses_list = mocker.patch(
        "controllers.expenses_controller.ExpensesController.list_expenses", 
        return_value=[{
            "amount": 500.0,
            "category": {
                "id": "adb59d31-d222-44af-b24c-c3cfbd658b4c",
                "name": "Alimentação"
            },
            "description": None,
            "expiration_date": "2024-06-25",
            "id": "123",
            "name": "Compras do mês",
            "paid": True,
            "payment_date": "2024-06-25",
            "user_id": 11
        }]
    )
    return mock_expenses_list


@pytest.fixture
def mock_expenses_list_categories(mocker):
    mock_expenses_list_categories = mocker.patch(
        "controllers.expenses_controller.ExpensesController.list_expenses_categories", 
        return_value=[{
            "description": "Categoria de despesa de Alimentação",
            "id": "adb59d31-d222-44af-b24c-c3cfbd658b4c",
            "name": "Alimentação"
        }]
    )
    return mock_expenses_list_categories


@pytest.fixture
def mock_validate_biometrics_true(mocker):
    mock_validate_biometrics_true = mocker.patch(
        "utils.face_recog.ValidateBiometric.validate_faces", 
        return_value=True
    )
    return mock_validate_biometrics_true


@pytest.fixture
def mock_validate_biometrics_false(mocker):
    mock_validate_biometrics_false = mocker.patch(
        "utils.face_recog.ValidateBiometric.validate_faces", 
        return_value=False
    )
    return mock_validate_biometrics_false