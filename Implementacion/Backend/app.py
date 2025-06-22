from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from controllers.health_check import health_bp
from controllers.usuario_controller import UsuarioController
import logging

from config.database import Database, DATABASE_URI

from repositories.base_repository_impl import InstanceNotFoundError


db = SQLAlchemy()

def create_flask_app():
    flask_app = Flask(__name__)
    CORS(flask_app, origins=["http://localhost:4200"])

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("app.log"),  # Guardar logs en 'app.log'
            logging.StreamHandler()            # También mostrar logs en la consola
        ]
    )
    logger = logging.getLogger(__name__)



    flask_app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    db.init_app(flask_app)

    usuario_controller = UsuarioController()

    flask_app.register_blueprint(usuario_controller.blueprint, url_prefix='/usuarios')
    flask_app.register_blueprint(health_bp, url_prefix='/health_check')


    return flask_app

def run_app(flask_app: Flask):
    flask_app.run(host="0.0.0.0", port=8000)

app = create_flask_app()

if __name__ == "__main__":
    run_app(app)