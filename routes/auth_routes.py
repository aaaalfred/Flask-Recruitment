from flask import Blueprint, request, jsonify
from services.auth_service import authenticate_user
from extensions import db

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
        from models import Usuario
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
