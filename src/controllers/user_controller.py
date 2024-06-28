from database.models import PartnerBiometrics, User, Document
from controllers.crypt_controller import CryptController
from controllers.expenses_controller import ExpensesController
from utils.index import generate_random_password
from utils.exceptions import BiometricsNotFound, UserAlreadyExistsException, LoginException, UserNotFound, BiometricsNotValid
from utils.face_recog import validade_faces

class UserController:
    @staticmethod
    def create_user(user):
        email = user["email"]
        cpf = user.get("cpf", None)
        cnpj = user.get("cnpj", None)
        has_email = False
        has_cpf = False
        has_cnpj = False

        users = User.find()

        crypted_email = CryptController.encrypt(email)
        crypted_cpf = CryptController.encrypt(cpf)
        crypted_cnpj = CryptController.encrypt(cnpj)
        crypted_password = CryptController.encrypt(user["password"])

        for existent_user in users:
            decrypt_email = CryptController.decrypt(existent_user.get("email", None))
            decrypt_cpf = CryptController.decrypt(existent_user.get("cpf", None))
            decrypt_cnpj = CryptController.decrypt(existent_user.get("cnpj", None))
            if email and email == decrypt_email:
                has_email = True
                break
            if cpf and cpf == decrypt_cpf:
                has_cpf = True
                break
            if cnpj and cnpj == decrypt_cnpj:
                has_cnpj = True
                break

        if has_email:
            raise UserAlreadyExistsException("Email já está cadastrado")
        if has_cpf:
            raise UserAlreadyExistsException("CPF já está cadastrado")
        if has_cnpj:
            raise UserAlreadyExistsException("CNPJ já está cadastrado")
        
        ExpensesController.auth()
        integration_password = generate_random_password()
        external_id = ExpensesController.register(email, integration_password)

        new_user = User(
            name=user["name"],
            email=crypted_email,
            cpf=crypted_cpf,
            cnpj=crypted_cnpj,
            cellphone=user["cellphone"],
            currency=user["currency"],
            balance=user["balance"],
            agency=user.get("agency"),
            institution=user.get("institution"),
            account=user.get("account"),
            password=crypted_password,
            external_id=external_id
        )

        user_id = new_user.save()

        return user_id

    @staticmethod
    def login(user_login):
        users = User.find()
        login = []
        for existent_user in users:
            decrypt_email = CryptController.decrypt(existent_user.get("email", None))
            decrypt_cpf = CryptController.decrypt(existent_user.get("cpf", None))
            decrypt_cnpj = CryptController.decrypt(existent_user.get("cnpj", None))
            decrypt_password = CryptController.decrypt(existent_user.get("password"))
            user_dict = {
                "email": decrypt_email,
                "cpf": decrypt_cpf,
                "cnpj": decrypt_cnpj,
                "password": decrypt_password
            }
            login.append(user_dict)

        if user_login.get("email"):
            field = "email"
            user = UserController.field_in_list(login, field, user_login.get("email"))
        elif user_login.get("cpf"):
            field = "cpf"
            user = UserController.field_in_list(login, field, user_login.get("cpf"))
        else:
            field = "cnpj"
            user = UserController.field_in_list(login, field, user_login.get("cnpj"))

        if not user:
            raise LoginException("Usuário ou senha inválido")

        if user["password"] == user_login["password"]:
            return 
        else:
            raise LoginException("Usuário ou senha inválido")
        
    @staticmethod
    def field_in_list(list, field, field_value):
        for dict in list:
            if dict.get(field) == field_value:
                return dict
        return
        
    @staticmethod
    def find_user_by_id(user_id):
        user = User.find_by_id(user_id)

        if not user:
            raise UserNotFound("Usuário não encontrado")
        user["_id"] = str(user["_id"])
        user.pop("password")
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
    
    @staticmethod
    def create_expense(user_id, expense):
        user = UserController.find_user_by_id(user_id)
        external_id = user["external_id"]
        return ExpensesController.create_expense(external_id, expense["reason"], expense["value"], expense["category"])

    @staticmethod
    def get_expenses(user_id):
        user = UserController.find_user_by_id(user_id)
        external_id = user["external_id"]
        return ExpensesController.list_expenses(external_id)