from copy import deepcopy
import json

payload_create = {
    "name": "Fulano de Tal",
    "email": "fulano@example.com",
    "cellphone": "123456789",
    "cpf": "912.815.100-33",
    "password": "Senha123!",
    "cnpj": "35.830.173/0001-11"
}

payload_login = {
        "email": "fulano@example.com",
        "password": "Senha123!"
    }

def test_create_user_success(client):
    """Testa o endpoint de criação de usuário com sucesso."""

    response = client.post("/create", json=payload_create)

    data = json.loads(response.data)
    assert response.status_code == 200
    assert data["status"] == "success"


def test_create_user_error_user_exists(client):
    """Testa o endpoint de criação de usuário com usuário já existente."""

    response = client.post("/create", json=payload_create)

    assert response.status_code == 200

    response = client.post("/create", json=payload_create)

    data = json.loads(response.data)
    assert response.status_code == 409
    assert data["message"] == "Email já está cadastrado"


def test_create_user_error_invalid_payload(client):
    """Testa o endpoint de criação de usuário com payload inválido."""
    invalid_payload_create = deepcopy(payload_create)
    invalid_payload_create.pop("email")

    response = client.post("/create", json=invalid_payload_create)

    data = json.loads(response.data)
    assert response.status_code == 422
    assert data["message"] == "{'email': ['O endereço de e-mail é obrigatório']}"


def test_create_user_error_other_exeception(client, mocker):
    """Testa o endpoint de criação de usuário com payload exceção generica."""

    mocker.patch(
        "controllers.user_controller.UserController.create_user", side_effect=Exception("Erro ao criar usuário")
    )

    response = client.post("/create", json=payload_create)
    data = json.loads(response.data)
    assert response.status_code == 400
    assert data["status"] == 400
    assert data["message"] == "Erro ao criar usuário"


def test_login_success_with_email(client):
    """Testa o endpoint de login de usuário com sucesso."""

    response = client.post("/create", json=payload_create)

    assert response.status_code == 200

    response = client.post("/login", json=payload_login)

    data = json.loads(response.data)
    assert response.status_code == 200
    assert data["status"] == "success"


def test_login_success_with_cpf(client):
    """Testa o endpoint de login de usuário com sucesso."""

    payload_login_with_cpf = {
        "cpf": "912.815.100-33",
        "password": "Senha123!"
    }

    response = client.post("/create", json=payload_create)

    assert response.status_code == 200

    response = client.post("/login", json=payload_login_with_cpf)

    data = json.loads(response.data)
    assert response.status_code == 200
    assert data["status"] == "success"


def test_login_success_with_cnpj(client):
    """Testa o endpoint de login de usuário com sucesso."""

    payload_login_with_cnpj = {
        "cnpj": "35.830.173/0001-11",
        "password": "Senha123!"
    }

    response = client.post("/create", json=payload_create)

    assert response.status_code == 200

    response = client.post("/login", json=payload_login_with_cnpj)

    data = json.loads(response.data)
    assert response.status_code == 200
    assert data["status"] == "success"


def test_login_invalid_password(client):
    """Testa o endpoint de login de usuário com senha inválida."""

    payload_login_invalid_password = deepcopy(payload_login)
    payload_login_invalid_password["password"] = "123"

    response = client.post("/create", json=payload_create)

    assert response.status_code == 200

    response = client.post("/login", json=payload_login_invalid_password)

    data = json.loads(response.data)
    assert response.status_code == 400
    assert data["status"] == 400
    assert data["message"] == "Usuário ou senha inválido"


def test_login_invalid_email(client):
    """Testa o endpoint de login de usuário com e-mail inválido."""

    response = client.post("/login", json=payload_login)

    data = json.loads(response.data)
    assert response.status_code == 400
    assert data["status"] == 400
    assert data["message"] == "Usuário ou senha inválido"


def test_login_invalid_payload(client):
    """Testa o endpoint de login de usuário com payload inválido."""

    payload_login_invalid_payload = deepcopy(payload_login)
    payload_login_invalid_payload.pop("email")

    response = client.post("/create", json=payload_create)

    assert response.status_code == 200

    response = client.post("/login", json=payload_login_invalid_payload)

    data = json.loads(response.data)
    assert response.status_code == 422
    assert data["status"] == 422
    assert data["message"] == "{'_schema': ['É necessário fornecer pelo menos um endereço de e-mail ou cpf/cnpj']}"


def test_login_generic_error(client, mocker):
    """Testa o endpoint de login com erro generico."""

    mocker.patch(
        "controllers.user_controller.UserController.login", side_effect=Exception("Erro ao logar")
    )

    response = client.post("/create", json=payload_create)

    assert response.status_code == 200

    response = client.post("/login", json=payload_login)

    data = json.loads(response.data)
    assert response.status_code == 400
    assert data["status"] == 400
    assert data["message"] == "Erro ao logar"