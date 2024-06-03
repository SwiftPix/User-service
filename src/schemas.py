import base64
import re
import io
from datetime import datetime
from base64 import b64decode
from marshmallow import Schema, fields, validate, ValidationError, pre_load, post_load
from utils.index import validate_cpf, validate_cnpj

def validate_password_complexity(password):
    if len(password) < 8:
        raise ValidationError("A senha deve ter no mínimo 8 caracteres")
    
    if not re.search(r'[A-Z]', password):
        raise ValidationError("A senha deve conter pelo menos uma letra maiúscula")
    
    if not re.search(r'\d', password):
        raise ValidationError("A senha deve conter pelo menos um número")
    
    if not re.search(r'[!@#$%^&*()_+{}[\]:;<>,.?~\\-]', password):
        raise ValidationError("A senha deve conter pelo menos um caractere especial")


class UserSchema(Schema):
    name = fields.Str(required=True, 
                               validate=validate.Length(min=1, error="O nome completo é obrigatório"))
    
    email = fields.Email(required=True, 
                         error_messages={"required": "O endereço de e-mail é obrigatório", 
                                         "invalid": "O endereço de e-mail fornecido não é válido"})
    
    cellphone = fields.Str(required=True, 
                                 validate=validate.Regexp(r'^\+?\d+$', 
                                                         error="O número de telefone deve conter apenas dígitos"))
    
    password = fields.Str(required=True, 
                       validate=[validate.Length(min=8, error="A senha deve ter no mínimo 8 caracteres"),
                                 validate_password_complexity])
    cpf = fields.Str(required=False, validate=validate_cpf)
    cnpj = fields.Str(required=False, validate=validate_cnpj)
    currency = fields.Str(missing="real")
    agency = fields.Str(missing="0001")
    institution = fields.Str(missing="001")
    account = fields.Str(missing="000")
    balance = fields.Float(missing=0.0)

    @pre_load
    def validate(self, data, **kwargs):
        if not data.get('cpf') and not data.get('cnpj'):
            raise ValidationError("É necessário fornecer um cpf ou cnpj")
        return data


class LoginSchema(Schema):
    email = fields.Email(required=False, 
                         error_messages={"required": "O endereço de e-mail é obrigatório", 
                                         "invalid": "O endereço de e-mail fornecido não é válido"})
    
    password = fields.Str(required=True, 
                                validate=validate.Length(min=1, error="A senha é obrigatória"))
    
    cpf = fields.Str(required=False, validate=validate_cpf)
    cnpj = fields.Str(required=False, validate=validate_cnpj)

    @pre_load
    def validate(self, data, **kwargs):
        if not data.get('email') and not data.get('cpf') and not data.get('cnpj'):
            raise ValidationError("É necessário fornecer pelo menos um endereço de e-mail ou cpf/cnpj")
        return data

class ImageSchema(Schema):
    file_b64 = fields.Str(required=True, error_messages={"required": "O arquivo é obrigatório"})
    content_type = fields.Str(required=True, error_messages={"required": "O tipo do arquivo é obrigatório"})

class DocumentSchema(Schema):
    document_type = fields.Str(required=True, validate=validate.OneOf(["cnh", "rne", "rg"]))
    file = fields.Nested(ImageSchema, required=True)

    @pre_load
    def _prepare_file_field(self, data: dict = None, **kwargs) -> dict:
        file = data.get("file")
        if not file:
            raise ValidationError("É necessário fornecer um arquivo.")
        
        file_binary = file.read()
        file_b64 = base64.b64encode(file_binary).decode('utf-8')
        content_type = file.content_type

        file_data = {
            "file_b64": file_b64,
            "content_type": content_type
        }
        data.update({"file": file_data})
        return data
    
class BiometricSchema(Schema):
    file = fields.Nested(ImageSchema, required=True)

    @pre_load
    def _prepare_file_field(self, data: dict = None, **kwargs) -> dict:
        file = data.get("file")
        if not file:
            raise ValidationError("É necessário fornecer um arquivo.")
        
        file_binary = file.read()
        file_b64 = base64.b64encode(file_binary).decode('utf-8')
        content_type = file.content_type

        file_data = {
            "file_b64": file_b64,
            "content_type": content_type
        }
        data.update({"file": file_data})
        return data