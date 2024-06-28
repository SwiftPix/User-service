from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from schemas import DocumentSchema, ExpensesSchema, UserSchema, LoginSchema, BiometricSchema
from controllers.user_controller import UserController
from flask_cors import CORS
from controllers.expenses_controller import ExpensesController
from utils.exceptions import BiometricsNotFound, BiometricsNotValid, ExpensesException, LoginException, UserAlreadyExistsException, UserNotFound

bp = Blueprint("user", __name__)
CORS(bp)  


@bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "message": "Service is healthy"})

@bp.route("/create", methods=["POST"])
def create_user():
    try:
        payload = request.get_json()
        validated_user = UserSchema().load(payload)
        id = UserController.create_user(validated_user)

        return jsonify({"status": "success", "message": f"Usuário criado com sucesso.", "user": str(id)})
    except UserAlreadyExistsException as e:
        return jsonify({"status": 409, "message": str(e)}), 409
    except ValidationError as e:
        return jsonify({"status": 422, "message": str(e)}), 422
    except Exception as e:
        return jsonify({"status": 400, "message": str(e)}), 400
    
@bp.route("/user/<user_id>", methods=["GET"])
def get_user(user_id):
    try:
        user = UserController.find_user_by_id(user_id)

        return user
    except UserNotFound as e:
        return jsonify({"status": 404, "message": str(e)}), 404
    except Exception as e:
        return jsonify({"status": 400, "message": str(e)}), 400

@bp.route("/login", methods=["POST"])
def login():
    try:
        payload = request.get_json()
        user = LoginSchema().load(payload)
        UserController.login(user)

        return jsonify({"status": "success", "message": "Usuário entrou"})
    except ValidationError as e:
        return jsonify({"status": 422, "message": str(e)}), 422
    except BiometricsNotFound as e:
        return jsonify({"status": 404, "message": str(e)}), 404
    except (LoginException, Exception) as e:
        return jsonify({"status": 400, "message": str(e)}), 400

@bp.route("/get_biometry_status/<user_id>", methods=["GET"])
def get_biometry_status(user_id):
    try:
        _ = UserController.get_biometric(user_id)

        return jsonify({"status": "success", "message": f"Cadastrado.", "user": str(user_id)})
    except Exception as e:
        return jsonify({"status": 400, "message": str(e)}), 400

@bp.route("/send_biometry/<user_id>", methods=["PUT"])
def send_biometry(user_id):
    try:
        file = request.files.get("file")

        if not file:
            raise ValidationError("Arquivo é  obrigatório")

        payload = {
            "file": file
        }

        biometric = BiometricSchema().load(payload)

        id = UserController.save_biometric(biometric, user_id)
        if not id:
            return jsonify({"status": "success", "message": f"Nenhuma biometra inserida."}) 
        return jsonify({"status": "success", "message": f"Biometria criada com sucesso.", "user": str(id)})
    except ValidationError as e:
        return jsonify({"status": 422, "message": str(e)}), 422
    except BiometricsNotFound as e:
        return jsonify({"status": 404, "message": str(e)}), 404
    except UserNotFound as e:
        return jsonify({"status": 404, "message": str(e)}), 404
    except (BiometricsNotValid, Exception) as e:
        return jsonify({"status": 400, "message": str(e)}), 400
    
@bp.route("/documents/<user_id>", methods=["PUT"])
def send_documents(user_id):
    try:
        document_type = request.form.get("document_type")
        file = request.files.get("file")

        if not document_type or not file:
            raise ValidationError("Tipo de documento e arquivo são obrigatórios")

        payload = {
            "document_type": document_type,
            "file": file
        }
        
        document = DocumentSchema().load(payload)

        id = UserController.create_document(document, user_id)
        if not id:
            return jsonify({"status": "success", "message": f"Nenhum documento inserido."}) 
        return jsonify({"status": "success", "message": f"Documento anexado com sucesso.", "user": str(id)})
    except ValidationError as e:
        return jsonify({"status": 422, "message": str(e)}), 422
    except UserNotFound as e:
        return jsonify({"status": 404, "message": str(e)}), 404
    except Exception as e:
        return jsonify({"status": 400, "message": str(e)}), 400
    
@bp.route("/biometrics/<user_id>", methods=["POST"])
def validate_biometrics(user_id):
    try:
        image = request.files.get("file")
        is_from_partner = request.form.get("integration", "False")
        is_from_partner = is_from_partner.lower()

        if not image:
            raise ValidationError("A imagem é obrigatória.")
        
        valid = UserController.validate_biometrics(image, user_id, is_from_partner)

        if not valid:
            return jsonify({"status": "success", "message": f"A validação biométrica falhou."}) 
        return jsonify({"status": "success", "message": f"Biometria validada com sucesso!"})
    except ValidationError as e:
        return jsonify({"status": 422, "message": str(e)}), 422
    except UserNotFound as e:
        return jsonify({"status": 404, "message": str(e)}), 404
    except Exception as e:
        return jsonify({"status": 400, "message": str(e)}), 400
    
@bp.route("/balance/<user_id>", methods=["GET"])
def get_balance(user_id):
    try:
        response = UserController.get_balance(user_id)
        return response
    except UserNotFound as e:
        return jsonify({"status": 404, "message": str(e)}), 404
    except Exception as e:
        return jsonify({"status": 400, "message": str(e)}), 400
    
@bp.route("/balance/<user_id>", methods=["PATCH"])
def update_balance(user_id):
    try:
        payload = request.get_json()
        balance = payload.get("balance")
        if not balance or not isinstance(balance, float):
            raise ValidationError("Valor a ser atualizado é um número e obrigatório")

        updated_user = UserController.update_balance(balance, user_id)
        if not updated_user:
            return jsonify({"status": "success", "message": f"Nenhum saldo alterado."}) 
        return jsonify({"status": "success", "message": f"Usuário atualizado."})
    except ValidationError as e:
        return jsonify({"status": 422, "message": str(e)}), 422
    except UserNotFound as e:
        return jsonify({"status": 404, "message": str(e)}), 404
    except Exception as e:
        return jsonify({"status": 400, "message": str(e)}), 400
    
@bp.route("/send_biometry", methods=["POST"])
def create_biometriy_for_partner():
    try:
        file = request.files.get("file")

        if not file:
            raise ValidationError("Tipo de documento e arquivo são obrigatórios")

        payload = {
            "file": file
        }

        biometric = BiometricSchema().load(payload)

        id = UserController.save_biometric_for_partner(biometric)
        if not id:
            return jsonify({"status": "success", "message": f"Nenhuma biometra inserida."}) 
        return jsonify({"status": "success", "message": f"Biometria criada com sucesso.", "user": str(id)})
    except ValidationError as e:
        return jsonify({"status": 422, "message": str(e)}), 422
    except Exception as e:
        return jsonify({"status": 400, "message": str(e)}), 400
    
@bp.route("/expense/<user_id>", methods=["POST"])
def create_expense(user_id):
    try:
        payload = request.get_json()
        validated_expense = ExpensesSchema().load(payload)
        expense= UserController.create_expense(user_id, validated_expense)

        return expense
    except UserNotFound as e:
        return jsonify({"status": 404, "message": str(e)}), 404
    except (ExpensesException, Exception) as e:
        return jsonify({"status": 400, "message": str(e)}), 400
    
@bp.route("/expense/<user_id>", methods=["GET"])
def get_expenses(user_id):
    try:
        response = UserController.get_expenses(user_id)
        return jsonify({"status": "success", "result": response})
    except UserNotFound as e:
        return jsonify({"status": 404, "message": str(e)}), 404
    except (ExpensesException, Exception) as e:
        return jsonify({"status": 400, "message": str(e)}), 400

@bp.route("/expenses", methods=["GET"])
def get_expenses_categories():
    try:
        response = ExpensesController.list_expenses_categories()
        return jsonify({"status": "success", "result": response})
    except UserNotFound as e:
        return jsonify({"status": 404, "message": str(e)}), 404
    except (ExpensesException, Exception) as e:
        return jsonify({"status": 400, "message": str(e)}), 400
    


