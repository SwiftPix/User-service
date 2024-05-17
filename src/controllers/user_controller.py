import bcrypt
from database.models import User
from utils.exceptions import UserAlreadyExistsException, LoginException

class UserController:
    @staticmethod
    def create_user(user):
        email = user["email"]
        if User.find_by_email(email):
            raise UserAlreadyExistsException("Email já está cadastrado")

        hash_password, salt = User.create_hash_password(user["password"])

        new_user = User(
            name=user["name"],
            email=email,
            cellphone=user["cellphone"],
            password=hash_password,
            salt=salt
        )

        user_id = new_user.save()

        return user_id

    @staticmethod
    def login(user_login):
        user = User.find_by_email(user_login["email"])

        if not user:
            raise LoginException("Usuário ou senha inválido")
        
        saved_salt = user["salt"]
        saved_hash = user["password"]

        provided_password = bcrypt.hashpw(user_login["password"].encode('utf-8'), saved_salt)
        if provided_password == saved_hash:
            return 
        else:
            raise LoginException("Usuário ou senha inválido")
