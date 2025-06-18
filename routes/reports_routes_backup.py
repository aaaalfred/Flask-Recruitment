from flask import Blueprint, request, jsonify
from services.auth_service import token_required, role_required
from models import Vacante, Candidato, Entrevista, CandidatosPositions, Usuario, Cliente, db
from sqlalchemy import func, desc, case
from datetime import datetime, timedelta

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/dashboard', methods=['GET'])
@token_required
def get_dashboard_stats(current_user):
    try:
        print(f"🔍 Generando estadísticas mejoradas para: {current_user.nombre} ({current_user.rol})")
        
        # Función para aplicar filtros según el rol del usuario
        def apply_filter(query, field):
            if current_user.rol == 'reclutador':
                return query.filter(field == current_user.id)
            elif current_user.rol == 'ejecutivo':
                # Los ejecutivos ven vacantes donde son ejecutivo_id
                if 'ejecutivo_id' in str(field):
                    return query.filter(field == current_user.id)
                elif 'reclutador_id' in str(field):
                    # Para candidatos/entrevistas, ver los de sus vacantes
                    vacantes_ejecutivo = db.session.query(Vacante.id).filter_by(ejecutivo_id=current_user.id).subquery()
                    if 'candidato' in str(query).lower():
                        return query.join(CandidatosPositions).join(Vacante).filter(Vacante.ejecutivo_id == current_user.id)
                    elif 'entrevista' in str(query).lower():
                        return query.join(Vacante).filter(Vacante.ejecutivo_id == current_user.id)
                return query
            return query
        
        # === ESTADÍSTICAS PRINCIPALES ===
        
        # Vacantes con filtros por rol
        if current_user.rol == 'reclutador':
            vacantes_query = Vacante.query.filter_by(reclutador_id=current_user.id)
        elif current_user.rol == 'ejecutivo':
            vacantes_query = Vacante.query.filter_by(ejecutivo_id=current_user.id)
        else:
            vacantes_query = Vacante.query
            
        total_vacantes = vacantes_query.count()
        vacantes_abiertas = vacantes_query.filter_by(estado='abierta').count()
        vacantes_cerradas = vacantes_query.filter_by(estado='cerrada').count()
        vacantes_pausadas = vacantes_query.filter_by(estado='pausada').count()
        vacantes_canceladas = vacantes_query.filter_by(estado='cancelada').count()
        vacantes_cubiertas = vacantes_query.filter_by(status_final='cubierta').count()
        
        # Candidatos con filtros por rol
        if current_user.rol == 'reclutador':
            candidatos_query = Candidato.query.filter_by(reclutador_id=current_user.id)
        elif current_user.rol == 'ejecutivo':
            # Los ejecutivos ven candidatos de sus vacantes
            candidatos_query = Candidato.query.join(CandidatosPositions).join(Vacante).filter(
                Vacante.ejecutivo_id == current_user.id
            )
        else:
            candidatos_query = Candidato.query
            
        total_candidatos = candidatos_query.count()
        candidatos_activos = candidatos_query.filter_by(estado='activo').count()
        candidatos_inactivos = candidatos_query.filter_by(estado='inactivo').count()
        candidatos_blacklist = candidatos_query.filter_by(estado='blacklist').count()
        
        # Entrevistas con filtros por rol
        if current_user.rol == 'reclutador':
            entrevistas_query = Entrevista.query.join(Candidato).filter(Candidato.reclutador_id == current_user.id)
        elif current_user.rol == 'ejecutivo':
            entrevistas_query = Entrevista.query.join(Vacante).filter(Vacante.ejecutivo_id == current_user.id)
        else:
            entrevistas_query = Entrevista.query
            
        total_entrevistas = entrevistas_query.count()
        entrevistas_pendientes = entrevistas_query.filter(Entrevista.resultado == 'pendiente').count()
        entrevistas_aprobadas = entrevistas_query.filter(Entrevista.resultado == 'aprobada').count()
        entrevistas_rechazadas = entrevistas_query.filter(Entrevista.resultado == 'rechazada').count()
        
        # === MÉTRICAS DE PROCESO REAL ===
        
        # Candidatos-posiciones con filtros
        if current_user.rol == 'reclutador':
            cp_query = CandidatosPositions.query.join(Candidato).filter(Candidato.reclutador_id == current_user.id)
        elif current_user.rol == 'ejecutivo':
            cp_query = CandidatosPositions.query.join(Vacante).filter(Vacante.ejecutivo_id == current_user.id)
        else:
            cp_query = CandidatosPositions.query
        
        # Estadísticas por status de candidatos
        candidatos_por_status = dict(
            cp_query.with_entities(CandidatosPositions.status, func.count(CandidatosPositions.id))
            .group_by(CandidatosPositions.status).all()
        )
        
        # Estadísticas por status de contratación
        candidatos_por_contratacion = dict(
            cp_query.with_entities(CandidatosPositions.contratado_status, func.count(CandidatosPositions.id))
            .group_by(CandidatosPositions.contratado_status).all()
        )
        
        # Candidatos aceptados por supervisor
        candidatos_aceptados_supervisor = cp_query.filter_by(aceptado=True).count()
        
        # === DISTRIBUCIONES ===
        
        # Vacantes por prioridad
        vacantes_por_prioridad = dict(
            vacantes_query.with_entities(Vacante.prioridad, func.count(Vacante.id))
            .group_by(Vacante.prioridad).all()
        )
        
        # Vacantes por modalidad
        vacantes_por_modalidad = dict(
            vacantes_query.with_entities(Vacante.modalidad, func.count(Vacante.id))
            .group_by(Vacante.modalidad).all()
        )
        
        # Entrevistas por tipo
        entrevistas_por_tipo = dict(
            entrevistas_query.with_entities(Entrevista.tipo, func.count(Entrevista.id))
            .group_by(Entrevista.tipo).all()
        )
        
        # === ACTIVIDAD RECIENTE (7 días) ===
        fecha_limite_7_dias = datetime.utcnow() - timedelta(days=7)
        
        # Actividad reciente (7 días)
        candidatos_recientes = candidatos_query.filter(Candidato.fecha_creacion >= fecha_limite_7_dias).count()
        entrevistas_recientes = entrevistas_query.filter(Entrevista.fecha >= fecha_limite_7_dias).count()
        vacantes_recientes = vacantes_query.filter(Vacante.fecha_solicitud >= fecha_limite_7_dias).count()
        
        # === ANÁLISIS POR CLIENTE (Solo supervisores) ===
        clientes_stats = []
        if current_user.rol in ['ejecutivo', 'reclutador_lider', 'administrador']:
            try:
                # Consulta optimizada para análisis de clientes
                clientes_data = db.session.query(
                    Cliente.nombre,
                    Cliente.ccp,
                    func.count(Vacante.id).label('total_vacantes'),
                    func.sum(case((Vacante.status_final == 'cubierta', 1), else_=0)).label('vacantes_cubiertas')
                ).join(Vacante, Cliente.id == Vacante.cliente_id, isouter=True)\
                 .group_by(Cliente.id, Cliente.nombre, Cliente.ccp)\
                 .having(func.count(Vacante.id) > 0)\
                 .order_by(desc('total_vacantes')).limit(8).all()
                
                clientes_stats = [{
                    'nombre': nombre,
                    'ccp': ccp,
                    'total_vacantes': total_vacantes or 0,
                    'vacantes_cubiertas': vacantes_cubiertas or 0,
                    'tasa_exito': round((vacantes_cubiertas / total_vacantes * 100), 1) if total_vacantes > 0 else 0
                } for nombre, ccp, total_vacantes, vacantes_cubiertas in clientes_data]
            except Exception as e:
                print(f"Warning: Error en análisis de clientes: {str(e)}")
                clientes_stats = []
        
        # === VACANTES QUE REQUIEREN ATENCIÓN ===
        fecha_limite_30_dias = datetime.utcnow() - timedelta(days=30)
        
        vacantes_antiguas_raw = vacantes_query.filter(
            Vacante.estado == 'abierta',
            Vacante.fecha_solicitud <= fecha_limite_30_dias
        ).order_by(Vacante.fecha_solicitud.asc()).limit(5).all()
        
        vacantes_antiguas = []
        for v in vacantes_antiguas_raw:
            dias_transcurridos = (datetime.utcnow() - v.fecha_solicitud).days if v.fecha_solicitud else 0
            candidatos_count = len(v.candidatos_posiciones) if v.candidatos_posiciones else 0
            candidatos_faltantes = max(0, (v.candidatos_requeridos or 3) - candidatos_count)
            
            vacantes_antiguas.append({
                'id': v.id,
                'nombre': v.nombre,
                'cliente_nombre': v.cliente.nombre if v.cliente else 'Sin cliente',
                'cliente_ccp': v.cliente.ccp if v.cliente else 'N/A',
                'dias_transcurridos': dias_transcurridos,
                'candidatos_actuales': candidatos_count,
                'candidatos_requeridos': v.candidatos_requeridos or 3,
                'candidatos_faltantes': candidatos_faltantes,
                'ejecutivo': v.ejecutivo.nombre if v.ejecutivo else 'N/A',
                'prioridad': v.prioridad or 'media',
                'avance': v.avance or 'Sin avance'
            })
        
        # === RENDIMIENTO POR RECLUTADOR (Solo supervisores) ===
        rendimiento_reclutadores = []
        if current_user.rol in ['ejecutivo', 'reclutador_lider', 'administrador']:
            reclutadores = Usuario.query.filter(
                Usuario.rol.in_(['reclutador', 'reclutador_lider']),
                Usuario.activo == True
            ).limit(8).all()
            
            for reclutador in reclutadores:
                r_vacantes = Vacante.query.filter_by(reclutador_id=reclutador.id).count()
                r_candidatos = Candidato.query.filter_by(reclutador_id=reclutador.id).count()
                
                r_aceptados = db.session.query(CandidatosPositions).join(Candidato).filter(
                    Candidato.reclutador_id == reclutador.id,
                    CandidatosPositions.aceptado == True
                ).count()
                
                r_contratados = db.session.query(CandidatosPositions).join(Candidato).filter(
                    Candidato.reclutador_id == reclutador.id,
                    CandidatosPositions.contratado_status == 'contratado'
                ).count()
                
                efectividad_final = round((r_contratados / r_candidatos * 100), 1) if r_candidatos > 0 else 0
                
                actividad_reciente = Candidato.query.filter(
                    Candidato.reclutador_id == reclutador.id,
                    Candidato.fecha_creacion >= fecha_limite_7_dias
                ).count()
                
                rendimiento_reclutadores.append({
                    'nombre': reclutador.nombre,
                    'vacantes_asignadas': r_vacantes,
                    'candidatos_gestionados': r_candidatos,
                    'candidatos_aceptados': r_aceptados,
                    'candidatos_contratados': r_contratados,
                    'efectividad_final': efectividad_final,
                    'actividad_reciente': actividad_reciente
                })
            
            rendimiento_reclutadores.sort(key=lambda x: x['efectividad_final'], reverse=True)
        
        # === MÉTRICAS DE RENDIMIENTO ===
        tasa_conversion_global = round((candidatos_aceptados_supervisor / total_candidatos * 100), 1) if total_candidatos > 0 else 0
        
        # Tiempo promedio de resolución simplificado
        vacantes_con_cierre = vacantes_query.filter(Vacante.fecha_cierre.isnot(None)).all()
        tiempos_resolucion = []
        for v in vacantes_con_cierre:
            if v.fecha_solicitud and v.fecha_cierre:
                dias = (v.fecha_cierre - v.fecha_solicitud).days
                tiempos_resolucion.append(dias)
        tiempo_promedio_resolucion = round(sum(tiempos_resolucion) / len(tiempos_resolucion), 1) if tiempos_resolucion else 0
        
        # === ESTADÍSTICAS DE USUARIOS (Solo supervisores) ===
        usuarios_stats = {}
        if current_user.rol in ['ejecutivo', 'reclutador_lider', 'administrador']:
            total_usuarios = Usuario.query.filter_by(activo=True).count()
            usuarios_por_rol = dict(
                Usuario.query.filter_by(activo=True)
                .with_entities(Usuario.rol, func.count(Usuario.id))
                .group_by(Usuario.rol).all()
            )
            usuarios_recientes = Usuario.query.filter(
                Usuario.fecha_creacion >= fecha_limite_7_dias,
                Usuario.activo == True
            ).count()
            
            usuarios_stats = {
                'total_usuarios': total_usuarios,
                'por_rol': usuarios_por_rol,
                'usuarios_recientes': usuarios_recientes
            }
        
        # === RESPUESTA FINAL ===
        stats = {
            # Métricas principales
            'total_vacantes': total_vacantes,
            'vacantes_abiertas': vacantes_abiertas,
            'vacantes_cerradas': vacantes_cerradas,
            'vacantes_pausadas': vacantes_pausadas,
            'vacantes_canceladas': vacantes_canceladas,
            'vacantes_cubiertas': vacantes_cubiertas,
            
            'total_candidatos': total_candidatos,
            'candidatos_activos': candidatos_activos,
            'candidatos_inactivos': candidatos_inactivos,
            'candidatos_blacklist': candidatos_blacklist,
            
            'total_entrevistas': total_entrevistas,
            'entrevistas_pendientes': entrevistas_pendientes,
            'entrevistas_aprobadas': entrevistas_aprobadas,
            'entrevistas_rechazadas': entrevistas_rechazadas,
            
            # Métricas de proceso
            'candidatos_por_status': candidatos_por_status,
            'candidatos_por_contratacion': candidatos_por_contratacion,
            'candidatos_aceptados_supervisor': candidatos_aceptados_supervisor,
            
            # Distribuciones
            'vacantes_por_prioridad': vacantes_por_prioridad,
            'vacantes_por_modalidad': vacantes_por_modalidad,
            'entrevistas_por_tipo': entrevistas_por_tipo,
            
            # Métricas de rendimiento
            'tiempo_promedio_resolucion': tiempo_promedio_resolucion,
            'tasa_conversion_global': tasa_conversion_global,
            
            # Actividad reciente
            'candidatos_recientes': candidatos_recientes,
            'entrevistas_recientes': entrevistas_recientes,
            'vacantes_recientes': vacantes_recientes,
            
            # Análisis por cliente
            'clientes_stats': clientes_stats,
            
            # Alertas y atención
            'vacantes_antiguas': vacantes_antiguas,
            
            # Rendimiento del equipo
            'rendimiento_reclutadores': rendimiento_reclutadores,
            
            # Usuarios (solo supervisores)
            'usuarios': usuarios_stats,
            
            # Metadatos
            'fecha_actualizacion': datetime.utcnow().isoformat(),
            'tipo_usuario': current_user.rol,
            'usuario_nombre': current_user.nombre,
            'filtrado_por_reclutador': current_user.rol == 'reclutador'
        }
        
        print(f"✅ Estadísticas mejoradas generadas para {current_user.nombre}")
        print(f"📊 Vacantes: {total_vacantes}, Candidatos: {total_candidatos}, Entrevistas: {total_entrevistas}")
        
        return jsonify(stats), 200
        
    except Exception as e:
        print(f"❌ Error en dashboard mejorado: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'message': f'Error obteniendo estadísticas: {str(e)}',
            'error_type': type(e).__name__
        }), 500

# Endpoint adicional simple para reportes de vacante
@reports_bp.route('/vacante/<int:vacante_id>/reporte', methods=['GET'])
@role_required('ejecutivo', 'reclutador_lider', 'administrador')
def get_vacante_report(current_user, vacante_id):
    try:
        vacante = Vacante.query.get_or_404(vacante_id)
        
        # Información básica de la vacante
        reporte = {
            'vacante': vacante.to_dict(),
            'resumen': {}
        }
        
        # Candidatos por estado
        candidatos_por_estado = {}
        for status in ['postulado', 'en_proceso', 'rechazado', 'aceptado', 'contratado']:
            count = CandidatosPositions.query.filter_by(vacante_id=vacante_id, status=status).count()
            candidatos_por_estado[status] = count
        
        reporte['resumen']['candidatos_por_estado'] = candidatos_por_estado
        
        # Entrevistas por resultado
        entrevistas_por_resultado = {}
        for resultado in ['pendiente', 'aprobada', 'rechazada', 'reprogramar']:
            count = Entrevista.query.filter_by(vacante_id=vacante_id, resultado=resultado).count()
            entrevistas_por_resultado[resultado] = count
        
        reporte['resumen']['entrevistas_por_resultado'] = entrevistas_por_resultado
        
        # Lista de candidatos con detalles
        candidatos_detalle = []
        candidatos_posiciones = CandidatosPositions.query.filter_by(vacante_id=vacante_id).all()
        
        for cp in candidatos_posiciones:
            candidato_dict = cp.candidato.to_dict()
            candidato_dict.update({
                'status_vacante': cp.status,
                'aceptado': cp.aceptado,
                'contratado_status': cp.contratado_status,
                'fecha_asignacion': cp.fecha_asignacion.isoformat() if cp.fecha_asignacion else None
            })
            candidatos_detalle.append(candidato_dict)
        
        reporte['candidatos'] = candidatos_detalle
        
        return jsonify(reporte), 200
        
    except Exception as e:
        print(f"❌ Error en reporte de vacante: {str(e)}")
        return jsonify({'message': f'Error generando reporte: {str(e)}'}), 500
