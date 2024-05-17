import json

def test_create_user_success(client):
    """Testa o endpoint de criação de usuário com sucesso."""

    payload = {
        "name": "Fulano de Tal",
        "email": "fulano@example.com",
        "cellphone": "123456789",
        "password": "Senha123!"
    }

    response = client.post("/create", json=payload)

    data = json.loads(response.data)
    assert response.status_code == 200
    assert data["status"] == "success"


def test_create_user_error_user_exists(client):
    """Testa o endpoint de criação de usuário com usuário já existente."""

    payload = {
        "name": "Fulano de Tal",
        "email": "fulano@example.com",
        "cellphone": "123456789",
        "password": "Senha123!"
    }

    response = client.post("/create", json=payload)

    assert response.status_code == 200

    response = client.post("/create", json=payload)

    data = json.loads(response.data)
    assert response.status_code == 409
    assert data["message"] == "Email já está cadastrado"


def test_create_user_error_invalid_payload(client):
    """Testa o endpoint de criação de usuário com payload inválido."""

    payload = {
        "name": "Fulano de Tal",
        "cellphone": "123456789",
        "password": "Senha123!"
    }

    response = client.post("/create", json=payload)

    data = json.loads(response.data)
    assert response.status_code == 422
    assert data["message"] == "{'email': ['O endereço de e-mail é obrigatório']}"


def test_create_user_error_other_exeception(client, mocker):
    """Testa o endpoint de criação de usuário com payload exceção generica."""

    mocker.patch(
        "controllers.user_controller.UserController.create_user", side_effect=Exception("Erro ao criar usuário")
    )

    payload = {
        "name": "Fulano de Tal",
        "email": "fulano@example.com",
        "cellphone": "123456789",
        "password": "Senha123!"
    }

    response = client.post("/create", json=payload)
    data = json.loads(response.data)
    assert response.status_code == 400
    assert data["status"] == 400
    assert data["message"] == "Erro ao criar usuário"


def test_login_success(client):
    """Testa o endpoint de login de usuário com sucesso."""

    payload = {
        "name": "Fulano de Tal",
        "email": "fulano@example.com",
        "cellphone": "123456789",
        "password": "Senha123!"
    }

    payload_login = {
        "email": "fulano@example.com",
        "password": "Senha123!"
    }

    response = client.post("/create", json=payload)

    assert response.status_code == 200

    response = client.post("/login", json=payload_login)

    data = json.loads(response.data)
    assert response.status_code == 200
    assert data["status"] == "success"


def test_login_invalid_password(client):
    """Testa o endpoint de login de usuário com senha inválida."""

    payload = {
        "name": "Fulano de Tal",
        "email": "fulano@example.com",
        "cellphone": "123456789",
        "password": "Senha123!"
    }

    payload_login = {
        "email": "fulano@example.com",
        "password": "tentativadesenha"
    }

    response = client.post("/create", json=payload)

    assert response.status_code == 200

    response = client.post("/login", json=payload_login)

    data = json.loads(response.data)
    assert response.status_code == 400
    assert data["status"] == 400
    assert data["message"] == "Usuário ou senha inválido"


def test_login_invalid_email(client):
    """Testa o endpoint de login de usuário com e-mail inválido."""

    payload_login = {
        "email": "ciclano@example.com",
        "password": "Senha123!"
    }

    response = client.post("/login", json=payload_login)

    data = json.loads(response.data)
    assert response.status_code == 400
    assert data["status"] == 400
    assert data["message"] == "Usuário ou senha inválido"


def test_login_invalid_payload(client):
    """Testa o endpoint de login de usuário com payload inválido."""

    payload = {
        "name": "Fulano de Tal",
        "email": "fulano@example.com",
        "cellphone": "123456789",
        "password": "Senha123!"
    }

    payload_login = {
        "password": "Senha123!"
    }

    response = client.post("/create", json=payload)

    assert response.status_code == 200

    response = client.post("/login", json=payload_login)

    data = json.loads(response.data)
    assert response.status_code == 422
    assert data["status"] == 422
    assert data["message"] == "{'email': ['O endereço de e-mail é obrigatório']}"


def test_login_generic_error(client, mocker):
    """Testa o endpoint de login com erro generico."""

    mocker.patch(
        "controllers.user_controller.UserController.login", side_effect=Exception("Erro ao logar")
    )

    payload = {
        "name": "Fulano de Tal",
        "email": "fulano@example.com",
        "cellphone": "123456789",
        "password": "Senha123!"
    }

    payload_login = {
        "email": "fulano@example.com",
        "password": "Senha123!"
    }

    response = client.post("/create", json=payload)

    assert response.status_code == 200

    response = client.post("/login", json=payload_login)

    data = json.loads(response.data)
    assert response.status_code == 400
    assert data["status"] == 400
    assert data["message"] == "Erro ao logar"