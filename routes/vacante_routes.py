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
