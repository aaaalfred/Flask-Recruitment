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
