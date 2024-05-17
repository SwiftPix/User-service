import bcrypt
from database.models import User
from utils.exceptions import UserAlreadyExistsException, LoginException

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
