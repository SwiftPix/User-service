from database.models import User
from utils.index import generate_random_password
from utils.exceptions import UserAlreadyExistsException, ValidationError, LoginException
from controllers.expenses_controller import ExpensesController

class UserController:
    @staticmethod
    def create_user(user):
        try:
            print(f"Recebido payload: {user}")
            required_keys = ["email", "cellphone", "name", "password", "account", "agency", "balance", "currency", "institution", "cpf"]
            for key in required_keys:
                if key not in user:
                    raise KeyError(f"Chave faltando no payload: {key}")

            email = user["email"]
            cpf = user.get("cpf", None)
            cnpj = user.get("cnpj", None)
            cellphone = user["cellphone"]
            name = user["name"]
            password = user["password"]
            account = user["account"]
            agency = user["agency"]
            balance = user["balance"]
            currency = user["currency"]
            institution = user["institution"]
            has_email = False
            has_cpf = False
            has_cnpj = False

            users = User.find()

            for existent_user in users:
                if email == existent_user.get("email", None):
                    has_email = True
                    break
                if cpf and cpf == existent_user.get("cpf", None):
                    has_cpf = True
                    break
                if cnpj and cnpj == existent_user.get("cnpj", None):
                    has_cnpj = True
                    break

            if has_email:
                raise UserAlreadyExistsException("Email já está cadastrado")
            if has_cpf:
                raise UserAlreadyExistsException("CPF já está cadastrado")
            if has_cnpj:
                raise UserAlreadyExistsException("CNPJ já está cadastrado")
            
            new_user = User(
                name=name,
                email=email,
                cpf=cpf,
                cnpj=cnpj,
                cellphone=cellphone,
                currency=currency,
                balance=balance,
                agency=agency,
                institution=institution,
                account=account,
                password=password,
                external_id=None  
            )
            user_id = new_user.save()
            return user_id
        except KeyError as e:
            print(f"Chave faltando no payload: {e}")
            raise ValidationError(f"Campo obrigatório ausente: {e}")
        except Exception as e:
            print(f"Erro ao criar usuário: {e}")
            raise

    @staticmethod
    def login(user_login):
        users = User.find()
        login = []
        for existent_user in users:
            user_dict = {
                "email": existent_user.get("email", None),
                "cpf": existent_user.get("cpf", None),
                "cnpj": existent_user.get("cnpj", None),
                "password": existent_user.get("password")
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
            return user
        else:
            raise LoginException("Usuário ou senha inválido")

    @staticmethod
    def field_in_list(users, field, value):
        for user in users:
            if user.get(field) == value:
                return user
        return None
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