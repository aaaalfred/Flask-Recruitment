from flask import Blueprint, request, jsonify
from services.auth_service import token_required, role_required
from models import CandidatosPositions, Candidato, Vacante, db
from datetime import datetime

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
        contratado_status = request.args.get('contratado_status')
        
        query = CandidatosPositions.query
        
        # Filtros
        if candidato_id:
            query = query.filter_by(candidato_id=candidato_id)
        if vacante_id:
            query = query.filter_by(vacante_id=vacante_id)
        if status:
            query = query.filter_by(status=status)
        if contratado_status:
            query = query.filter_by(contratado_status=contratado_status)
        
        # Filtrar según rol del usuario
        if current_user.rol == 'reclutador':
            query = query.join(Candidato).filter(Candidato.reclutador_id == current_user.id)
        
        asignaciones = query.order_by(CandidatosPositions.fecha_asignacion.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        result = []
        for asignacion in asignaciones.items:
            asignacion_dict = asignacion.to_dict()
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
            aceptado=data.get('aceptado', False),
            contratado_status=data.get('contratado_status', 'pendiente'),
            comentarios_finales=data.get('comentarios_finales'),
            archivo_cv=data.get('archivo_cv'),
            cv_url_especifico=data.get('cv_url_especifico'),
            se_presento=data.get('se_presento', True),
            motivo_rechazo=data.get('motivo_rechazo')
        )
        
        db.session.add(nueva_asignacion)
        db.session.commit()
        
        return jsonify({
            'message': 'Candidato asignado a vacante exitosamente',
            'asignacion': nueva_asignacion.to_dict()
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
        
        # Campos actualizables del proceso real
        campos_actualizables = [
            'status', 'aceptado', 'contratado_status', 'comentarios_finales',
            'archivo_cv', 'cv_url_especifico', 'se_presento', 'motivo_rechazo',
            'entrevista_realizada'
        ]
        
        for campo in campos_actualizables:
            if campo in data:
                setattr(asignacion, campo, data[campo])
        
        # Actualizar fecha de decisión si se cambia el status de contratación
        if 'contratado_status' in data and data['contratado_status'] != 'pendiente':
            asignacion.fecha_decision_final = datetime.utcnow()
        
        # Actualizar el status general basado en el contratado_status
        if asignacion.contratado_status == 'contratado':
            asignacion.status = 'contratado'
        elif asignacion.contratado_status in ['rechazado', 'no_contratable']:
            asignacion.status = 'rechazado'
        
        db.session.commit()
        
        # Verificar si la vacante debe marcarse como cubierta
        vacante = asignacion.vacante
        if vacante:
            vacante.actualizar_status_final()
            db.session.commit()
        
        return jsonify({
            'message': 'Asignación actualizada exitosamente',
            'asignacion': asignacion.to_dict()
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

# Nuevos endpoints específicos para el flujo real

@candidatos_posiciones_bp.route('/<int:asignacion_id>/aceptar-supervisor', methods=['POST'])
@token_required
def aceptar_por_supervisor(current_user, asignacion_id):
    """Marcar candidato como aceptado por supervisor"""
    try:
        asignacion = CandidatosPositions.query.get_or_404(asignacion_id)
        
        data = request.get_json()
        aceptado = data.get('aceptado', True)
        comentarios = data.get('comentarios', '')
        
        asignacion.aceptado = aceptado
        asignacion.status = 'aceptado_supervisor' if aceptado else 'rechazado_supervisor'
        
        if comentarios:
            asignacion.comentarios_finales = comentarios
        
        # Si es aceptado, marcarlo como en proceso para contratación
        if aceptado:
            asignacion.contratado_status = 'pendiente'
        else:
            asignacion.contratado_status = 'rechazado'
            asignacion.fecha_decision_final = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': f'Candidato {"aceptado" if aceptado else "rechazado"} por supervisor',
            'asignacion': asignacion.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error procesando decisión: {str(e)}'}), 500

@candidatos_posiciones_bp.route('/<int:asignacion_id>/finalizar-proceso', methods=['POST'])
@token_required
def finalizar_proceso_candidato(current_user, asignacion_id):
    """Finalizar proceso de candidato con decisión final"""
    try:
        asignacion = CandidatosPositions.query.get_or_404(asignacion_id)
        
        data = request.get_json()
        contratado_status = data.get('contratado_status')  # contratado, rechazado, no_contratable
        comentarios_finales = data.get('comentarios_finales', '')
        se_presento = data.get('se_presento', True)
        
        if not contratado_status:
            return jsonify({'message': 'contratado_status es requerido'}), 400
        
        asignacion.contratado_status = contratado_status
        asignacion.comentarios_finales = comentarios_finales
        asignacion.se_presento = se_presento
        asignacion.fecha_decision_final = datetime.utcnow()
        
        # Actualizar status general
        if contratado_status == 'contratado':
            asignacion.status = 'contratado'
        else:
            asignacion.status = 'rechazado'
        
        db.session.commit()
        
        # Actualizar status de la vacante
        vacante = asignacion.vacante
        if vacante:
            vacante.actualizar_status_final()
            db.session.commit()
        
        return jsonify({
            'message': 'Proceso finalizado exitosamente',
            'asignacion': asignacion.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error finalizando proceso: {str(e)}'}), 500

@candidatos_posiciones_bp.route('/por-vacante/<int:vacante_id>', methods=['GET'])
@token_required
def get_candidatos_por_vacante(current_user, vacante_id):
    """Obtener todos los candidatos de una vacante específica con su estado"""
    try:
        vacante = Vacante.query.get_or_404(vacante_id)
        
        # Verificar permisos
        if (current_user.rol == 'reclutador' and 
            vacante.reclutador_id != current_user.id):
            return jsonify({'message': 'Sin permisos para ver candidatos de esta vacante'}), 403
        
        asignaciones = CandidatosPositions.query.filter_by(vacante_id=vacante_id).all()
        
        candidatos_detalle = []
        for asignacion in asignaciones:
            candidato_info = {
                'asignacion_id': asignacion.id,
                'candidato': asignacion.candidato.to_dict(),
                'proceso': asignacion.to_dict()
            }
            candidatos_detalle.append(candidato_info)
        
        # Estadísticas de la vacante
        stats = {
            'total_candidatos': len(asignaciones),
            'aceptados_supervisor': len([a for a in asignaciones if a.aceptado]),
            'contratados': len([a for a in asignaciones if a.contratado_status == 'contratado']),
            'rechazados': len([a for a in asignaciones if a.contratado_status == 'rechazado']),
            'no_contratables': len([a for a in asignaciones if a.contratado_status == 'no_contratable']),
            'pendientes': len([a for a in asignaciones if a.contratado_status == 'pendiente'])
        }
        
        return jsonify({
            'vacante': vacante.to_dict(),
            'candidatos': candidatos_detalle,
            'estadisticas': stats
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error obteniendo candidatos: {str(e)}'}), 500

@candidatos_posiciones_bp.route('/estadisticas', methods=['GET'])
@token_required
def get_estadisticas_proceso(current_user):
    """Obtener estadísticas generales del proceso de candidatos"""
    try:
        query = CandidatosPositions.query
        
        # Filtrar según rol del usuario
        if current_user.rol == 'reclutador':
            query = query.join(Candidato).filter(Candidato.reclutador_id == current_user.id)
        
        asignaciones = query.all()
        
        stats = {
            'total_asignaciones': len(asignaciones),
            'por_status': {},
            'por_contratado_status': {},
            'aceptados_supervisor': len([a for a in asignaciones if a.aceptado]),
            'no_se_presentaron': len([a for a in asignaciones if not a.se_presento]),
            'con_entrevista': len([a for a in asignaciones if a.entrevista_realizada])
        }
        
        # Contar por status
        for asignacion in asignaciones:
            status = asignacion.status or 'sin_status'
            contratado_status = asignacion.contratado_status or 'sin_status'
            
            stats['por_status'][status] = stats['por_status'].get(status, 0) + 1
            stats['por_contratado_status'][contratado_status] = stats['por_contratado_status'].get(contratado_status, 0) + 1
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({'message': f'Error obteniendo estadísticas: {str(e)}'}), 500
