import sys
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from views.api import bp as views_bp
from settings import settings
from controllers.user_controller import UserController

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

def create_app():
    app = Flask(__name__)
    
    # Permitir todas as origens com CORS
    CORS(app, resources={r"/*": {"origins": "*"}})

    app.config.from_object(settings)
    app.register_blueprint(views_bp)
    
    return app

app = create_app()

@app.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    print(f"Dados recebidos na rota /create: {data}")
    try:
        # Chame o método para criar o usuário
        user_id = UserController.create_user(data)
        return jsonify({"user_id": str(user_id)}), 201
    except Exception as e:
        print(f"Erro ao processar requisição: {e}")
        return jsonify({"error": str(e)}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    print(f"Dados recebidos na rota /login: {data}")
    try:
        user = UserController.authenticate_user(data)
        if user:
            return jsonify({"message": "Login bem-sucedido"}), 200
        else:
            return jsonify({"error": "Credenciais inválidas"}), 401
    except Exception as e:
        print(f"Erro ao processar requisição na rota /login: {e}")
        return jsonify({"error": str(e)}), 400

@app.errorhandler(Exception)
def handle_exception(e):
    print(f"Erro global: {e}")
    return jsonify({"error": "Ocorreu um erro interno"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True, use_reloader=True)
