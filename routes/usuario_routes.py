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
