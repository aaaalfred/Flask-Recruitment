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
cors = CORS()
