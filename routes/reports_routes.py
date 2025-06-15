from flask import Blueprint, request, jsonify
from services.auth_service import token_required, role_required
from models import Vacante, Candidato, Entrevista, CandidatosPositions, Usuario, db
from sqlalchemy import func, desc
from datetime import datetime, timedelta

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/dashboard', methods=['GET'])
@token_required
def get_dashboard_stats(current_user):
    try:
        from sqlalchemy import and_, or_
        stats = {}
        
        print(f"🔍 Generando estadísticas para usuario: {current_user.nombre} ({current_user.rol})")
        
        # Aplicar filtros según el rol del usuario
        if current_user.rol == 'reclutador':
            # Solo datos del reclutador
            vacantes_filter = Vacante.reclutador_id == current_user.id
            candidatos_filter = Candidato.reclutador_id == current_user.id
        else:
            # Datos generales para ejecutivos y líderes
            vacantes_filter = True
            candidatos_filter = True
        
        # === CONSULTAS OPTIMIZADAS ===
        
        # 1. Estadísticas de vacantes en una sola consulta
        vacantes_stats = db.session.query(
            func.count(Vacante.id).label('total'),
            func.sum(func.case((Vacante.estado == 'abierta', 1), else_=0)).label('abiertas'),
            func.sum(func.case((Vacante.estado == 'cerrada', 1), else_=0)).label('cerradas'),
            func.sum(func.case((Vacante.estado == 'pausada', 1), else_=0)).label('pausadas'),
            func.sum(func.case((Vacante.estado == 'cancelada', 1), else_=0)).label('canceladas')
        ).filter(vacantes_filter).first()
        
        # 2. Estadísticas de candidatos en una sola consulta
        candidatos_stats = db.session.query(
            func.count(Candidato.id).label('total'),
            func.sum(func.case((Candidato.estado == 'activo', 1), else_=0)).label('activos'),
            func.sum(func.case((Candidato.estado == 'inactivo', 1), else_=0)).label('inactivos'),
            func.sum(func.case((Candidato.estado == 'blacklist', 1), else_=0)).label('blacklist')
        ).filter(candidatos_filter).first()
        
        # 3. Estadísticas de entrevistas en una sola consulta
        if current_user.rol == 'reclutador':
            entrevistas_stats = db.session.query(
                func.count(Entrevista.id).label('total'),
                func.sum(func.case((Entrevista.resultado == 'pendiente', 1), else_=0)).label('pendientes'),
                func.sum(func.case((Entrevista.resultado == 'aprobada', 1), else_=0)).label('aprobadas'),
                func.sum(func.case((Entrevista.resultado == 'rechazada', 1), else_=0)).label('rechazadas')
            ).join(Candidato).filter(Candidato.reclutador_id == current_user.id).first()
        else:
            entrevistas_stats = db.session.query(
                func.count(Entrevista.id).label('total'),
                func.sum(func.case((Entrevista.resultado == 'pendiente', 1), else_=0)).label('pendientes'),
                func.sum(func.case((Entrevista.resultado == 'aprobada', 1), else_=0)).label('aprobadas'),
                func.sum(func.case((Entrevista.resultado == 'rechazada', 1), else_=0)).label('rechazadas')
            ).first()
        
        # 4. Distribuciones con una consulta cada una
        vacantes_por_prioridad = db.session.query(
            func.coalesce(Vacante.prioridad, 'sin_prioridad').label('prioridad'),
            func.count(Vacante.id).label('count')
        ).filter(vacantes_filter).group_by(Vacante.prioridad).all()
        
        vacantes_por_modalidad = db.session.query(
            func.coalesce(Vacante.modalidad, 'sin_modalidad').label('modalidad'),
            func.count(Vacante.id).label('count')
        ).filter(vacantes_filter).group_by(Vacante.modalidad).all()
        
        # 5. Candidatos por estado en posiciones
        if current_user.rol == 'reclutador':
            candidatos_por_estado = db.session.query(
                func.coalesce(CandidatosPositions.status, 'sin_estado').label('estado'),
                func.count(CandidatosPositions.id).label('count')
            ).join(Candidato).filter(
                Candidato.reclutador_id == current_user.id
            ).group_by(CandidatosPositions.status).all()
        else:
            candidatos_por_estado = db.session.query(
                func.coalesce(CandidatosPositions.status, 'sin_estado').label('estado'),
                func.count(CandidatosPositions.id).label('count')
            ).group_by(CandidatosPositions.status).all()
        
        # 6. Entrevistas por tipo
        if current_user.rol == 'reclutador':
            entrevistas_por_tipo = db.session.query(
                func.coalesce(Entrevista.tipo, 'sin_tipo').label('tipo'),
                func.count(Entrevista.id).label('count')
            ).join(Candidato).filter(
                Candidato.reclutador_id == current_user.id
            ).group_by(Entrevista.tipo).all()
        else:
            entrevistas_por_tipo = db.session.query(
                func.coalesce(Entrevista.tipo, 'sin_tipo').label('tipo'),
                func.count(Entrevista.id).label('count')
            ).group_by(Entrevista.tipo).all()
        
        # 7. Estadísticas de usuarios (solo para ejecutivos y líderes)
        usuarios_stats = {}
        if current_user.rol in ['ejecutivo', 'reclutador_lider']:
            total_usuarios = Usuario.query.filter_by(activo=True).count()
            usuarios_por_rol = db.session.query(
                Usuario.rol,
                func.count(Usuario.id).label('count')
            ).filter_by(activo=True).group_by(Usuario.rol).all()
            
            usuarios_stats = {
                'total_usuarios': total_usuarios,
                'por_rol': {rol: count for rol, count in usuarios_por_rol}
            }
        
        # 8. Rendimiento por reclutador (simplificado)
        rendimiento_reclutadores = []
        if current_user.rol in ['ejecutivo', 'reclutador_lider']:
            # Solo obtener reclutadores activos
            reclutadores = db.session.query(Usuario.id, Usuario.nombre).filter(
                Usuario.rol.in_(['reclutador', 'reclutador_lider']),
                Usuario.activo == True
            ).limit(10).all()  # Limitar a 10 para performance
            
            for reclutador_id, reclutador_nombre in reclutadores:
                # Consulta optimizada por reclutador
                r_stats = db.session.query(
                    func.count(func.distinct(Vacante.id)).label('vacantes'),
                    func.count(func.distinct(Candidato.id)).label('candidatos'),
                    func.count(func.distinct(Entrevista.id)).label('entrevistas')
                ).select_from(Candidato).outerjoin(
                    Vacante, Vacante.reclutador_id == Candidato.reclutador_id
                ).outerjoin(
                    Entrevista, Entrevista.candidato_id == Candidato.id
                ).filter(Candidato.reclutador_id == reclutador_id).first()
                
                r_seleccionados = db.session.query(func.count(CandidatosPositions.id)).join(
                    Candidato
                ).filter(
                    Candidato.reclutador_id == reclutador_id,
                    CandidatosPositions.status == 'seleccionado'
                ).scalar() or 0
                
                efectividad = (r_seleccionados / r_stats.candidatos * 100) if r_stats.candidatos > 0 else 0
                
                rendimiento_reclutadores.append({
                    'nombre': reclutador_nombre,
                    'vacantes': r_stats.vacantes or 0,
                    'candidatos': r_stats.candidatos or 0,
                    'entrevistas': r_stats.entrevistas or 0,
                    'seleccionados': r_seleccionados,
                    'efectividad': round(efectividad, 1)
                })
        
        # 9. Vacantes antiguas (limitado a 5)
        now = datetime.utcnow()
        fecha_limite_30_dias = now - timedelta(days=30)
        
        vacantes_antiguas_query = db.session.query(
            Vacante.id,
            Vacante.nombre,
            Vacante.fecha_creacion,
            func.coalesce(Vacante.prioridad, 'sin_prioridad').label('prioridad'),
            Usuario.nombre.label('ejecutivo_nombre')
        ).join(Usuario, Vacante.ejecutivo_id == Usuario.id, isouter=True).filter(
            and_(
                vacantes_filter,
                Vacante.estado == 'abierta',
                Vacante.fecha_creacion.isnot(None),
                Vacante.fecha_creacion <= fecha_limite_30_dias
            )
        ).order_by(Vacante.fecha_creacion.asc()).limit(5).all()
        
        vacantes_antiguas = []
        for v in vacantes_antiguas_query:
            dias_transcurridos = (now - v.fecha_creacion).days
            candidatos_count = db.session.query(func.count(CandidatosPositions.id)).filter_by(
                vacante_id=v.id
            ).scalar() or 0
            
            vacantes_antiguas.append({
                'id': v.id,
                'nombre': v.nombre,
                'dias_transcurridos': dias_transcurridos,
                'candidatos': candidatos_count,
                'ejecutivo': v.ejecutivo_nombre or 'N/A',
                'prioridad': v.prioridad
            })
        
        # 10. Actividad reciente (últimos 7 días)
        fecha_limite_7_dias = now - timedelta(days=7)
        
        candidatos_recientes = db.session.query(func.count(Candidato.id)).filter(
            and_(
                candidatos_filter,
                Candidato.fecha_creacion >= fecha_limite_7_dias
            )
        ).scalar() or 0
        
        if current_user.rol == 'reclutador':
            entrevistas_recientes = db.session.query(func.count(Entrevista.id)).join(
                Candidato
            ).filter(
                and_(
                    Candidato.reclutador_id == current_user.id,
                    Entrevista.fecha.isnot(None),
                    Entrevista.fecha >= fecha_limite_7_dias
                )
            ).scalar() or 0
        else:
            entrevistas_recientes = db.session.query(func.count(Entrevista.id)).filter(
                and_(
                    Entrevista.fecha.isnot(None),
                    Entrevista.fecha >= fecha_limite_7_dias
                )
            ).scalar() or 0
        
        # === COMPILAR RESPUESTA OPTIMIZADA ===
        stats = {
            # Métricas principales
            'total_vacantes': vacantes_stats.total or 0,
            'vacantes_abiertas': vacantes_stats.abiertas or 0,
            'vacantes_cerradas': vacantes_stats.cerradas or 0,
            'vacantes_pausadas': vacantes_stats.pausadas or 0,
            'vacantes_canceladas': vacantes_stats.canceladas or 0,
            
            'total_candidatos': candidatos_stats.total or 0,
            'candidatos_activos': candidatos_stats.activos or 0,
            'candidatos_inactivos': candidatos_stats.inactivos or 0,
            'candidatos_blacklist': candidatos_stats.blacklist or 0,
            
            'total_entrevistas': entrevistas_stats.total or 0,
            'entrevistas_pendientes': entrevistas_stats.pendientes or 0,
            'entrevistas_aprobadas': entrevistas_stats.aprobadas or 0,
            'entrevistas_rechazadas': entrevistas_stats.rechazadas or 0,
            
            # Distribuciones
            'vacantes_por_prioridad': {prioridad: count for prioridad, count in vacantes_por_prioridad},
            'vacantes_por_modalidad': {modalidad: count for modalidad, count in vacantes_por_modalidad},
            'candidatos_por_estado': {estado: count for estado, count in candidatos_por_estado},
            'entrevistas_por_tipo': {tipo: count for tipo, count in entrevistas_por_tipo},
            
            # Usuarios (solo para ejecutivos y líderes)
            'usuarios': usuarios_stats,
            
            # Rendimiento
            'rendimiento_reclutadores': rendimiento_reclutadores,
            
            # Vacantes que requieren atención
            'vacantes_antiguas': vacantes_antiguas,
            
            # Actividad reciente
            'candidatos_recientes': candidatos_recientes,
            'entrevistas_recientes': entrevistas_recientes,
            
            # Metadatos
            'fecha_actualizacion': now.isoformat(),
            'tipo_usuario': current_user.rol
        }
        
        print(f"✅ Estadísticas generadas exitosamente")
        return jsonify(stats), 200
        
    except Exception as e:
        print(f"❌ Error en dashboard: {str(e)}")
        import traceback
        traceback.print_exc()
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

# === ENDPOINT ADICIONAL PARA ESTADÍSTICAS DE USUARIOS ===
@reports_bp.route('/usuarios/estadisticas', methods=['GET'])
@role_required('ejecutivo', 'reclutador_lider')
def get_user_stats(current_user):
    try:
        # Estadísticas generales de usuarios
        total_usuarios = Usuario.query.filter_by(activo=True).count()
        usuarios_inactivos = Usuario.query.filter_by(activo=False).count()
        
        # Usuarios por rol
        usuarios_por_rol = db.session.query(
            Usuario.rol,
            func.count(Usuario.id).label('count')
        ).filter_by(activo=True).group_by(Usuario.rol).all()
        
        # Usuarios creados en los últimos 30 días
        fecha_limite = datetime.utcnow() - timedelta(days=30)
        usuarios_recientes = Usuario.query.filter(
            Usuario.fecha_creacion >= fecha_limite,
            Usuario.activo == True
        ).count()
        
        # Actividad por reclutador (últimos 30 días)
        actividad_reclutadores = []
        reclutadores = Usuario.query.filter(
            Usuario.rol.in_(['reclutador', 'reclutador_lider']),
            Usuario.activo == True
        ).all()
        
        for reclutador in reclutadores:
            # Actividad reciente
            candidatos_mes = Candidato.query.filter(
                Candidato.reclutador_id == reclutador.id,
                Candidato.fecha_creacion >= fecha_limite
            ).count()
            
            entrevistas_mes = Entrevista.query.join(Candidato).filter(
                Candidato.reclutador_id == reclutador.id,
                Entrevista.fecha >= fecha_limite
            ).count()
            
            actividad_reclutadores.append({
                'id': reclutador.id,
                'nombre': reclutador.nombre,
                'email': reclutador.email,
                'rol': reclutador.rol,
                'candidatos_mes': candidatos_mes,
                'entrevistas_mes': entrevistas_mes,
                'fecha_creacion': reclutador.fecha_creacion.isoformat() if reclutador.fecha_creacion else None
            })
        
        # Ordenar por actividad (candidatos + entrevistas)
        actividad_reclutadores.sort(
            key=lambda x: x['candidatos_mes'] + x['entrevistas_mes'], 
            reverse=True
        )
        
        stats = {
            'total_usuarios': total_usuarios,
            'usuarios_inactivos': usuarios_inactivos,
            'usuarios_por_rol': {rol: count for rol, count in usuarios_por_rol},
            'usuarios_recientes': usuarios_recientes,
            'actividad_reclutadores': actividad_reclutadores,
            'fecha_actualizacion': datetime.utcnow().isoformat()
        }
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({'message': f'Error obteniendo estadísticas de usuarios: {str(e)}'}), 500
