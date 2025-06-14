"""
Extensions module - Inicializa las extensiones de Flask
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
jwt = JWTManager()
migrate = Migrate()

# Configuración mejorada de CORS
cors = CORS(
    resources={
        r"/api/*": {
            "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    }
)
