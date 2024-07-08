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

payload_documents = {
    "document_type": "cnh",
    "mimetype": "image/png", 
    "file_extension": "png"
}

payload_biometrics = {
    "document_type": "biometrics",
    "mimetype": "image/png", 
    "file_extension": "png"
}

payload_biometric_from_partner = {"integration": True}

payload_update_balance = {
    "balance": 300.0
}

payload_expenses = {
    "reason": "Compras do mês",
    "value": 500.0,
    "category": "adb59d31-d222-44af-b24c-c3cfbd658b4c"
}
