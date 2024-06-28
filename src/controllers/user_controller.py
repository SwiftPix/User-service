from database.models import User
from utils.index import generate_random_password
from utils.exceptions import UserAlreadyExistsException, ValidationError
from database.models import User
from utils.exceptions import UserNotFoundException, InvalidCredentialsException

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
            
            # Criação de usuário sem a chamada ao ExpensesController
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
                external_id=None  # Pode ser None ou qualquer valor padrão
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
    def authenticate_user(data):
            try:
                cpf = data.get('cpf')
                password = data.get('password')
                user = User.find_one({"cpf": cpf, "password": password})
                if user:
                    return user
                else:
                    raise InvalidCredentialsException("Credenciais inválidas")
            except Exception as e:
                print(f"Erro ao autenticar usuário: {e}")
                raise