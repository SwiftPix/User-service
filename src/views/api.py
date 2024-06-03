from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from schemas import DocumentSchema, UserSchema, LoginSchema
from controllers.user_controller import UserController
from utils.exceptions import LoginException, UserAlreadyExistsException, UserNotFound

bp = Blueprint("user", __name__)

@bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "message": "Service is healthy"})

@bp.route("/create", methods=["POST"])
def create_user():
    try:
        payload = request.get_json()
        validated_user = UserSchema().load(payload)
        id = UserController.create_user(validated_user)

        return jsonify({"status": "success", "message": f"Usuário criado com sucesso. ID: {id}"})
    except UserAlreadyExistsException as e:
        return jsonify({"status": 409, "message": str(e)}), 409
    except ValidationError as e:
        return jsonify({"status": 422, "message": str(e)}), 422
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
    except (LoginException, Exception) as e:
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
        return jsonify({"status": "success", "message": f"Documento criado com sucesso. ID: {id}"})
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
        if not balance:
            raise ValidationError("Valor a ser atualizado é obrigatório")

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