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
