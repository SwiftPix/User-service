import bcrypt, sys
from database.models import PartnerBiometrics, User, Document
from utils.exceptions import BiometricsNotFound, UserAlreadyExistsException, LoginException, UserNotFound, BiometricsNotValid
from utils.face_recog import validade_faces

class UserController:
    @staticmethod
    def create_user(user):
        email = user["email"]
        cpf = user.get("cpf", "")
        cnpj = user.get("cnpj", "")
        has_email = False
        has_cpf = False
        has_cnpj = False

        users = User.find()

        for existent_user in users:
            if existent_user.get('email') == email:
                has_email = True
                break
            if existent_user.get('cpf') == cpf:
                has_cpf = True
                break
            if existent_user.get('cnpj') == cnpj:
                has_cnpj = True
                break

        if has_email:
            raise UserAlreadyExistsException("Email já está cadastrado")
        if has_cpf:
            raise UserAlreadyExistsException("CPF já está cadastrado")
        if has_cnpj:
            raise UserAlreadyExistsException("CNPJ já está cadastrado")

        hash_password, salt = User.create_hash_password(user["password"])

        new_user = User(
            name=user["name"],
            email=email,
            cpf=user.get("cpf"),
            cnpj=user.get("cnpj"),
            cellphone=user["cellphone"],
            currency=user["currency"],
            balance=user["balance"],
            agency=user.get("agency"),
            institution=user.get("institution"),
            account=user.get("account"),
            password=hash_password,
            salt=salt
        )

        user_id = new_user.save()

        return user_id

    @staticmethod
    def login(user_login):
        if user_login.get("email"):
            user = User.find_by_email(user_login["email"])
        elif user_login.get("cpf"):
            user = User.find_by_cpf(user_login["cpf"])
        else:
            user = User.find_by_cnpj(user_login["cnpj"])

        if not user:
            raise LoginException("Usuário ou senha inválido")
        
        saved_salt = user["salt"]
        saved_hash = user["password"]

        provided_password = bcrypt.hashpw(user_login["password"].encode('utf-8'), saved_salt)
        if provided_password == saved_hash:
            return 
        else:
            raise LoginException("Usuário ou senha inválido")
        
    @staticmethod
    def find_user_by_id(user_id):
        user = User.find_by_id(user_id)

        if not user:
            raise UserNotFound("Usuário não encontrado")
        user["_id"] = str(user["_id"])
        user.pop("password")
        user.pop("salt")
        return user
        
    @staticmethod
    def create_document(document, user_id):

        UserController.find_user_by_id(user_id)

        new_document = Document(
            document_type=document["document_type"],
            file=document["file"],
            user_id=user_id
        )

        document_id = new_document.save()

        return document_id
    
    @staticmethod
    def save_biometric(biometric, user_id):

        UserController.find_user_by_id(user_id)

        new_biometric = Document(
            document_type="biometrics",
            file=biometric["file"],
            user_id=user_id
        )

        biometric_id = new_biometric.save()

        return biometric_id
    
    @staticmethod
    def save_biometric_for_partner(biometric):

        new_biometric = PartnerBiometrics(
            file=biometric["file"]
        )

        user_id = new_biometric.save()

        return user_id
    
    @staticmethod
    def validate_biometrics(image, user_id, is_from_partner):

        biometric = UserController.get_biometric(user_id, is_from_partner)
        
        is_valid = validade_faces(image, biometric)

        if is_valid:
            return True
        else:
            raise BiometricsNotValid("Biometria inválida.")
        
    @staticmethod
    def get_biometric(user_id, is_from_partner):
        biometric = []
        if is_from_partner == "true":
            user = PartnerBiometrics.find_by_user_id(user_id)
            user = list(user)
            for item in user:
                biometric = item["file"]["file_b64"]
        else:
            user = UserController.find_user_by_id(user_id)
            for document in user["documents"]:
                if document["document_type"] == "biometrics":
                    biometric = document["file"]["file_b64"]

        if not biometric:
            raise BiometricsNotFound("Biometria não encontrada.")

        return biometric

    @staticmethod
    def get_balance(user_id):
        user = UserController.find_user_by_id(user_id)
        
        result = {
            "balance": user.get("balance"),
            "currency": user.get("currency")
        }
        return result
    
    @staticmethod
    def update_balance(balance, user_id): 
        UserController.find_user_by_id(user_id)

        updated_user = User.update(balance, user_id)

        return updated_user
