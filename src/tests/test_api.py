from copy import deepcopy
from io import BytesIO
import json
import os
import re
from utils.exceptions import ExpensesException
from tests.payloads import (
    payload_create,
    payload_login,
    payload_documents,
    payload_update_balance,
    payload_expenses,
    payload_biometrics,
    payload_biometric_from_partner
)


def test_create_user_success(client, mock_encrypt, mock_decrypt, mock_expenses_auth, mock_expenses_register):
    """Testa o endpoint de criação de usuário com sucesso."""

    response = client.post("/create", json=payload_create)

    data = json.loads(response.data)
    assert response.status_code == 200
    assert data["status"] == "success"


def test_create_user_error_user_exists(client, mock_encrypt, mock_decrypt, mock_expenses_auth, mock_expenses_register):
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


def test_login_success_with_email(client, mock_encrypt, mock_decrypt, mock_expenses_auth, mock_expenses_register):
    """Testa o endpoint de login de usuário com sucesso."""

    response = client.post("/create", json=payload_create)

    assert response.status_code == 200

    response = client.post("/login", json=payload_login)

    data = json.loads(response.data)
    assert response.status_code == 200
    assert data["status"] == "success"


def test_login_success_with_cpf(client, mock_encrypt, mock_decrypt, mock_expenses_auth, mock_expenses_register):
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


def test_login_success_with_cnpj(client, mock_encrypt, mock_decrypt, mock_expenses_auth, mock_expenses_register):
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


def test_login_invalid_password(client, mock_encrypt, mock_decrypt, mock_expenses_auth, mock_expenses_register):
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


def test_login_invalid_email(client, mock_decrypt):
    """Testa o endpoint de login de usuário com e-mail inválido."""

    response = client.post("/login", json=payload_login)

    data = json.loads(response.data)
    assert response.status_code == 400
    assert data["status"] == 400
    assert data["message"] == "Usuário ou senha inválido"


def test_login_invalid_payload(client, mock_encrypt, mock_decrypt, mock_expenses_auth, mock_expenses_register):
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


def test_login_generic_error(client, mocker, mock_encrypt, mock_decrypt, mock_expenses_auth, mock_expenses_register):
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


def test_documents_success(client, mock_encrypt, mock_decrypt, mock_expenses_auth, mock_expenses_register):
    """Testa o endpoint de documento com sucesso."""

    file_content = b"This is a test file"
    file = BytesIO(file_content)
    file.name = "test_file.png"

    payload_documents["file"] = (file, file.name)

    response = client.post("/create", json=payload_create)

    assert response.status_code == 200
    user_id = response.json["user"]

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


def test_documents_invalid_payload(client, mock_encrypt, mock_decrypt, mock_expenses_auth, mock_expenses_register):
    """Testa o endpoint de documento de usuário com payload inválido."""

    file_content = b"This is a test file"
    file = BytesIO(file_content)
    file.name = "test_file.png"

    payload_documents["file"] = (file, file.name)

    payload_login_invalid_payload = deepcopy(payload_login)
    payload_login_invalid_payload.pop("email")

    response = client.post("/create", json=payload_create)

    assert response.status_code == 200

    user_id = response.json["user"]

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


def test_documents_generic_error(client, mocker, mock_encrypt, mock_decrypt, mock_expenses_auth, mock_expenses_register):
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

    user_id = response.json["user"]

    response = client.put(
        f'/documents/{user_id}',
        data=payload_documents,
        content_type='multipart/form-data'
    )

    data = json.loads(response.data)
    assert response.status_code == 400
    assert data["status"] == 400
    assert data["message"] == "Erro ao salvar documento"


def test_update_balance_success(client, mock_encrypt, mock_decrypt, mock_expenses_auth, mock_expenses_register):
    """Testa o endpoint de atualizar saldo do usuário."""

    response = client.post("/create", json=payload_create)

    assert response.status_code == 200
    user_id = response.json["user"]

    response = client.patch(f"/balance/{user_id}", json=payload_update_balance)

    assert response.status_code == 200


def test_update_balance_validation_error(client, mock_encrypt, mock_decrypt, mock_expenses_auth, mock_expenses_register):
    """Testa o endpoint de atualizar saldo do usuário com erro de validação."""

    response = client.post("/create", json=payload_create)

    assert response.status_code == 200
    user_id = response.json["user"]

    payload_update_balance_invalid_payload = deepcopy(payload_update_balance)
    payload_update_balance_invalid_payload["balance"] = "teste"

    response = client.patch(f"/balance/{user_id}", json=payload_update_balance_invalid_payload)

    assert response.status_code == 422


def test_update_balance_user_not_found(client):
    """Testa o endpoint de atualizar saldo do usuário com erro de usuário não encontrado."""

    response = client.patch("/balance/664e9b2da3835b65a119b35d", json=payload_update_balance)

    assert response.status_code == 404


def test_update_balance_generic_error(client, mocker, mock_encrypt, mock_decrypt, mock_expenses_auth, mock_expenses_register):
    """Testa o endpoint de atualizar saldo do usuário com erro generico."""

    response = client.post("/create", json=payload_create)

    assert response.status_code == 200
    user_id = response.json["user"]

    mocker.patch(
        "controllers.user_controller.UserController.update_balance", side_effect=Exception("Erro ao salvar saldo")
    )

    response = client.patch(f"/balance/{user_id}", json=payload_update_balance)

    data = json.loads(response.data)
    assert response.status_code == 400
    assert data["status"] == 400
    assert data["message"] == "Erro ao salvar saldo"


def test_get_balance_success(client, mock_encrypt, mock_decrypt, mock_expenses_auth, mock_expenses_register):
    """Testa o endpoint de buscar saldo do usuário."""

    response = client.post("/create", json=payload_create)

    assert response.status_code == 200
    user_id = response.json["user"]
    expected_response = {
        "currency": "BRL",
        "balance": 0.0
    }

    response = client.get(f"/balance/{user_id}")
    assert response.status_code == 200
    assert response.json == expected_response


def test_get_balance_user_not_found(client):
    """Testa o endpoint de buscar saldo do usuário com erro de usuário não encontrado."""

    response = client.get("/balance/664e9b2da3835b65a119b35d")

    assert response.status_code == 404


def test_update_balance_generic_error(client, mocker, mock_encrypt, mock_decrypt, mock_expenses_auth, mock_expenses_register):
    """Testa o endpoint de atualizar saldo do usuário com erro generico."""

    response = client.post("/create", json=payload_create)

    assert response.status_code == 200
    user_id = response.json["user"]

    mocker.patch(
        "controllers.user_controller.UserController.get_balance", side_effect=Exception("Erro ao buscar saldo")
    )

    response = client.get(f"/balance/{user_id}")

    data = json.loads(response.data)
    assert response.status_code == 400
    assert data["status"] == 400
    assert data["message"] == "Erro ao buscar saldo"


def test_create_expense_success(
        client,
        mock_encrypt,
        mock_decrypt,
        mock_expenses_auth,
        mock_expenses_register,
        mock_expenses_create
    ):
    """Testa o endpoint de criar despesas do usuário com sucesso."""

    response = client.post("/create", json=payload_create)

    assert response.status_code == 200
    user_id = response.json["user"]

    response = client.post(f"/expense/{user_id}", json=payload_expenses)

    assert response.status_code == 200


def test_create_expense_user_not_found(
        client,
        mock_encrypt,
        mock_decrypt,
        mock_expenses_auth,
        mock_expenses_register,
        mock_expenses_create
    ):
    """Testa o endpoint de criar despesas do usuário com usuario não encontrado."""

    response = client.post("/expense/665e0069183ce834954a2f44", json=payload_expenses)

    assert response.status_code == 404
    assert response.json == {"status": 404, "message": "Usuário não encontrado"}


def test_create_expense_service_offline(
        client,
        mocker,
        mock_encrypt,
        mock_decrypt,
        mock_expenses_auth, 
        mock_expenses_register
    ):
    """Testa o endpoint de criar despesas do usuário com serviço de despesas indisponivel."""

    mocker.patch(
        "controllers.expenses_controller.ExpensesController.create_expense", side_effect=ExpensesException("Não foi possível comunicar com o servidor de despesas")
    )

    response = client.post("/create", json=payload_create)

    assert response.status_code == 200
    user_id = response.json["user"]

    response = client.post(f"/expense/{user_id}", json=payload_expenses)

    assert response.status_code == 400
    assert response.json == {"status": 400, "message": "Não foi possível comunicar com o servidor de despesas"}


def test_create_expense_generic_error(
        client,
        mocker,
        mock_encrypt,
        mock_decrypt,
        mock_expenses_auth,
        mock_expenses_register,
        mock_expenses_create
    ):
    """Testa o endpoint de criar despesas do usuário com erro generico."""

    mocker.patch(
        "controllers.user_controller.UserController.create_expense", side_effect=Exception("Erro gerar despesa")
    )

    response = client.post("/create", json=payload_create)

    assert response.status_code == 200
    user_id = response.json["user"]

    response = client.post(f"/expense/{user_id}", json=payload_expenses)

    assert response.status_code == 400
    assert response.json == {"status": 400, "message": "Erro gerar despesa"}


def test_get_expenses_success(
        client,
        mock_encrypt,
        mock_decrypt,
        mock_expenses_auth,
        mock_expenses_register,
        mock_expenses_create,
        mock_expenses_list
    ):
    """Testa o endpoint de buscar despesas do usuário com sucesso."""

    response = client.post("/create", json=payload_create)

    assert response.status_code == 200
    user_id = response.json["user"]

    response = client.post(f"/expense/{user_id}", json=payload_expenses)

    assert response.status_code == 200

    response = client.get(f"/expense/{user_id}")

    assert response.status_code == 200


def test_get_expenses_user_not_found(
        client,
        mock_encrypt,
        mock_decrypt,
        mock_expenses_auth,
        mock_expenses_register,
        mock_expenses_create,
        mock_expenses_list
    ):
    """Testa o endpoint de buscar despesas do usuário com sucesso."""

    response = client.get("/expense/665e0069183ce834954a2f44", json=payload_expenses)

    assert response.status_code == 404
    assert response.json == {"status": 404, "message": "Usuário não encontrado"}


def test_get_expenses_service_offline(
        client,
        mocker,
        mock_encrypt,
        mock_decrypt,
        mock_expenses_auth,
        mock_expenses_register,
        mock_expenses_create,
        mock_expenses_list
    ):
    """Testa o endpoint de buscar despesas do usuário com serviço de despesas indisponivel."""

    mocker.patch(
        "controllers.expenses_controller.ExpensesController.list_expenses", side_effect=ExpensesException("Não foi possível comunicar com o servidor de despesas")
    )

    response = client.post("/create", json=payload_create)

    assert response.status_code == 200
    user_id = response.json["user"]

    response = client.post(f"/expense/{user_id}", json=payload_expenses)

    assert response.status_code == 200

    response = client.get(f"/expense/{user_id}")

    assert response.status_code == 400
    assert response.json == {"status": 400, "message": "Não foi possível comunicar com o servidor de despesas"}


def test_get_expenses_generic_error(
        client,
        mocker,
        mock_encrypt,
        mock_decrypt,
        mock_expenses_auth,
        mock_expenses_register,
        mock_expenses_create,
        mock_expenses_list
    ):
    """Testa o endpoint de buscar despesas do usuário com erro generico."""

    mocker.patch(
        "controllers.user_controller.UserController.get_expenses", side_effect=Exception("Erro buscar despesa")
    )

    response = client.post("/create", json=payload_create)

    assert response.status_code == 200
    user_id = response.json["user"]

    response = client.post(f"/expense/{user_id}", json=payload_expenses)

    assert response.status_code == 200

    response = client.get(f"/expense/{user_id}")

    assert response.status_code == 400
    assert response.json == {"status": 400, "message": "Erro buscar despesa"}


def test_get_expenses_categories_success(
        client,
        mock_expenses_list_categories
    ):
    """Testa o endpoint de buscar categorias de despesas do usuário com sucesso."""

    response = client.get(f"/expenses")

    assert response.status_code == 200


def test_get_expenses_categories_service_offline(
        client,
        mocker,
        mock_expenses_list_categories
    ):
    """Testa o endpoint de buscar categorias de despesas do usuário com serviço de despesas indisponivel."""

    mocker.patch(
        "controllers.expenses_controller.ExpensesController.list_expenses_categories", side_effect=ExpensesException("Não foi possível comunicar com o servidor de despesas")
    )

    response = client.get(f"/expenses")

    assert response.status_code == 400
    assert response.json == {"status": 400, "message": "Não foi possível comunicar com o servidor de despesas"}


def test_get_expenses_categories_generic_error(
        client,
        mocker,
        mock_expenses_list_categories
    ):
    """Testa o endpoint de buscar categorias de despesas do usuário com erro generico."""

    mocker.patch(
        "controllers.expenses_controller.ExpensesController.list_expenses_categories", side_effect=Exception("Erro ao buscar categorias de despesas")
    )

    response = client.get(f"/expenses")

    assert response.status_code == 400
    assert response.json == {"status": 400, "message": "Erro ao buscar categorias de despesas"}


def test_biometrics_success(client, mock_encrypt, mock_decrypt, mock_expenses_auth, mock_expenses_register):
    """Testa o endpoint de biometria com sucesso."""

    file_content = b"This is a test file"
    file = BytesIO(file_content)
    file.name = "test_file.png"

    payload_biometrics["file"] = (file, file.name)

    response = client.post("/create", json=payload_create)

    assert response.status_code == 200
    user_id = response.json["user"]

    response = client.put(
        f'/send_biometry/{user_id}',
        data=payload_biometrics,
        content_type='multipart/form-data'
    )

    data = json.loads(response.data)
    assert response.status_code == 200
    assert data["status"] == "success"


def test_biometrics_user_doesnt_exists_payload(client):
    """Testa o endpoint de biometria de usuário com usuário inexistente."""

    file_content = b"This is a test file"
    file = BytesIO(file_content)
    file.name = "test_file.png"

    payload_biometrics["file"] = (file, file.name)

    response = client.put(
        '/send_biometry/664e9b2da3835b65a119b35d',
        data=payload_biometrics,
        content_type='multipart/form-data'
    )

    data = json.loads(response.data)
    assert response.status_code == 404
    assert data["status"] == 404
    assert data["message"] == "Usuário não encontrado"


def test_biometrics_invalid_payload(client, mock_encrypt, mock_decrypt, mock_expenses_auth, mock_expenses_register):
    """Testa o endpoint de briometria de usuário com payload inválido."""

    file_content = b"This is a test file"
    file = BytesIO(file_content)
    file.name = "test_file.png"

    payload_biometrics["file"] = (file, file.name)

    payload_login_invalid_payload = deepcopy(payload_login)
    payload_login_invalid_payload.pop("email")

    response = client.post("/create", json=payload_create)

    assert response.status_code == 200

    user_id = response.json["user"]

    payload_biometrics_invalid_payload = deepcopy(payload_biometrics)
    payload_biometrics_invalid_payload.pop("file")

    response = client.put(
        f'/send_biometry/{user_id}',
        data=payload_biometrics_invalid_payload,
        content_type='multipart/form-data'
    )

    data = json.loads(response.data)
    assert response.status_code == 422
    assert data["status"] == 422
    assert data["message"] == "Arquivo é obrigatório"


def test_biometrics_generic_error(client, mocker, mock_encrypt, mock_decrypt, mock_expenses_auth, mock_expenses_register):
    """Testa o endpoint de biometria de usuário com erro generico."""

    file_content = b"This is a test file"
    file = BytesIO(file_content)
    file.name = "test_file.png"

    payload_biometrics["file"] = (file, file.name)

    mocker.patch(
        "controllers.user_controller.UserController.save_biometric", side_effect=Exception("Erro ao salvar biometria")
    )

    response = client.post("/create", json=payload_create)

    assert response.status_code == 200

    user_id = response.json["user"]

    response = client.put(
        f'/send_biometry/{user_id}',
        data=payload_biometrics,
        content_type='multipart/form-data'
    )

    data = json.loads(response.data)
    assert response.status_code == 400
    assert data["status"] == 400
    assert data["message"] == "Erro ao salvar biometria"


def test_get_biometrics_success(client, mock_encrypt, mock_decrypt, mock_expenses_auth, mock_expenses_register):
    """Testa o endpoint de buscar biometria com sucesso."""

    file_content = b"This is a test file"
    file = BytesIO(file_content)
    file.name = "test_file.png"

    payload_biometrics["file"] = (file, file.name)

    response = client.post("/create", json=payload_create)

    assert response.status_code == 200
    user_id = response.json["user"]

    response = client.put(
        f'/send_biometry/{user_id}',
        data=payload_biometrics,
        content_type='multipart/form-data'
    )

    assert response.status_code == 200

    response = client.get(f"/get_biometry_status/{user_id}")

    assert response.status_code == 200
    

def test_get_biometrics_user_doesnt_exists(client):
    """Testa o endpoint de buscar biometria de usuário com usuário inexistente."""

    response = client.get("/get_biometry_status/664e9b2da3835b65a119b35d")

    data = json.loads(response.data)
    assert response.status_code == 404
    assert data["status"] == 404
    assert data["message"] == "Usuário não encontrado"


def test_get_biometrics_doesnt_exists(client, mock_encrypt, mock_decrypt, mock_expenses_auth, mock_expenses_register):
    """Testa o endpoint de buscar briometria sem biometria cadastrada."""

    file_content = b"This is a test file"
    file = BytesIO(file_content)
    file.name = "test_file.png"

    payload_biometrics["file"] = (file, file.name)

    response = client.post("/create", json=payload_create)

    assert response.status_code == 200

    user_id = response.json["user"]

    response = client.get(f"/get_biometry_status/{user_id}")

    data = json.loads(response.data)
    assert data["status"] == 404
    assert data["message"] == "Biometria não encontrada."


def test_get_biometrics_generic_error(client, mocker, mock_encrypt, mock_decrypt, mock_expenses_auth, mock_expenses_register):
    """Testa o endpoint de buscar biometria de usuário com erro generico."""

    file_content = b"This is a test file"
    file = BytesIO(file_content)
    file.name = "test_file.png"

    payload_biometrics["file"] = (file, file.name)

    mocker.patch(
        "controllers.user_controller.UserController.get_biometric", side_effect=Exception("Erro ao buscar biometria")
    )

    response = client.post("/create", json=payload_create)

    assert response.status_code == 200

    user_id = response.json["user"]

    response = client.put(
        f'/send_biometry/{user_id}',
        data=payload_biometrics,
        content_type='multipart/form-data'
    )

    assert response.status_code == 200

    response = client.get(f"/get_biometry_status/{user_id}")

    data = json.loads(response.data)
    assert response.status_code == 400
    assert data["status"] == 400
    assert data["message"] == "Erro ao buscar biometria"


def test_validate_biometrics_success(
        client,
        mocker,
        mock_encrypt,
        mock_decrypt,
        mock_expenses_auth,
        mock_expenses_register,
        mock_validate_biometrics_true
    ):
    """Testa o endpoint de validar biometria com sucesso."""
    payload_biometric_to_validate = {}

    file_content = b"This is a test file"
    file_content_validate = b"This is a validation of test file"
    file = BytesIO(file_content)
    file.name = "test_file.png"
    file_validate = BytesIO(file_content_validate)
    file_validate.name = "test_file.png"

    payload_biometrics["file"] = (file, file.name)
    payload_biometric_to_validate["file"] = (file_validate, file_validate.name)

    response = client.post("/create", json=payload_create)

    assert response.status_code == 200
    user_id = response.json["user"]

    response = client.put(
        f'/send_biometry/{user_id}',
        data=payload_biometrics,
        content_type='multipart/form-data'
    )

    assert response.status_code == 200

    response = client.post(
        f'/biometrics/{user_id}',
        data=payload_biometric_to_validate,
        content_type='multipart/form-data'
    )
    assert response.status_code == 200


def test_validate_biometrics_doesnt_match(
        client,
        mock_encrypt,
        mock_decrypt,
        mock_expenses_auth,
        mock_expenses_register,
        mock_validate_biometrics_false
    ):
    """Testa o endpoint de validar biometria com biometria não reconhecida."""

    payload_biometric_to_validate = {}

    file_content = b"This is a test file"
    file_content_validate = b"This is a validation of test file"
    file = BytesIO(file_content)
    file.name = "test_file.png"
    file_validate = BytesIO(file_content_validate)
    file_validate.name = "test_file.png"

    payload_biometrics["file"] = (file, file.name)
    payload_biometric_to_validate["file"] = (file_validate, file_validate.name)

    response = client.post("/create", json=payload_create)

    assert response.status_code == 200
    user_id = response.json["user"]

    response = client.put(
        f'/send_biometry/{user_id}',
        data=payload_biometrics,
        content_type='multipart/form-data'
    )

    assert response.status_code == 200

    response = client.post(
        f'/biometrics/{user_id}',
        data=payload_biometric_to_validate,
        content_type='multipart/form-data'
    )
    data = json.loads(response.data)
    assert response.status_code == 400
    assert data["status"] == 400
    assert data["message"] == "Biometria inválida."
    

def test_validate_biometrics_user_doesnt_exists(client):
    """Testa o endpoint de validar biometria de usuário com usuário inexistente."""

    payload_biometric_to_validate = {}

    file_content = b"This is a test file"
    file_content_validate = b"This is a validation of test file"
    file = BytesIO(file_content)
    file.name = "test_file.png"
    file_validate = BytesIO(file_content_validate)
    file_validate.name = "test_file.png"

    payload_biometrics["file"] = (file, file.name)
    payload_biometric_to_validate["file"] = (file_validate, file_validate.name)

    response = client.post(
        '/biometrics/664e9b2da3835b65a119b35d',
        data=payload_biometric_to_validate,
        content_type='multipart/form-data'
    )

    data = json.loads(response.data)
    assert response.status_code == 404
    assert data["status"] == 404
    assert data["message"] == "Usuário não encontrado"


def test_validate_biometrics_doesnt_exists(client, mock_encrypt, mock_decrypt, mock_expenses_auth, mock_expenses_register):
    """Testa o endpoint de validar briometria sem biometria cadastrada."""

    payload_biometric_to_validate = {}

    file_content = b"This is a test file"
    file_content_validate = b"This is a validation of test file"
    file = BytesIO(file_content)
    file.name = "test_file.png"
    file_validate = BytesIO(file_content_validate)
    file_validate.name = "test_file.png"

    payload_biometrics["file"] = (file, file.name)
    payload_biometric_to_validate["file"] = (file_validate, file_validate.name)
    response = client.post("/create", json=payload_create)

    assert response.status_code == 200

    user_id = response.json["user"]

    response = client.post(
        f'/biometrics/{user_id}',
        data=payload_biometric_to_validate,
        content_type='multipart/form-data'
    )

    data = json.loads(response.data)
    assert data["status"] == 404
    assert data["message"] == "Biometria não encontrada."


def test_validate_biometrics_generic_error(client, mocker, mock_encrypt, mock_decrypt, mock_expenses_auth, mock_expenses_register):
    """Testa o endpoint de validar biometria de usuário com erro generico."""

    payload_biometric_to_validate = {}

    file_content = b"This is a test file"
    file_content_validate = b"This is a validation of test file"
    file = BytesIO(file_content)
    file.name = "test_file.png"
    file_validate = BytesIO(file_content_validate)
    file_validate.name = "test_file.png"

    payload_biometrics["file"] = (file, file.name)
    payload_biometric_to_validate["file"] = (file_validate, file_validate.name)

    mocker.patch(
        "controllers.user_controller.UserController.validate_biometrics", side_effect=Exception("Erro ao validar biometria")
    )

    response = client.post("/create", json=payload_create)

    assert response.status_code == 200

    user_id = response.json["user"]

    response = client.put(
        f'/send_biometry/{user_id}',
        data=payload_biometrics,
        content_type='multipart/form-data'
    )

    assert response.status_code == 200

    response = client.post(
        f'/biometrics/{user_id}',
        data=payload_biometric_to_validate,
        content_type='multipart/form-data'
    )

    data = json.loads(response.data)
    assert response.status_code == 400
    assert data["status"] == 400
    assert data["message"] == "Erro ao validar biometria"


def test_biometrics_from_partner_success(client):
    """Testa o endpoint de biometria de parceiro com sucesso."""

    partner_biometrics = {}
    file_content = b"This is a test file"
    file = BytesIO(file_content)
    file.name = "test_file.png"

    partner_biometrics["file"] = (file, file.name)

    response = client.post(
        f'/send_biometry',
        data=partner_biometrics,
        content_type='multipart/form-data'
    )

    data = json.loads(response.data)
    assert response.status_code == 200
    assert data["status"] == "success"


def test_biometrics_from_partner_invalid_payload(client):
    """Testa o endpoint de briometria de usuário de parceiro com payload inválido."""
    partner_biometrics = {}
    response = client.post(
        f'/send_biometry',
        data=partner_biometrics,
        content_type='multipart/form-data'
    )

    data = json.loads(response.data)
    assert response.status_code == 422
    assert data["status"] == 422
    assert data["message"] == "Tipo de documento e arquivo são obrigatórios"


def test_biometrics_from_partner_generic_error(client, mocker):
    """Testa o endpoint de biometria de usuário de parceiro com erro generico."""

    partner_biometrics = {}
    file_content = b"This is a test file"
    file = BytesIO(file_content)
    file.name = "test_file.png"

    partner_biometrics["file"] = (file, file.name)

    mocker.patch(
        "controllers.user_controller.UserController.save_biometric_for_partner", side_effect=Exception("Erro ao salvar biometria")
    )

    response = client.post(
        f'/send_biometry',
        data=partner_biometrics,
        content_type='multipart/form-data'
    )

    data = json.loads(response.data)
    assert response.status_code == 400
    assert data["status"] == 400
    assert data["message"] == "Erro ao salvar biometria"


def test_get_biometrics_from_partner_success(client):
    """Testa o endpoint de buscar biometria de parceiro com sucesso."""

    partner_biometrics = {}
    file_content = b"This is a test file"
    file = BytesIO(file_content)
    file.name = "test_file.png"

    partner_biometrics["file"] = (file, file.name)

    response = client.post(
        f'/send_biometry',
        data=partner_biometrics,
        content_type='multipart/form-data'
    )
    user_id = response.json["user"]

    assert response.status_code == 200

    response = client.get(f"/get_biometry_status/{user_id}?integration=True")

    assert response.status_code == 200
    

def test_get_biometrics_from_partner_doesnt_exists(client):
    """Testa o endpoint de buscar biometria de usuário com usuário inexistente."""

    response = client.get("/get_biometry_status/664e9b2da3835b65a119b35d?integration=True")

    data = json.loads(response.data)
    assert response.status_code == 404
    assert data["status"] == 404
    assert data["message"] == "Biometria não encontrada."


def test_validate_biometrics_from_partner_success(
        client,
        mocker,
        mock_encrypt,
        mock_decrypt,
        mock_expenses_auth,
        mock_expenses_register,
        mock_validate_biometrics_true
    ):
    """Testa o endpoint de validar biometria de parceiro com sucesso."""
    partner_biometrics = {}
    file_content = b"This is a test file"
    file_content_validate = b"This is a validation of test file"
    file = BytesIO(file_content)
    file.name = "test_file.png"
    file_validate = BytesIO(file_content_validate)
    file_validate.name = "test_file.png"

    partner_biometrics["file"] = (file, file.name)
    payload_biometric_from_partner["file"] = (file_validate, file_validate.name)

    response = client.post(
        f'/send_biometry',
        data=partner_biometrics,
        content_type='multipart/form-data'
    )
    user_id = response.json["user"]

    response = client.post(
        f'/biometrics/{user_id}?integration=True',
        data=payload_biometric_from_partner,
        content_type='multipart/form-data'
    )
    assert response.status_code == 200


def test_validate_biometrics_from_partner_doesnt_match(
        client,
        mock_encrypt,
        mock_decrypt,
        mock_expenses_auth,
        mock_expenses_register,
        mock_validate_biometrics_false
    ):
    """Testa o endpoint de validar biometria de parceiro com biometria não reconhecida."""
    partner_biometrics = {}
    file_content = b"This is a test file"
    file_content_validate = b"This is a validation of test file"
    file = BytesIO(file_content)
    file.name = "test_file.png"
    file_validate = BytesIO(file_content_validate)
    file_validate.name = "test_file.png"

    partner_biometrics["file"] = (file, file.name)
    payload_biometric_from_partner["file"] = (file_validate, file_validate.name)

    response = client.post(
        f'/send_biometry',
        data=partner_biometrics,
        content_type='multipart/form-data'
    )
    user_id = response.json["user"]

    assert response.status_code == 200

    response = client.post(
        f'/biometrics/{user_id}',
        data=payload_biometric_from_partner,
        content_type='multipart/form-data'
    )
    data = json.loads(response.data)
    assert response.status_code == 400
    assert data["status"] == 400
    assert data["message"] == "Biometria inválida."
    

def test_validate_biometrics_from_partner_doesnt_exists(client):
    """Testa o endpoint de validar biometria de parceiro sem biometria cadastrada."""

    file_content = b"This is a test file"
    file_content_validate = b"This is a validation of test file"
    file = BytesIO(file_content)
    file.name = "test_file.png"
    file_validate = BytesIO(file_content_validate)
    file_validate.name = "test_file.png"

    payload_biometrics["file"] = (file, file.name)
    payload_biometric_from_partner["file"] = (file_validate, file_validate.name)

    response = client.post(
        '/biometrics/664e9b2da3835b65a119b35d',
        data=payload_biometric_from_partner,
        content_type='multipart/form-data'
    )

    data = json.loads(response.data)
    assert response.status_code == 404
    assert data["status"] == 404
    assert data["message"] == "Biometria não encontrada."