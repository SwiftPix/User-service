from datetime import datetime, timezone

def default_datetime():
    return datetime.now().astimezone(timezone.utc)
    
def validate_cnpj(cnpj):
    cnpj = ''.join(filter(str.isdigit, cnpj))
    if len(cnpj) != 14:
        return False
    if cnpj == cnpj[0] * 14:
        return False

    soma = 0
    peso = 5
    for i in range(12):
        soma += int(cnpj[i]) * peso
        peso -= 1
        if peso == 1:
            peso = 9

    digito1 = 11 - (soma % 11)
    if digito1 > 9:
        digito1 = 0
    if int(cnpj[12]) != digito1:
        return False

    soma = 0
    peso = 6
    for i in range(13):
        soma += int(cnpj[i]) * peso
        peso -= 1
        if peso == 1:
            peso = 9

    digito2 = 11 - (soma % 11)
    if digito2 > 9:
        digito2 = 0

    if int(cnpj[13]) != digito2:
        return False

    return True

def validate_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) != 11:
        return False

    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = 11 - (soma % 11)
    if digito1 > 9:
        digito1 = 0
    if int(cpf[9]) != digito1:
        return False

    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = 11 - (soma % 11)
    if digito2 > 9:
        digito2 = 0
    if int(cpf[10]) != digito2:
        return False

    return True

