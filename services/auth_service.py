from functools import wraps
from flask import jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from extensions import db

def token_required(f):
    @wraps(f)
    @jwt_required()
    def decorated(*args, **kwargs):
        try:
            from models import Usuario
            current_user_id = get_jwt_identity()
            current_user = Usuario.query.get(int(current_user_id))  # Convertir de vuelta a int
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
        from models import Usuario
        user = Usuario.query.filter_by(email=email, activo=True).first()
        if user and user.check_password(password):
            access_token = create_access_token(identity=str(user.id))  # Convertir a string
            return {
                'success': True,
                'access_token': access_token,
                'user': user.to_dict()
            }
        return {'success': False, 'message': 'Credenciales inválidas'}
    except Exception as e:
        return {'success': False, 'message': f'Error de autenticación: {str(e)}'}
