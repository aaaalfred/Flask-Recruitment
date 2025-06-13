# Sistema de Gestión de Vacantes y Candidatos
# Flask + SQLAlchemy + MySQL + AWS S3

# requirements.txt
"""
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-Login==0.6.3
Flask-JWT-Extended==4.5.3
Flask-CORS==4.0.0
Flask-Migrate==4.0.5
PyMySQL==1.1.0
boto3==1.28.85
python-dotenv==1.0.0
Werkzeug==2.3.7
marshmallow==3.20.1
flask-marshmallow==0.15.0
marshmallow-sqlalchemy==0.29.0
"""

# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database Configuration
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or 'password'
    MYSQL_DB = os.environ.get('MYSQL_DB') or 'recruitment_system'
    
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # AWS S3 Configuration
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_S3_BUCKET = os.environ.get('AWS_S3_BUCKET')
    AWS_S3_REGION = os.environ.get('AWS_S3_REGION') or 'us-east-1'
    
    # File Upload Configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'jpg', 'jpeg', 'png'}
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-string'
    JWT_ACCESS_TOKEN_EXPIRES = False

# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from config import Config

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
jwt = JWTManager()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    
    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
    
    # Register blueprints
    from routes.auth_routes import auth_bp
    from routes.usuario_routes import usuario_bp
    from routes.vacante_routes import vacante_bp
    from routes.candidato_routes import candidato_bp
    from routes.documento_routes import documento_bp
    from routes.entrevista_routes import entrevista_bp
    from routes.candidatos_posiciones_routes import candidatos_posiciones_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(usuario_bp, url_prefix='/api/usuarios')
    app.register_blueprint(vacante_bp, url_prefix='/api/vacantes')
    app.register_blueprint(candidato_bp, url_prefix='/api/candidatos')
    app.register_blueprint(documento_bp, url_prefix='/api/documentos')
    app.register_blueprint(entrevista_bp, url_prefix='/api/entrevistas')
    app.register_blueprint(candidatos_posiciones_bp, url_prefix='/api/candidatos-posiciones')
    
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)

# models/__init__.py
from app import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Tabla intermedia para relación muchos a muchos
class CandidatosPositions(db.Model):
    __tablename__ = 'candidatos_posiciones'
    
    id = db.Column(db.Integer, primary_key=True)
    candidato_id = db.Column(db.Integer, db.ForeignKey('candidato.id'), nullable=False)
    vacante_id = db.Column(db.Integer, db.ForeignKey('vacante.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='postulado')
    nota = db.Column(db.Text)
    fecha_asignacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    candidato = db.relationship('Candidato', backref='posiciones_rel')
    vacante = db.relationship('Vacante', backref='candidatos_rel')

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuario'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.Enum('ejecutivo', 'reclutador', 'reclutador_lider'), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    vacantes_ejecutivo = db.relationship('Vacante', foreign_keys='Vacante.ejecutivo_id', backref='ejecutivo')
    vacantes_reclutador = db.relationship('Vacante', foreign_keys='Vacante.reclutador_id', backref='reclutador')
    vacantes_lider = db.relationship('Vacante', foreign_keys='Vacante.reclutador_lider_id', backref='reclutador_lider')
    candidatos = db.relationship('Candidato', backref='reclutador_asignado')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'rol': self.rol,
            'activo': self.activo,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }

class Vacante(db.Model):
    __tablename__ = 'vacante'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    fecha_solicitud = db.Column(db.DateTime, default=datetime.utcnow)
    ejecutivo_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    reclutador_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    reclutador_lider_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    vacantes = db.Column(db.Integer, default=1)
    estado = db.Column(db.Enum('abierta', 'pausada', 'cerrada', 'cancelada'), default='abierta')
    prioridad = db.Column(db.Enum('baja', 'media', 'alta', 'critica'), default='media')
    salario_min = db.Column(db.Decimal(10, 2))
    salario_max = db.Column(db.Decimal(10, 2))
    ubicacion = db.Column(db.String(100))
    modalidad = db.Column(db.Enum('presencial', 'remoto', 'hibrido'))
    fecha_limite = db.Column(db.DateTime)
    comentarios = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    entrevistas = db.relationship('Entrevista', backref='vacante_rel', cascade='all, delete-orphan')
    candidatos_posiciones = db.relationship('CandidatosPositions', backref='vacante_rel', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'fecha_solicitud': self.fecha_solicitud.isoformat() if self.fecha_solicitud else None,
            'ejecutivo_id': self.ejecutivo_id,
            'reclutador_id': self.reclutador_id,
            'reclutador_lider_id': self.reclutador_lider_id,
            'vacantes': self.vacantes,
            'estado': self.estado,
            'prioridad': self.prioridad,
            'salario_min': float(self.salario_min) if self.salario_min else None,
            'salario_max': float(self.salario_max) if self.salario_max else None,
            'ubicacion': self.ubicacion,
            'modalidad': self.modalidad,
            'fecha_limite': self.fecha_limite.isoformat() if self.fecha_limite else None,
            'comentarios': self.comentarios,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'ejecutivo': self.ejecutivo.nombre if self.ejecutivo else None,
            'reclutador': self.reclutador.nombre if self.reclutador else None,
            'reclutador_lider': self.reclutador_lider.nombre if self.reclutador_lider else None
        }

class Candidato(db.Model):
    __tablename__ = 'candidato'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefono = db.Column(db.String(20))
    cv_url = db.Column(db.String(500))
    estado = db.Column(db.Enum('activo', 'inactivo', 'blacklist'), default='activo')
    comentarios_finales = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    reclutador_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    salario_esperado = db.Column(db.Decimal(10, 2))
    experiencia_anos = db.Column(db.Integer)
    ubicacion = db.Column(db.String(100))
    disponibilidad = db.Column(db.Enum('inmediata', '15_dias', '30_dias', 'a_convenir'))
    nivel_ingles = db.Column(db.Enum('basico', 'intermedio', 'avanzado', 'nativo'))
    linkedin_url = db.Column(db.String(200))
    
    # Relationships
    documentos = db.relationship('Documento', backref='candidato_rel', cascade='all, delete-orphan')
    entrevistas = db.relationship('Entrevista', backref='candidato_rel', cascade='all, delete-orphan')
    candidatos_posiciones = db.relationship('CandidatosPositions', backref='candidato_rel', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'telefono': self.telefono,
            'cv_url': self.cv_url,
            'estado': self.estado,
            'comentarios_finales': self.comentarios_finales,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'reclutador_id': self.reclutador_id,
            'salario_esperado': float(self.salario_esperado) if self.salario_esperado else None,
            'experiencia_anos': self.experiencia_anos,
            'ubicacion': self.ubicacion,
            'disponibilidad': self.disponibilidad,
            'nivel_ingles': self.nivel_ingles,
            'linkedin_url': self.linkedin_url,
            'reclutador': self.reclutador_asignado.nombre if self.reclutador_asignado else None
        }

class Documento(db.Model):
    __tablename__ = 'documento'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre_original = db.Column(db.String(200), nullable=False)
    url_s3 = db.Column(db.String(500), nullable=False)
    key_s3 = db.Column(db.String(500), nullable=False)
    tipo = db.Column(db.Enum('cv', 'certificado', 'comprobante', 'otro'), nullable=False)
    candidato_id = db.Column(db.Integer, db.ForeignKey('candidato.id'), nullable=False)
    tamaño_bytes = db.Column(db.Integer)
    content_type = db.Column(db.String(100))
    fecha_subida = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre_original': self.nombre_original,
            'url_s3': self.url_s3,
            'tipo': self.tipo,
            'candidato_id': self.candidato_id,
            'tamaño_bytes': self.tamaño_bytes,
            'content_type': self.content_type,
            'fecha_subida': self.fecha_subida.isoformat() if self.fecha_subida else None
        }

class Entrevista(db.Model):
    __tablename__ = 'entrevista'
    
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False)
    tipo = db.Column(db.Enum('telefonica', 'video', 'presencial', 'tecnica'), nullable=False)
    resultado = db.Column(db.Enum('pendiente', 'aprobada', 'rechazada', 'reprogramar'), default='pendiente')
    comentarios = db.Column(db.Text)
    puntuacion = db.Column(db.Integer)  # 1-10
    candidato_id = db.Column(db.Integer, db.ForeignKey('candidato.id'), nullable=False)
    vacante_id = db.Column(db.Integer, db.ForeignKey('vacante.id'), nullable=False)
    entrevistador_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    duracion_minutos = db.Column(db.Integer)
    ubicacion = db.Column(db.String(200))  # Para presenciales o link para video
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    entrevistador = db.relationship('Usuario', backref='entrevistas_realizadas')
    
    def to_dict(self):
        return {
            'id': self.id,
            'fecha': self.fecha.isoformat() if self.fecha else None,
            'tipo': self.tipo,
            'resultado': self.resultado,
            'comentarios': self.comentarios,
            'puntuacion': self.puntuacion,
            'candidato_id': self.candidato_id,
            'vacante_id': self.vacante_id,
            'entrevistador_id': self.entrevistador_id,
            'duracion_minutos': self.duracion_minutos,
            'ubicacion': self.ubicacion,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'candidato': self.candidato_rel.nombre if self.candidato_rel else None,
            'vacante': self.vacante_rel.nombre if self.vacante_rel else None,
            'entrevistador': self.entrevistador.nombre if self.entrevistador else None
        }

# services/s3_service.py
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
import uuid
import os
from flask import current_app

class S3Service:
    def __init__(self):
        self.s3_client = None
        self.bucket_name = None
        self._initialize_client()
    
    def _initialize_client(self):
        try:
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
                aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'],
                region_name=current_app.config['AWS_S3_REGION']
            )
            self.bucket_name = current_app.config['AWS_S3_BUCKET']
        except Exception as e:
            current_app.logger.error(f"Error inicializando cliente S3: {str(e)}")
            raise
    
    def upload_file(self, file_obj, file_name, content_type, folder='documents'):
        """
        Sube un archivo a S3 y retorna la URL y key
        """
        try:
            # Generar nombre único para el archivo
            file_extension = os.path.splitext(file_name)[1]
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            key = f"{folder}/{unique_filename}"
            
            # Subir archivo
            self.s3_client.upload_fileobj(
                file_obj,
                self.bucket_name,
                key,
                ExtraArgs={
                    'ContentType': content_type,
                    'ACL': 'private'  # Archivos privados por defecto
                }
            )
            
            # Generar URL
            url = f"https://{self.bucket_name}.s3.{current_app.config['AWS_S3_REGION']}.amazonaws.com/{key}"
            
            return {
                'success': True,
                'url': url,
                'key': key,
                'message': 'Archivo subido exitosamente'
            }
            
        except NoCredentialsError:
            return {
                'success': False,
                'error': 'Credenciales de AWS no configuradas correctamente'
            }
        except ClientError as e:
            return {
                'success': False,
                'error': f'Error del cliente S3: {str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Error inesperado: {str(e)}'
            }
    
    def delete_file(self, key):
        """
        Elimina un archivo de S3
        """
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=key)
            return {'success': True, 'message': 'Archivo eliminado exitosamente'}
        except ClientError as e:
            return {'success': False, 'error': f'Error eliminando archivo: {str(e)}'}
    
    def generate_presigned_url(self, key, expiration=3600):
        """
        Genera una URL firmada para descargar un archivo privado
        """
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': key},
                ExpiresIn=expiration
            )
            return {'success': True, 'url': url}
        except ClientError as e:
            return {'success': False, 'error': f'Error generando URL: {str(e)}'}

# services/auth_service.py
from functools import wraps
from flask import jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from models import Usuario

def token_required(f):
    @wraps(f)
    @jwt_required()
    def decorated(*args, **kwargs):
        try:
            current_user_id = get_jwt_identity()
            current_user = Usuario.query.get(current_user_id)
            if not current_user or not current_user.activo:
                return jsonify({'message': 'Token inválido o usuario inactivo'}), 401
            return f(current_user, *args, **kwargs)
        except Exception as e:
            return jsonify({'message': 'Token inválido'}), 401
    return decorated

def role_required(*allowed_roles):
    def decorator(f):
        @wraps(f)
        @token_required
        def decorated(current_user, *args, **kwargs):
            if current_user.rol not in allowed_roles:
                return jsonify({'message': 'Permisos insuficientes'}), 403
            return f(current_user, *args, **kwargs)
        return decorated
    return decorator

def authenticate_user(email, password):
    """Autentica un usuario y retorna un token JWT"""
    try:
        user = Usuario.query.filter_by(email=email, activo=True).first()
        if user and user.check_password(password):
            access_token = create_access_token(identity=user.id)
            return {
                'success': True,
                'access_token': access_token,
                'user': user.to_dict()
            }
        return {'success': False, 'message': 'Credenciales inválidas'}
    except Exception as e:
        return {'success': False, 'message': f'Error de autenticación: {str(e)}'}

# routes/auth_routes.py
from flask import Blueprint, request, jsonify
from services.auth_service import authenticate_user
from models import Usuario, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'message': 'Email y contraseña son requeridos'}), 400
        
        result = authenticate_user(email, password)
        
        if result['success']:
            return jsonify({
                'message': 'Login exitoso',
                'access_token': result['access_token'],
                'user': result['user']
            }), 200
        else:
            return jsonify({'message': result['message']}), 401
            
    except Exception as e:
        return jsonify({'message': f'Error en login: {str(e)}'}), 500

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        required_fields = ['nombre', 'email', 'password', 'rol']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'message': f'{field} es requerido'}), 400
        
        # Verificar si el email ya existe
        existing_user = Usuario.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({'message': 'El email ya está registrado'}), 400
        
        # Crear nuevo usuario
        new_user = Usuario(
            nombre=data['nombre'],
            email=data['email'],
            rol=data['rol']
        )
        new_user.set_password(data['password'])
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            'message': 'Usuario creado exitosamente',
            'user': new_user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error creando usuario: {str(e)}'}), 500

# utils/file_utils.py
import os
from flask import current_app

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def get_file_size(file_obj):
    file_obj.seek(0, os.SEEK_END)
    size = file_obj.tell()
    file_obj.seek(0)
    return size

def validate_file_upload(file):
    """Valida que el archivo cumple con los requisitos"""
    if not file or file.filename == '':
        return {'valid': False, 'error': 'No se seleccionó ningún archivo'}
    
    if not allowed_file(file.filename):
        return {'valid': False, 'error': 'Tipo de archivo no permitido'}
    
    # Verificar tamaño
    file_size = get_file_size(file)
    if file_size > current_app.config['MAX_CONTENT_LENGTH']:
        return {'valid': False, 'error': 'El archivo es demasiado grande'}
    
    return {'valid': True, 'size': file_size}

# .env template
"""
# Database Configuration
MYSQL_HOST=localhost
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password
MYSQL_DB=recruitment_system

# AWS S3 Configuration
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_S3_BUCKET=your-s3-bucket-name
AWS_S3_REGION=us-east-1

# Security
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
"""

# README.md
"""
# Sistema de Gestión de Vacantes y Candidatos

## Descripción
Sistema completo para la gestión de procesos de reclutamiento, desarrollado con Flask, SQLAlchemy, MySQL y AWS S3.

## Características principales
- CRUD completo para todas las entidades
- Gestión de roles y permisos
- Subida de archivos a AWS S3
- Relaciones muchos-a-muchos entre candidatos y vacantes
- API RESTful documentada
- Autenticación JWT

## Tecnologías utilizadas
- **Backend**: Flask (Python)
- **Base de datos**: MySQL
- **ORM**: SQLAlchemy
- **Almacenamiento**: AWS S3
- **Autenticación**: JWT + Flask-Login
- **Migraciones**: Flask-Migrate

## Instalación

1. Clonar el repositorio
2. Crear entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configurar variables de entorno:
   - Copiar `.env.template` a `.env`
   - Completar con tus credenciales

5. Inicializar base de datos:
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. Ejecutar aplicación:
   ```bash
   python app.py
   ```

## Estructura del proyecto
```
/app
  /models/          # Modelos de SQLAlchemy
  /routes/          # Blueprints con endpoints
  /services/        # Servicios (S3, Auth)
  /utils/           # Utilidades
  config.py         # Configuración
  app.py           # Aplicación principal
requirements.txt
README.md
.env.template
```

## Endpoints principales

### Autenticación
- `POST /api/auth/login` - Iniciar sesión
- `POST /api/auth/register` - Registrar usuario

### Usuarios
- `GET /api/usuarios` - Listar usuarios
- `POST /api/usuarios` - Crear usuario
- `GET /api/usuarios/<id>` - Obtener usuario
- `PUT /api/usuarios/<id>` - Actualizar usuario
- `DELETE /api/usuarios/<id>` - Eliminar usuario

### Vacantes
- `GET /api/vacantes` - Listar vacantes
- `POST /api/vacantes` - Crear vacante
- `GET /api/vacantes/<id>` - Obtener vacante
- `PUT /api/vacantes/<id>` - Actualizar vacante
- `DELETE /api/vacantes/<id>` - Eliminar vacante

### Candidatos
- `GET /api/candidatos` - Listar candidatos
- `POST /api/candidatos` - Crear candidato
- `GET /api/candidatos/<id>` - Obtener candidato
- `PUT /api/candidatos/<id>` - Actualizar candidato
- `DELETE /api/candidatos/<id>` - Eliminar candidato

### Documentos
- `POST /api/documentos/upload` - Subir archivo
- `GET /api/documentos/<id>` - Obtener documento
- `DELETE /api/documentos/<id>` - Eliminar documento

### Entrevistas
- `GET /api/entrevistas` - Listar entrevistas
- `POST /api/entrevistas` - Crear entrevista
- `GET /api/entrevistas/<id>` - Obtener entrevista
- `PUT /api/entrevistas/<id>` - Actualizar entrevista
- `DELETE /api/entrevistas/<id>` - Eliminar entrevista

### Candidatos-Posiciones
- `GET /api/candidatos-posiciones` - Listar asignaciones
- `POST /api/candidatos-posiciones` - Asignar candidato a vacante
- `PUT /api/candidatos-posiciones/<id>` - Actualizar estado
- `DELETE /api/candidatos-posiciones/<id>` - Eliminar asignación

## Roles de usuario
- **Ejecutivo**: Puede crear vacantes y ver reportes
- **Reclutador**: Gestiona candidatos y entrevistas
- **Reclutador Líder**: Supervisión general

## Base de datos
El sistema utiliza las siguientes tablas:
- usuarios
- vacantes
- candidatos
- documentos
- entrevistas
- candidatos_posiciones (tabla intermedia)
"""

# routes/usuario_routes.py
from flask import Blueprint, request, jsonify
from services.auth_service import token_required, role_required
from models import Usuario, db

usuario_bp = Blueprint('usuario', __name__)

@usuario_bp.route('', methods=['GET'])
@token_required
def get_usuarios(current_user):
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        usuarios = Usuario.query.filter_by(activo=True).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'usuarios': [usuario.to_dict() for usuario in usuarios.items],
            'total': usuarios.total,
            'pages': usuarios.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error obteniendo usuarios: {str(e)}'}), 500

@usuario_bp.route('/<int:usuario_id>', methods=['GET'])
@token_required
def get_usuario(current_user, usuario_id):
    try:
        usuario = Usuario.query.get_or_404(usuario_id)
        return jsonify(usuario.to_dict()), 200
    except Exception as e:
        return jsonify({'message': f'Error obteniendo usuario: {str(e)}'}), 500

@usuario_bp.route('', methods=['POST'])
@role_required('ejecutivo', 'reclutador_lider')
def create_usuario(current_user):
    try:
        data = request.get_json()
        
        required_fields = ['nombre', 'email', 'password', 'rol']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'message': f'{field} es requerido'}), 400
        
        # Verificar email único
        if Usuario.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'El email ya existe'}), 400
        
        nuevo_usuario = Usuario(
            nombre=data['nombre'],
            email=data['email'],
            rol=data['rol']
        )
        nuevo_usuario.set_password(data['password'])
        
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        return jsonify({
            'message': 'Usuario creado exitosamente',
            'usuario': nuevo_usuario.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error creando usuario: {str(e)}'}), 500

@usuario_bp.route('/<int:usuario_id>', methods=['PUT'])
@role_required('ejecutivo', 'reclutador_lider')
def update_usuario(current_user, usuario_id):
    try:
        usuario = Usuario.query.get_or_404(usuario_id)
        data = request.get_json()
        
        # Actualizar campos permitidos
        if 'nombre' in data:
            usuario.nombre = data['nombre']
        if 'email' in data:
            # Verificar que el email no esté en uso por otro usuario
            existing = Usuario.query.filter_by(email=data['email']).first()
            if existing and existing.id != usuario_id:
                return jsonify({'message': 'El email ya está en uso'}), 400
            usuario.email = data['email']
        if 'rol' in data:
            usuario.rol = data['rol']
        if 'activo' in data:
            usuario.activo = data['activo']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Usuario actualizado exitosamente',
            'usuario': usuario.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error actualizando usuario: {str(e)}'}), 500

@usuario_bp.route('/<int:usuario_id>', methods=['DELETE'])
@role_required('ejecutivo', 'reclutador_lider')
def delete_usuario(current_user, usuario_id):
    try:
        usuario = Usuario.query.get_or_404(usuario_id)
        
        # Soft delete
        usuario.activo = False
        db.session.commit()
        
        return jsonify({'message': 'Usuario desactivado exitosamente'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error eliminando usuario: {str(e)}'}), 500

# routes/vacante_routes.py
from flask import Blueprint, request, jsonify
from services.auth_service import token_required, role_required
from models import Vacante, Usuario, db
from datetime import datetime

vacante_bp = Blueprint('vacante', __name__)

@vacante_bp.route('', methods=['GET'])
@token_required
def get_vacantes(current_user):
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        estado = request.args.get('estado')
        
        query = Vacante.query
        
        # Filtrar por estado si se proporciona
        if estado:
            query = query.filter_by(estado=estado)
        
        # Filtrar según rol del usuario
        if current_user.rol == 'reclutador':
            query = query.filter_by(reclutador_id=current_user.id)
        
        vacantes = query.order_by(Vacante.fecha_creacion.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'vacantes': [vacante.to_dict() for vacante in vacantes.items],
            'total': vacantes.total,
            'pages': vacantes.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error obteniendo vacantes: {str(e)}'}), 500

@vacante_bp.route('/<int:vacante_id>', methods=['GET'])
@token_required
def get_vacante(current_user, vacante_id):
    try:
        vacante = Vacante.query.get_or_404(vacante_id)
        
        # Verificar permisos
        if (current_user.rol == 'reclutador' and 
            vacante.reclutador_id != current_user.id):
            return jsonify({'message': 'Sin permisos para ver esta vacante'}), 403
        
        return jsonify(vacante.to_dict()), 200
        
    except Exception as e:
        return jsonify({'message': f'Error obteniendo vacante: {str(e)}'}), 500

@vacante_bp.route('', methods=['POST'])
@role_required('ejecutivo', 'reclutador_lider')
def create_vacante(current_user):
    try:
        data = request.get_json()
        
        required_fields = ['nombre', 'reclutador_id']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'message': f'{field} es requerido'}), 400
        
        # Verificar que el reclutador existe
        reclutador = Usuario.query.get(data['reclutador_id'])
        if not reclutador or reclutador.rol not in ['reclutador', 'reclutador_lider']:
            return jsonify({'message': 'Reclutador inválido'}), 400
        
        nueva_vacante = Vacante(
            nombre=data['nombre'],
            descripcion=data.get('descripcion'),
            ejecutivo_id=current_user.id,
            reclutador_id=data['reclutador_id'],
            reclutador_lider_id=data.get('reclutador_lider_id'),
            vacantes=data.get('vacantes', 1),
            prioridad=data.get('prioridad', 'media'),
            salario_min=data.get('salario_min'),
            salario_max=data.get('salario_max'),
            ubicacion=data.get('ubicacion'),
            modalidad=data.get('modalidad'),
            fecha_limite=datetime.fromisoformat(data['fecha_limite']) if data.get('fecha_limite') else None,
            comentarios=data.get('comentarios')
        )
        
        db.session.add(nueva_vacante)
        db.session.commit()
        
        return jsonify({
            'message': 'Vacante creada exitosamente',
            'vacante': nueva_vacante.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error creando vacante: {str(e)}'}), 500

@vacante_bp.route('/<int:vacante_id>', methods=['PUT'])
@token_required
def update_vacante(current_user, vacante_id):
    try:
        vacante = Vacante.query.get_or_404(vacante_id)
        
        # Verificar permisos
        if (current_user.rol not in ['ejecutivo', 'reclutador_lider'] and 
            vacante.reclutador_id != current_user.id):
            return jsonify({'message': 'Sin permisos para modificar esta vacante'}), 403
        
        data = request.get_json()
        
        # Actualizar campos permitidos
        campos_actualizables = [
            'nombre', 'descripcion', 'estado', 'prioridad', 'vacantes',
            'salario_min', 'salario_max', 'ubicacion', 'modalidad', 'comentarios'
        ]
        
        for campo in campos_actualizables:
            if campo in data:
                setattr(vacante, campo, data[campo])
        
        if 'fecha_limite' in data and data['fecha_limite']:
            vacante.fecha_limite = datetime.fromisoformat(data['fecha_limite'])
        
        db.session.commit()
        
        return jsonify({
            'message': 'Vacante actualizada exitosamente',
            'vacante': vacante.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error actualizando vacante: {str(e)}'}), 500

@vacante_bp.route('/<int:vacante_id>', methods=['DELETE'])
@role_required('ejecutivo', 'reclutador_lider')
def delete_vacante(current_user, vacante_id):
    try:
        vacante = Vacante.query.get_or_404(vacante_id)
        
        # Cambiar estado a cancelada en lugar de eliminar físicamente
        vacante.estado = 'cancelada'
        db.session.commit()
        
        return jsonify({'message': 'Vacante cancelada exitosamente'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error eliminando vacante: {str(e)}'}), 500

# routes/candidato_routes.py
from flask import Blueprint, request, jsonify
from services.auth_service import token_required, role_required
from models import Candidato, db

candidato_bp = Blueprint('candidato', __name__)

@candidato_bp.route('', methods=['GET'])
@token_required
def get_candidatos(current_user):
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        estado = request.args.get('estado')
        search = request.args.get('search')
        
        query = Candidato.query
        
        # Filtrar por estado
        if estado:
            query = query.filter_by(estado=estado)
        
        # Búsqueda por nombre o email
        if search:
            query = query.filter(
                (Candidato.nombre.contains(search)) |
                (Candidato.email.contains(search))
            )
        
        # Filtrar según rol del usuario
        if current_user.rol == 'reclutador':
            query = query.filter_by(reclutador_id=current_user.id)
        
        candidatos = query.order_by(Candidato.fecha_creacion.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'candidatos': [candidato.to_dict() for candidato in candidatos.items],
            'total': candidatos.total,
            'pages': candidatos.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error obteniendo candidatos: {str(e)}'}), 500

@candidato_bp.route('/<int:candidato_id>', methods=['GET'])
@token_required
def get_candidato(current_user, candidato_id):
    try:
        candidato = Candidato.query.get_or_404(candidato_id)
        
        # Verificar permisos
        if (current_user.rol == 'reclutador' and 
            candidato.reclutador_id != current_user.id):
            return jsonify({'message': 'Sin permisos para ver este candidato'}), 403
        
        # Incluir información adicional
        candidato_dict = candidato.to_dict()
        candidato_dict['documentos'] = [doc.to_dict() for doc in candidato.documentos]
        candidato_dict['entrevistas'] = [entrevista.to_dict() for entrevista in candidato.entrevistas]
        candidato_dict['posiciones'] = []
        
        for pos in candidato.candidatos_posiciones:
            candidato_dict['posiciones'].append({
                'id': pos.id,
                'vacante_id': pos.vacante_id,
                'vacante_nombre': pos.vacante.nombre,
                'status': pos.status,
                'nota': pos.nota,
                'fecha_asignacion': pos.fecha_asignacion.isoformat() if pos.fecha_asignacion else None
            })
        
        return jsonify(candidato_dict), 200
        
    except Exception as e:
        return jsonify({'message': f'Error obteniendo candidato: {str(e)}'}), 500

@candidato_bp.route('', methods=['POST'])
@role_required('reclutador', 'reclutador_lider')
def create_candidato(current_user):
    try:
        data = request.get_json()
        
        required_fields = ['nombre', 'email']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'message': f'{field} es requerido'}), 400
        
        # Verificar email único
        if Candidato.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'El email ya existe'}), 400
        
        nuevo_candidato = Candidato(
            nombre=data['nombre'],
            email=data['email'],
            telefono=data.get('telefono'),
            reclutador_id=current_user.id,
            salario_esperado=data.get('salario_esperado'),
            experiencia_anos=data.get('experiencia_anos'),
            ubicacion=data.get('ubicacion'),
            disponibilidad=data.get('disponibilidad'),
            nivel_ingles=data.get('nivel_ingles'),
            linkedin_url=data.get('linkedin_url'),
            comentarios_finales=data.get('comentarios_finales')
        )
        
        db.session.add(nuevo_candidato)
        db.session.commit()
        
        return jsonify({
            'message': 'Candidato creado exitosamente',
            'candidato': nuevo_candidato.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error creando candidato: {str(e)}'}), 500

@candidato_bp.route('/<int:candidato_id>', methods=['PUT'])
@token_required
def update_candidato(current_user, candidato_id):
    try:
        candidato = Candidato.query.get_or_404(candidato_id)
        
        # Verificar permisos
        if (current_user.rol == 'reclutador' and 
            candidato.reclutador_id != current_user.id):
            return jsonify({'message': 'Sin permisos para modificar este candidato'}), 403
        
        data = request.get_json()
        
        # Campos actualizables
        campos_actualizables = [
            'nombre', 'email', 'telefono', 'estado', 'comentarios_finales',
            'salario_esperado', 'experiencia_anos', 'ubicacion', 'disponibilidad',
            'nivel_ingles', 'linkedin_url'
        ]
        
        for campo in campos_actualizables:
            if campo in data:
                # Verificar email único si se está actualizando
                if campo == 'email':
                    existing = Candidato.query.filter_by(email=data[campo]).first()
                    if existing and existing.id != candidato_id:
                        return jsonify({'message': 'El email ya está en uso'}), 400
                
                setattr(candidato, campo, data[campo])
        
        db.session.commit()
        
        return jsonify({
            'message': 'Candidato actualizado exitosamente',
            'candidato': candidato.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error actualizando candidato: {str(e)}'}), 500

@candidato_bp.route('/<int:candidato_id>', methods=['DELETE'])
@role_required('reclutador_lider')
def delete_candidato(current_user, candidato_id):
    try:
        candidato = Candidato.query.get_or_404(candidato_id)
        
        # Cambiar estado a inactivo en lugar de eliminar
        candidato.estado = 'inactivo'
        db.session.commit()
        
        return jsonify({'message': 'Candidato desactivado exitosamente'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error eliminando candidato: {str(e)}'}), 500

# routes/documento_routes.py
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from services.auth_service import token_required
from services.s3_service import S3Service
from models import Documento, Candidato, db
from utils.file_utils import validate_file_upload

documento_bp = Blueprint('documento', __name__)

@documento_bp.route('/upload', methods=['POST'])
@token_required
def upload_documento(current_user):
    try:
        # Verificar que se envió un archivo
        if 'file' not in request.files:
            return jsonify({'message': 'No se encontró archivo'}), 400
        
        file = request.files['file']
        candidato_id = request.form.get('candidato_id')
        tipo = request.form.get('tipo', 'otro')
        
        if not candidato_id:
            return jsonify({'message': 'candidato_id es requerido'}), 400
        
        # Verificar que el candidato existe
        candidato = Candidato.query.get(candidato_id)
        if not candidato:
            return jsonify({'message': 'Candidato no encontrado'}), 404
        
        # Verificar permisos
        if (current_user.rol == 'reclutador' and 
            candidato.reclutador_id != current_user.id):
            return jsonify({'message': 'Sin permisos para subir archivos a este candidato'}), 403
        
        # Validar archivo
        validation = validate_file_upload(file)
        if not validation['valid']:
            return jsonify({'message': validation['error']}), 400
        
        # Subir a S3
        s3_service = S3Service()
        upload_result = s3_service.upload_file(
            file_obj=file,
            file_name=secure_filename(file.filename),
            content_type=file.content_type,
            folder=f'candidatos/{candidato_id}'
        )
        
        if not upload_result['success']:
            return jsonify({'message': upload_result['error']}), 500
        
        # Guardar en base de datos
        nuevo_documento = Documento(
            nombre_original=file.filename,
            url_s3=upload_result['url'],
            key_s3=upload_result['key'],
            tipo=tipo,
            candidato_id=candidato_id,
            tamaño_bytes=validation['size'],
            content_type=file.content_type
        )
        
        db.session.add(nuevo_documento)
        
        # Si es un CV, actualizar el candidato
        if tipo == 'cv':
            candidato.cv_url = upload_result['url']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Archivo subido exitosamente',
            'documento': nuevo_documento.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error subiendo archivo: {str(e)}'}), 500

@documento_bp.route('/<int:documento_id>', methods=['GET'])
@token_required
def get_documento(current_user, documento_id):
    try:
        documento = Documento.query.get_or_404(documento_id)
        
        # Verificar permisos
        if (current_user.rol == 'reclutador' and 
            documento.candidato_rel.reclutador_id != current_user.id):
            return jsonify({'message': 'Sin permisos para ver este documento'}), 403
        
        # Generar URL firmada para descarga
        s3_service = S3Service()
        url_result = s3_service.generate_presigned_url(documento.key_s3)
        
        if not url_result['success']:
            return jsonify({'message': url_result['error']}), 500
        
        documento_dict = documento.to_dict()
        documento_dict['download_url'] = url_result['url']
        
        return jsonify(documento_dict), 200
        
    except Exception as e:
        return jsonify({'message': f'Error obteniendo documento: {str(e)}'}), 500

@documento_bp.route('/<int:documento_id>', methods=['DELETE'])
@token_required
def delete_documento(current_user, documento_id):
    try:
        documento = Documento.query.get_or_404(documento_id)
        
        # Verificar permisos
        if (current_user.rol == 'reclutador' and 
            documento.candidato_rel.reclutador_id != current_user.id):
            return jsonify({'message': 'Sin permisos para eliminar este documento'}), 403
        
        # Eliminar de S3
        s3_service = S3Service()
        s3_service.delete_file(documento.key_s3)
        
        # Eliminar de base de datos
        db.session.delete(documento)
        db.session.commit()
        
        return jsonify({'message': 'Documento eliminado exitosamente'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error eliminando documento: {str(e)}'}), 500

# routes/entrevista_routes.py
from flask import Blueprint, request, jsonify
from services.auth_service import token_required
from models import Entrevista, Candidato, Vacante, db
from datetime import datetime

entrevista_bp = Blueprint('entrevista', __name__)

@entrevista_bp.route('', methods=['GET'])
@token_required
def get_entrevistas(current_user):
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        fecha_desde = request.args.get('fecha_desde')
        fecha_hasta = request.args.get('fecha_hasta')
        
        query = Entrevista.query
        
        # Filtrar por fechas si se proporcionan
        if fecha_desde:
            query = query.filter(Entrevista.fecha >= datetime.fromisoformat(fecha_desde))
        if fecha_hasta:
            query = query.filter(Entrevista.fecha <= datetime.fromisoformat(fecha_hasta))
        
        # Filtrar según rol del usuario
        if current_user.rol == 'reclutador':
            # Solo entrevistas de candidatos asignados al reclutador
            query = query.join(Candidato).filter(Candidato.reclutador_id == current_user.id)
        
        entrevistas = query.order_by(Entrevista.fecha.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'entrevistas': [entrevista.to_dict() for entrevista in entrevistas.items],
            'total': entrevistas.total,
            'pages': entrevistas.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error obteniendo entrevistas: {str(e)}'}), 500

@entrevista_bp.route('/<int:entrevista_id>', methods=['GET'])
@token_required
def get_entrevista(current_user, entrevista_id):
    try:
        entrevista = Entrevista.query.get_or_404(entrevista_id)
        
        # Verificar permisos
        if (current_user.rol == 'reclutador' and 
            entrevista.candidato_rel.reclutador_id != current_user.id):
            return jsonify({'message': 'Sin permisos para ver esta entrevista'}), 403
        
        return jsonify(entrevista.to_dict()), 200
        
    except Exception as e:
        return jsonify({'message': f'Error obteniendo entrevista: {str(e)}'}), 500

@entrevista_bp.route('', methods=['POST'])
@token_required
def create_entrevista(current_user):
    try:
        data = request.get_json()
        
        required_fields = ['fecha', 'tipo', 'candidato_id', 'vacante_id']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'message': f'{field} es requerido'}), 400
        
        # Verificar que candidato y vacante existen
        candidato = Candidato.query.get(data['candidato_id'])
        vacante = Vacante.query.get(data['vacante_id'])
        
        if not candidato:
            return jsonify({'message': 'Candidato no encontrado'}), 404
        if not vacante:
            return jsonify({'message': 'Vacante no encontrada'}), 404
        
        # Verificar permisos
        if (current_user.rol == 'reclutador' and 
            candidato.reclutador_id != current_user.id):
            return jsonify({'message': 'Sin permisos para programar entrevista a este candidato'}), 403
        
        nueva_entrevista = Entrevista(
            fecha=datetime.fromisoformat(data['fecha']),
            tipo=data['tipo'],
            candidato_id=data['candidato_id'],
            vacante_id=data['vacante_id'],
            entrevistador_id=current_user.id,
            comentarios=data.get('comentarios'),
            duracion_minutos=data.get('duracion_minutos'),
            ubicacion=data.get('ubicacion')
        )
        
        db.session.add(nueva_entrevista)
        db.session.commit()
        
        return jsonify({
            'message': 'Entrevista creada exitosamente',
            'entrevista': nueva_entrevista.to_dict()
        }), 201
        
    except ValueError as e:
        return jsonify({'message': 'Formato de fecha inválido'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error creando entrevista: {str(e)}'}), 500

@entrevista_bp.route('/<int:entrevista_id>', methods=['PUT'])
@token_required
def update_entrevista(current_user, entrevista_id):
    try:
        entrevista = Entrevista.query.get_or_404(entrevista_id)
        
        # Verificar permisos
        if (current_user.rol == 'reclutador' and 
            entrevista.candidato_rel.reclutador_id != current_user.id):
            return jsonify({'message': 'Sin permisos para modificar esta entrevista'}), 403
        
        data = request.get_json()
        
        # Campos actualizables
        if 'fecha' in data:
            entrevista.fecha = datetime.fromisoformat(data['fecha'])
        if 'tipo' in data:
            entrevista.tipo = data['tipo']
        if 'resultado' in data:
            entrevista.resultado = data['resultado']
        if 'comentarios' in data:
            entrevista.comentarios = data['comentarios']
        if 'puntuacion' in data:
            entrevista.puntuacion = data['puntuacion']
        if 'duracion_minutos' in data:
            entrevista.duracion_minutos = data['duracion_minutos']
        if 'ubicacion' in data:
            entrevista.ubicacion = data['ubicacion']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Entrevista actualizada exitosamente',
            'entrevista': entrevista.to_dict()
        }), 200
        
    except ValueError as e:
        return jsonify({'message': 'Formato de fecha inválido'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error actualizando entrevista: {str(e)}'}), 500

@entrevista_bp.route('/<int:entrevista_id>', methods=['DELETE'])
@token_required
def delete_entrevista(current_user, entrevista_id):
    try:
        entrevista = Entrevista.query.get_or_404(entrevista_id)
        
        # Verificar permisos
        if (current_user.rol == 'reclutador' and 
            entrevista.candidato_rel.reclutador_id != current_user.id):
            return jsonify({'message': 'Sin permisos para eliminar esta entrevista'}), 403
        
        db.session.delete(entrevista)
        db.session.commit()
        
        return jsonify({'message': 'Entrevista eliminada exitosamente'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error eliminando entrevista: {str(e)}'}), 500

# routes/candidatos_posiciones_routes.py
from flask import Blueprint, request, jsonify
from services.auth_service import token_required
from models import CandidatosPositions, Candidato, Vacante, db

candidatos_posiciones_bp = Blueprint('candidatos_posiciones', __name__)

@candidatos_posiciones_bp.route('', methods=['GET'])
@token_required
def get_candidatos_posiciones(current_user):
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        candidato_id = request.args.get('candidato_id')
        vacante_id = request.args.get('vacante_id')
        status = request.args.get('status')
        
        query = CandidatosPositions.query
        
        # Filtros
        if candidato_id:
            query = query.filter_by(candidato_id=candidato_id)
        if vacante_id:
            query = query.filter_by(vacante_id=vacante_id)
        if status:
            query = query.filter_by(status=status)
        
        # Filtrar según rol del usuario
        if current_user.rol == 'reclutador':
            query = query.join(Candidato).filter(Candidato.reclutador_id == current_user.id)
        
        asignaciones = query.order_by(CandidatosPositions.fecha_asignacion.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        result = []
        for asignacion in asignaciones.items:
            asignacion_dict = {
                'id': asignacion.id,
                'candidato_id': asignacion.candidato_id,
                'vacante_id': asignacion.vacante_id,
                'status': asignacion.status,
                'nota': asignacion.nota,
                'fecha_asignacion': asignacion.fecha_asignacion.isoformat() if asignacion.fecha_asignacion else None,
                'fecha_actualizacion': asignacion.fecha_actualizacion.isoformat() if asignacion.fecha_actualizacion else None,
                'candidato_nombre': asignacion.candidato.nombre,
                'vacante_nombre': asignacion.vacante.nombre
            }
            result.append(asignacion_dict)
        
        return jsonify({
            'asignaciones': result,
            'total': asignaciones.total,
            'pages': asignaciones.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error obteniendo asignaciones: {str(e)}'}), 500

@candidatos_posiciones_bp.route('', methods=['POST'])
@token_required
def create_candidato_posicion(current_user):
    try:
        data = request.get_json()
        
        required_fields = ['candidato_id', 'vacante_id']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'message': f'{field} es requerido'}), 400
        
        # Verificar que candidato y vacante existen
        candidato = Candidato.query.get(data['candidato_id'])
        vacante = Vacante.query.get(data['vacante_id'])
        
        if not candidato:
            return jsonify({'message': 'Candidato no encontrado'}), 404
        if not vacante:
            return jsonify({'message': 'Vacante no encontrada'}), 404
        
        # Verificar permisos
        if (current_user.rol == 'reclutador' and 
            candidato.reclutador_id != current_user.id):
            return jsonify({'message': 'Sin permisos para asignar este candidato'}), 403
        
        # Verificar que no existe ya la asignación
        existing = CandidatosPositions.query.filter_by(
            candidato_id=data['candidato_id'],
            vacante_id=data['vacante_id']
        ).first()
        
        if existing:
            return jsonify({'message': 'El candidato ya está asignado a esta vacante'}), 400
        
        nueva_asignacion = CandidatosPositions(
            candidato_id=data['candidato_id'],
            vacante_id=data['vacante_id'],
            status=data.get('status', 'postulado'),
            nota=data.get('nota')
        )
        
        db.session.add(nueva_asignacion)
        db.session.commit()
        
        return jsonify({
            'message': 'Candidato asignado a vacante exitosamente',
            'asignacion': {
                'id': nueva_asignacion.id,
                'candidato_id': nueva_asignacion.candidato_id,
                'vacante_id': nueva_asignacion.vacante_id,
                'status': nueva_asignacion.status,
                'nota': nueva_asignacion.nota,
                'fecha_asignacion': nueva_asignacion.fecha_asignacion.isoformat() if nueva_asignacion.fecha_asignacion else None,
                'candidato_nombre': candidato.nombre,
                'vacante_nombre': vacante.nombre
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error creando asignación: {str(e)}'}), 500

@candidatos_posiciones_bp.route('/<int:asignacion_id>', methods=['PUT'])
@token_required
def update_candidato_posicion(current_user, asignacion_id):
    try:
        asignacion = CandidatosPositions.query.get_or_404(asignacion_id)
        
        # Verificar permisos
        if (current_user.rol == 'reclutador' and 
            asignacion.candidato.reclutador_id != current_user.id):
            return jsonify({'message': 'Sin permisos para modificar esta asignación'}), 403
        
        data = request.get_json()
        
        if 'status' in data:
            asignacion.status = data['status']
        if 'nota' in data:
            asignacion.nota = data['nota']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Asignación actualizada exitosamente',
            'asignacion': {
                'id': asignacion.id,
                'candidato_id': asignacion.candidato_id,
                'vacante_id': asignacion.vacante_id,
                'status': asignacion.status,
                'nota': asignacion.nota,
                'fecha_actualizacion': asignacion.fecha_actualizacion.isoformat() if asignacion.fecha_actualizacion else None,
                'candidato_nombre': asignacion.candidato.nombre,
                'vacante_nombre': asignacion.vacante.nombre
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error actualizando asignación: {str(e)}'}), 500

@candidatos_posiciones_bp.route('/<int:asignacion_id>', methods=['DELETE'])
@token_required
def delete_candidato_posicion(current_user, asignacion_id):
    try:
        asignacion = CandidatosPositions.query.get_or_404(asignacion_id)
        
        # Verificar permisos
        if (current_user.rol == 'reclutador' and 
            asignacion.candidato.reclutador_id != current_user.id):
            return jsonify({'message': 'Sin permisos para eliminar esta asignación'}), 403
        
        db.session.delete(asignacion)
        db.session.commit()
        
        return jsonify({'message': 'Asignación eliminada exitosamente'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error eliminando asignación: {str(e)}'}), 500

# routes/reports_routes.py (Rutas adicionales para reportes)
from flask import Blueprint, request, jsonify
from services.auth_service import token_required, role_required
from models import Vacante, Candidato, Entrevista, CandidatosPositions, db
from sqlalchemy import func, desc

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/dashboard', methods=['GET'])
@token_required
def get_dashboard_stats(current_user):
    try:
        stats = {}
        
        # Estadísticas básicas
        if current_user.rol == 'reclutador':
            # Solo datos del reclutador
            stats['vacantes_activas'] = Vacante.query.filter_by(
                reclutador_id=current_user.id, 
                estado='abierta'
            ).count()
            
            stats['candidatos_totales'] = Candidato.query.filter_by(
                reclutador_id=current_user.id,
                estado='activo'
            ).count()
            
            stats['entrevistas_pendientes'] = Entrevista.query.join(Candidato).filter(
                Candidato.reclutador_id == current_user.id,
                Entrevista.resultado == 'pendiente'
            ).count()
            
        else:
            # Datos generales para ejecutivos y líderes
            stats['vacantes_activas'] = Vacante.query.filter_by(estado='abierta').count()
            stats['candidatos_totales'] = Candidato.query.filter_by(estado='activo').count()
            stats['entrevistas_pendientes'] = Entrevista.query.filter_by(resultado='pendiente').count()
        
        # Estadísticas por estado de candidatos
        candidatos_por_estado = db.session.query(
            CandidatosPositions.status,
            func.count(CandidatosPositions.id).label('count')
        ).group_by(CandidatosPositions.status).all()
        
        stats['candidatos_por_estado'] = {estado: count for estado, count in candidatos_por_estado}
        
        # Vacantes con más candidatos
        vacantes_populares = db.session.query(
            Vacante.nombre,
            func.count(CandidatosPositions.id).label('candidatos')
        ).join(CandidatosPositions).group_by(Vacante.id, Vacante.nombre)\
         .order_by(desc('candidatos')).limit(5).all()
        
        stats['vacantes_populares'] = [
            {'nombre': nombre, 'candidatos': candidatos} 
            for nombre, candidatos in vacantes_populares
        ]
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({'message': f'Error obteniendo estadísticas: {str(e)}'}), 500

@reports_bp.route('/vacante/<int:vacante_id>/reporte', methods=['GET'])
@role_required('ejecutivo', 'reclutador_lider')
def get_vacante_report(current_user, vacante_id):
    try:
        vacante = Vacante.query.get_or_404(vacante_id)
        
        # Información básica de la vacante
        reporte = {
            'vacante': vacante.to_dict(),
            'resumen': {}
        }
        
        # Candidatos por estado
        candidatos_por_estado = db.session.query(
            CandidatosPositions.status,
            func.count(CandidatosPositions.id).label('count')
        ).filter_by(vacante_id=vacante_id).group_by(CandidatosPositions.status).all()
        
        reporte['resumen']['candidatos_por_estado'] = {
            estado: count for estado, count in candidatos_por_estado
        }
        
        # Entrevistas realizadas
        entrevistas_por_resultado = db.session.query(
            Entrevista.resultado,
            func.count(Entrevista.id).label('count')
        ).filter_by(vacante_id=vacante_id).group_by(Entrevista.resultado).all()
        
        reporte['resumen']['entrevistas_por_resultado'] = {
            resultado: count for resultado, count in entrevistas_por_resultado
        }
        
        # Lista de candidatos con detalles
        candidatos_detalle = db.session.query(
            Candidato, CandidatosPositions
        ).join(CandidatosPositions).filter(
            CandidatosPositions.vacante_id == vacante_id
        ).all()
        
        reporte['candidatos'] = []
        for candidato, asignacion in candidatos_detalle:
            candidato_dict = candidato.to_dict()
            candidato_dict['status_vacante'] = asignacion.status
            candidato_dict['nota_vacante'] = asignacion.nota
            candidato_dict['fecha_asignacion'] = asignacion.fecha_asignacion.isoformat() if asignacion.fecha_asignacion else None
            
            # Agregar entrevistas para esta vacante
            candidato_dict['entrevistas'] = [
                entrevista.to_dict() for entrevista in candidato.entrevistas
                if entrevista.vacante_id == vacante_id
            ]
            
            reporte['candidatos'].append(candidato_dict)
        
        return jsonify(reporte), 200
        
    except Exception as e:
        return jsonify({'message': f'Error generando reporte: {str(e)}'}), 500

# Database migration script (migrations/create_initial_tables.py)
"""
Script para crear las tablas iniciales de la base de datos
Ejecutar con: flask db init && flask db migrate -m "Initial migration" && flask db upgrade
"""

def create_initial_data():
    """Crear datos iniciales para testing"""
    from models import Usuario, db
    from werkzeug.security import generate_password_hash
    
    try:
        # Crear usuario administrador inicial
        admin_user = Usuario(
            nombre='Administrador',
            email='admin@empresa.com',
            rol='ejecutivo',
            activo=True
        )
        admin_user.set_password('admin123')
        
        # Crear reclutador de prueba
        recruiter_user = Usuario(
            nombre='Reclutador Test',
            email='reclutador@empresa.com',
            rol='reclutador',
            activo=True
        )
        recruiter_user.set_password('reclutador123')
        
        db.session.add(admin_user)
        db.session.add(recruiter_user)
        db.session.commit()
        
        print("Usuarios iniciales creados exitosamente")
        print("Admin: admin@empresa.com / admin123")
        print("Reclutador: reclutador@empresa.com / reclutador123")
        
    except Exception as e:
        db.session.rollback()
        print(f"Error creando datos iniciales: {str(e)}")

# Postman Collection Example (postman_collection.json)
"""
{
  "info": {
    "name": "Sistema de Reclutamiento API",
    "description": "Collection para probar todos los endpoints del sistema",
    "version": "1.0.0"
  },
  "auth": {
    "type": "bearer",
    "bearer": [
      {
        "key": "token",
        "value": "{{jwt_token}}",
        "type": "string"
      }
    ]
  },
  "variable": [
    {
      "key": "base_url",
      "value": "http://localhost:5000/api"
    },
    {
      "key": "jwt_token",
      "value": ""
    }
  ],
  "item": [
    {
      "name": "Auth",
      "item": [
        {
          "name": "Login",
          "request": {
            "method": "POST",
            "header": [],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"email\": \"admin@empresa.com\",\n  \"password\": \"admin123\"\n}",
              "options": {
                "raw": {
                  "language": "json"
                }
              }
            },
            "url": {
              "raw": "{{base_url}}/auth/login",
              "host": ["{{base_url}}"],
              "path": ["auth", "login"]
            }
          }
        }
      ]
    }
  ]
}
"""

# Docker Configuration (docker-compose.yml)
"""
version: '3.8'

services:
  mysql:
    image: mysql:8.0
    container_name: recruitment_mysql
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: recruitment_system
      MYSQL_USER: recruitment_user
      MYSQL_PASSWORD: recruitment_pass
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
    networks:
      - recruitment_network

  app:
    build: .
    container_name: recruitment_app
    environment:
      MYSQL_HOST: mysql
      MYSQL_USER: recruitment_user
      MYSQL_PASSWORD: recruitment_pass
      MYSQL_DB: recruitment_system
    ports:
      - "5000:5000"
    depends_on:
      - mysql
    volumes:
      - .:/app
    networks:
      - recruitment_network

volumes:
  mysql_data:

networks:
  recruitment_network:
    driver: bridge
"""

# Dockerfile
"""
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
"""

# Testing script (test_api.py)
"""
Script básico para probar los endpoints principales
"""

import requests
import json

BASE_URL = 'http://localhost:5000/api'
headers = {'Content-Type': 'application/json'}

def test_login():
    """Test login endpoint"""
    login_data = {
        'email': 'admin@empresa.com',
        'password': 'admin123'
    }
    
    response = requests.post(f'{BASE_URL}/auth/login', 
                           json=login_data, 
                           headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        token = data['access_token']
        print(f"Login exitoso. Token: {token[:50]}...")
        return token
    else:
        print(f"Error en login: {response.text}")
        return None

def test_create_candidato(token):
    """Test crear candidato"""
    auth_headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    
    candidato_data = {
        'nombre': 'Juan Pérez',
        'email': 'juan.perez@email.com',
        'telefono': '+52 55 1234 5678',
        'experiencia_anos': 5,
        'salario_esperado': 50000.00,
        'ubicacion': 'Ciudad de México',
        'disponibilidad': 'inmediata',
        'nivel_ingles': 'intermedio'
    }
    
    response = requests.post(f'{BASE_URL}/candidatos',
                           json=candidato_data,
                           headers=auth_headers)
    
    if response.status_code == 201:
        print("Candidato creado exitosamente")
        return response.json()['candidato']['id']
    else:
        print(f"Error creando candidato: {response.text}")
        return None

def test_create_vacante(token):
    """Test crear vacante"""
    auth_headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    
    vacante_data = {
        'nombre': 'Desarrollador Python Senior',
        'descripcion': 'Buscamos desarrollador Python con experiencia en Flask y Django',
        'reclutador_id': 2,  # ID del reclutador creado en datos iniciales
        'vacantes': 2,
        'prioridad': 'alta',
        'salario_min': 40000.00,
        'salario_max': 80000.00,
        'ubicacion': 'Ciudad de México',
        'modalidad': 'hibrido'
    }
    
    response = requests.post(f'{BASE_URL}/vacantes',
                           json=vacante_data,
                           headers=auth_headers)
    
    if response.status_code == 201:
        print("Vacante creada exitosamente")
        return response.json()['vacante']['id']
    else:
        print(f"Error creando vacante: {response.text}")
        return None

if __name__ == '__main__':
    print("Iniciando tests de la API...")
    
    # Test login
    token = test_login()
    if not token:
        exit(1)
    
    # Test crear candidato
    candidato_id = test_create_candidato(token)
    
    # Test crear vacante
    vacante_id = test_create_vacante(token)
    
    print("\nTests completados exitosamente!")

# Production deployment script (deploy.sh)
"""
#!/bin/bash

echo "Iniciando deployment del Sistema de Reclutamiento..."

# Actualizar código
git pull origin main

# Instalar/actualizar dependencias
pip install -r requirements.txt

# Ejecutar migraciones
flask db upgrade

# Reiniciar servicio (ajustar según tu setup de producción)
sudo systemctl restart recruitment-app

echo "Deployment completado!"
"""

# Security improvements (security_utils.py)
from functools import wraps
from flask import request, jsonify, current_app
import time
from collections import defaultdict

# Rate limiting simple
request_counts = defaultdict(lambda: {'count': 0, 'window_start': time.time()})

def rate_limit(max_requests=100, window=3600):  # 100 requests per hour
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            client_ip = request.remote_addr
            current_time = time.time()
            
            # Reset window if needed
            if current_time - request_counts[client_ip]['window_start'] > window:
                request_counts[client_ip] = {'count': 0, 'window_start': current_time}
            
            # Check limit
            if request_counts[client_ip]['count'] >= max_requests:
                return jsonify({'message': 'Rate limit exceeded'}), 429
            
            request_counts[client_ip]['count'] += 1
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def validate_file_type(allowed_types):
    """Decorator para validar tipos de archivo"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'file' in request.files:
                file = request.files['file']
                if file and file.filename:
                    file_ext = file.filename.rsplit('.', 1)[1].lower()
                    if file_ext not in allowed_types:
                        return jsonify({'message': f'Tipo de archivo no permitido. Permitidos: {", ".join(allowed_types)}'}), 400
            return f(*args, **kwargs)
        return decorated_function
    return decorator