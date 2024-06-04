from copy import deepcopy
from io import BytesIO
import json
import re
from tests.payloads import payload_create, payload_login, payload_documents, payload_update_balance


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


def test_documents_success(client):
    """Testa o endpoint de documento com sucesso."""

    file_content = b"This is a test file"
    file = BytesIO(file_content)
    file.name = "test_file.png"

    payload_documents["file"] = (file, file.name)

    response = client.post("/create", json=payload_create)

    assert response.status_code == 200
    user_created = json.loads(response.data)
    match = re.search(r"ID: ([a-f0-9]{24})", user_created["message"])
    assert match is not None
    user_id = match.group(1)

    response = client.put(
        f'/documents/{user_id}',
        data=payload_documents,
        content_type='multipart/form-data'
    )

    data = json.loads(response.data)
    assert response.status_code == 200
    assert data["status"] == "success"


def test_documents_user_doesnt_exists_payload(client):
    """Testa o endpoint de documento de usuário com usuário inexistente."""

    file_content = b"This is a test file"
    file = BytesIO(file_content)
    file.name = "test_file.png"

    payload_documents["file"] = (file, file.name)

    response = client.put(
        '/documents/664e9b2da3835b65a119b35d',
        data=payload_documents,
        content_type='multipart/form-data'
    )

    data = json.loads(response.data)
    assert response.status_code == 404
    assert data["status"] == 404
    assert data["message"] == "Usuário não encontrado"


def test_documents_invalid_payload(client):
    """Testa o endpoint de documento de usuário com payload inválido."""

    file_content = b"This is a test file"
    file = BytesIO(file_content)
    file.name = "test_file.png"

    payload_documents["file"] = (file, file.name)

    payload_login_invalid_payload = deepcopy(payload_login)
    payload_login_invalid_payload.pop("email")

    response = client.post("/create", json=payload_create)

    assert response.status_code == 200

    user_created = json.loads(response.data)
    match = re.search(r"ID: ([a-f0-9]{24})", user_created["message"])
    assert match is not None
    user_id = match.group(1)

    payload_documents_invalid_payload = deepcopy(payload_documents)
    payload_documents_invalid_payload.pop("document_type")

    response = client.put(
        f'/documents/{user_id}',
        data=payload_documents_invalid_payload,
        content_type='multipart/form-data'
    )

    data = json.loads(response.data)
    assert response.status_code == 422
    assert data["status"] == 422
    assert data["message"] == "Tipo de documento e arquivo são obrigatórios"


def test_login_generic_error(client, mocker):
    """Testa o endpoint de documento de usuário com erro generico."""

    file_content = b"This is a test file"
    file = BytesIO(file_content)
    file.name = "test_file.png"

    payload_documents["file"] = (file, file.name)

    mocker.patch(
        "controllers.user_controller.UserController.create_document", side_effect=Exception("Erro ao salvar documento")
    )

    response = client.post("/create", json=payload_create)

    assert response.status_code == 200

    user_created = json.loads(response.data)
    match = re.search(r"ID: ([a-f0-9]{24})", user_created["message"])
    assert match is not None
    user_id = match.group(1)

    response = client.put(
        f'/documents/{user_id}',
        data=payload_documents,
        content_type='multipart/form-data'
    )

    data = json.loads(response.data)
    assert response.status_code == 400
    assert data["status"] == 400
    assert data["message"] == "Erro ao salvar documento"


def test_update_balance_success(client):
    """Testa o endpoint de atualizar saldo do usuário."""

    response = client.post("/create", json=payload_create)

    data = json.loads(response.data)
    assert response.status_code == 200
    match = re.search(r"ID: ([a-f0-9]{24})", data["message"])
    assert match is not None
    user_id = match.group(1)

    response = client.patch(f"/balance/{user_id}", json=payload_update_balance)

    assert response.status_code == 200


def test_update_balance_validation_error(client):
    """Testa o endpoint de atualizar saldo do usuário com erro de validação."""

    response = client.post("/create", json=payload_create)

    data = json.loads(response.data)
    assert response.status_code == 200
    match = re.search(r"ID: ([a-f0-9]{24})", data["message"])
    assert match is not None
    user_id = match.group(1)

    payload_update_balance_invalid_payload = deepcopy(payload_update_balance)
    payload_update_balance_invalid_payload["balance"] = "teste"

    response = client.patch(f"/balance/{user_id}", json=payload_update_balance_invalid_payload)

    assert response.status_code == 422


def test_update_balance_user_not_found(client):
    """Testa o endpoint de atualizar saldo do usuário com erro de usuário não encontrado."""

    response = client.patch("/balance/664e9b2da3835b65a119b35d", json=payload_update_balance)

    assert response.status_code == 404


def test_update_balance_generic_error(client, mocker):
    """Testa o endpoint de atualizar saldo do usuário com erro generico."""

    response = client.post("/create", json=payload_create)

    data = json.loads(response.data)
    assert response.status_code == 200
    match = re.search(r"ID: ([a-f0-9]{24})", data["message"])
    assert match is not None
    user_id = match.group(1)

    mocker.patch(
        "controllers.user_controller.UserController.update_balance", side_effect=Exception("Erro ao salvar saldo")
    )

    response = client.patch(f"/balance/{user_id}", json=payload_update_balance)

    data = json.loads(response.data)
    assert response.status_code == 400
    assert data["status"] == 400
    assert data["message"] == "Erro ao salvar saldo"


def test_get_balance_success(client):
    """Testa o endpoint de buscar saldo do usuário."""

    response = client.post("/create", json=payload_create)

    data = json.loads(response.data)
    assert response.status_code == 200
    match = re.search(r"ID: ([a-f0-9]{24})", data["message"])
    assert match is not None
    user_id = match.group(1)
    expected_response = {
        "currency": "real",
        "balance": 0.0
    }

    response = client.get(f"/balance/{user_id}")
    assert response.status_code == 200
    assert response.json == expected_response


def test_get_balance_user_not_found(client):
    """Testa o endpoint de buscar saldo do usuário com erro de usuário não encontrado."""

    response = client.get("/balance/664e9b2da3835b65a119b35d")

    assert response.status_code == 404


def test_update_balance_generic_error(client, mocker):
    """Testa o endpoint de atualizar saldo do usuário com erro generico."""

    response = client.post("/create", json=payload_create)

    data = json.loads(response.data)
    assert response.status_code == 200
    match = re.search(r"ID: ([a-f0-9]{24})", data["message"])
    assert match is not None
    user_id = match.group(1)

    mocker.patch(
        "controllers.user_controller.UserController.get_balance", side_effect=Exception("Erro ao buscar saldo")
    )

    response = client.get(f"/balance/{user_id}")

    data = json.loads(response.data)
    assert response.status_code == 400
    assert data["status"] == 400
    assert data["message"] == "Erro ao buscar saldo"
