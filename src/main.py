from flask import Flask
from flask_cors import CORS
from views.api import bp as views_bp
from settings import settings

def create_app():
    app = Flask(__name__)
    
    # Aplicar CORS a todas as rotas e para todas as origens
    CORS(app, resources={r"/*": {"origins": "*"}})  # Atenção ao uso de "*", ajuste conforme necessário para segurança

    app.config.from_object(settings)
    app.register_blueprint(views_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=3000, debug=True, use_reloader=True)
