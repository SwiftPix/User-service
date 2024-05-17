from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from schemas import UserSchema, LoginSchema
from controllers.user_controller import UserController
from utils.exceptions import LoginException, UserAlreadyExistsException

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