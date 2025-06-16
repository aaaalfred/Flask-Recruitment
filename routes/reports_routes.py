from flask import Blueprint, request, jsonify
from services.auth_service import token_required, role_required
from models import Vacante, Candidato, Entrevista, CandidatosPositions, Usuario, db
from sqlalchemy import func, desc, and_, or_
from datetime import datetime, timedelta

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/dashboard', methods=['GET'])
@token_required
def get_dashboard_stats(current_user):
    try:
        print(f"🔍 Generando estadísticas para usuario: {current_user.nombre} ({current_user.rol})")
        
        stats = {}
        
        # === CONSULTAS BÁSICAS SIMPLIFICADAS ===
        
        # 1. Estadísticas básicas de vacantes
        if current_user.rol == 'reclutador':
            total_vacantes = Vacante.query.filter_by(reclutador_id=current_user.id).count()
            vacantes_abiertas = Vacante.query.filter_by(
                reclutador_id=current_user.id, 
                estado='abierta'
            ).count()
        else:
            total_vacantes = Vacante.query.count()
            vacantes_abiertas = Vacante.query.filter_by(estado='abierta').count()
        
        vacantes_cerradas = Vacante.query.filter_by(estado='cerrada').count()
        vacantes_pausadas = Vacante.query.filter_by(estado='pausada').count()
        vacantes_canceladas = Vacante.query.filter_by(estado='cancelada').count()
        
        # 2. Estadísticas básicas de candidatos
        if current_user.rol == 'reclutador':
            total_candidatos = Candidato.query.filter_by(reclutador_id=current_user.id).count()
            candidatos_activos = Candidato.query.filter_by(
                reclutador_id=current_user.id, 
                estado='activo'
            ).count()
        else:
            total_candidatos = Candidato.query.count()
            candidatos_activos = Candidato.query.filter_by(estado='activo').count()
        
        candidatos_inactivos = Candidato.query.filter_by(estado='inactivo').count()
        candidatos_blacklist = Candidato.query.filter_by(estado='blacklist').count()
        
        # 3. Estadísticas básicas de entrevistas
        if current_user.rol == 'reclutador':
            # Contar entrevistas usando join seguro
            total_entrevistas = db.session.query(Entrevista).join(Candidato).filter(
                Candidato.reclutador_id == current_user.id
            ).count()
            entrevistas_pendientes = db.session.query(Entrevista).join(Candidato).filter(
                Candidato.reclutador_id == current_user.id,
                Entrevista.resultado == 'pendiente'
            ).count()
        else:
            total_entrevistas = Entrevista.query.count()
            entrevistas_pendientes = Entrevista.query.filter_by(resultado='pendiente').count()
        
        entrevistas_aprobadas = Entrevista.query.filter_by(resultado='aprobada').count()
        entrevistas_rechazadas = Entrevista.query.filter_by(resultado='rechazada').count()
        
        # 4. Estadísticas de usuarios (solo para ejecutivos y líderes)
        usuarios_stats = {}
        if current_user.rol in ['ejecutivo', 'reclutador_lider', 'administrador']:
            total_usuarios = Usuario.query.filter_by(activo=True).count()
            ejecutivos = Usuario.query.filter_by(rol='ejecutivo', activo=True).count()
            reclutadores = Usuario.query.filter_by(rol='reclutador', activo=True).count()
            lideres = Usuario.query.filter_by(rol='reclutador_lider', activo=True).count()
            admins = Usuario.query.filter_by(rol='administrador', activo=True).count()
            
            usuarios_stats = {
                'total_usuarios': total_usuarios,
                'por_rol': {
                    'ejecutivo': ejecutivos,
                    'reclutador': reclutadores,
                    'reclutador_lider': lideres,
                    'administrador': admins
                }
            }
        
        # 5. Actividad reciente (últimos 7 días)
        fecha_limite_7_dias = datetime.utcnow() - timedelta(days=7)
        
        if current_user.rol == 'reclutador':
            candidatos_recientes = Candidato.query.filter(
                Candidato.reclutador_id == current_user.id,
                Candidato.fecha_creacion >= fecha_limite_7_dias
            ).count()
            entrevistas_recientes = db.session.query(Entrevista).join(Candidato).filter(
                Candidato.reclutador_id == current_user.id,
                Entrevista.fecha >= fecha_limite_7_dias
            ).count()
        else:
            candidatos_recientes = Candidato.query.filter(
                Candidato.fecha_creacion >= fecha_limite_7_dias
            ).count()
            entrevistas_recientes = Entrevista.query.filter(
                Entrevista.fecha >= fecha_limite_7_dias
            ).count()
        
        # 6. Vacantes que requieren atención (más de 30 días)
        fecha_limite_30_dias = datetime.utcnow() - timedelta(days=30)
        
        if current_user.rol == 'reclutador':
            vacantes_antiguas_query = Vacante.query.filter(
                Vacante.reclutador_id == current_user.id,
                Vacante.estado == 'abierta',
                Vacante.fecha_creacion <= fecha_limite_30_dias
            ).limit(5).all()
        else:
            vacantes_antiguas_query = Vacante.query.filter(
                Vacante.estado == 'abierta',
                Vacante.fecha_creacion <= fecha_limite_30_dias
            ).limit(5).all()
        
        vacantes_antiguas = []
        for v in vacantes_antiguas_query:
            dias_transcurridos = (datetime.utcnow() - v.fecha_creacion).days if v.fecha_creacion else 0
            candidatos_count = CandidatosPositions.query.filter_by(vacante_id=v.id).count()
            
            vacantes_antiguas.append({
                'id': v.id,
                'nombre': v.nombre,
                'dias_transcurridos': dias_transcurridos,
                'candidatos': candidatos_count,
                'ejecutivo': v.ejecutivo.nombre if v.ejecutivo else 'N/A',
                'prioridad': v.prioridad or 'media'
            })
        
        # 7. Rendimiento por reclutador (solo para supervisores)
        rendimiento_reclutadores = []
        if current_user.rol in ['ejecutivo', 'reclutador_lider', 'administrador']:
            reclutadores = Usuario.query.filter(
                Usuario.rol.in_(['reclutador', 'reclutador_lider']),
                Usuario.activo == True
            ).limit(10).all()
            
            for reclutador in reclutadores:
                r_vacantes = Vacante.query.filter_by(reclutador_id=reclutador.id).count()
                r_candidatos = Candidato.query.filter_by(reclutador_id=reclutador.id).count()
                r_entrevistas = db.session.query(Entrevista).join(Candidato).filter(
                    Candidato.reclutador_id == reclutador.id
                ).count()
                
                # Candidatos aceptados (usando el campo 'aceptado' de CandidatosPositions)
                r_aceptados = db.session.query(CandidatosPositions).join(Candidato).filter(
                    Candidato.reclutador_id == reclutador.id,
                    CandidatosPositions.aceptado == True
                ).count()
                
                efectividad = (r_aceptados / r_candidatos * 100) if r_candidatos > 0 else 0
                
                rendimiento_reclutadores.append({
                    'nombre': reclutador.nombre,
                    'vacantes': r_vacantes,
                    'candidatos': r_candidatos,
                    'entrevistas': r_entrevistas,
                    'aceptados': r_aceptados,
                    'efectividad': round(efectividad, 1)
                })
        
        # 8. Distribuciones simples - SIMPLIFICADO PARA EVITAR ERRORES
        vacantes_por_prioridad = {
            'baja': 0, 'media': 0, 'alta': 0, 'critica': 0
        }
        
        vacantes_por_modalidad = {
            'presencial': 0, 'remoto': 0, 'hibrido': 0
        }
        
        candidatos_por_estado = {
            'postulado': 0, 'en_proceso': 0, 'rechazado': 0, 'aceptado': 0, 'contratado': 0
        }
        
        entrevistas_por_tipo = {
            'telefonica': 0, 'video': 0, 'presencial': 0, 'tecnica': 0, 'operativa': 0, 'definitiva': 0
        }
        
        # Contar de manera simple y segura
        for prioridad in ['baja', 'media', 'alta', 'critica']:
            if current_user.rol == 'reclutador':
                count = Vacante.query.filter_by(
                    reclutador_id=current_user.id, 
                    prioridad=prioridad
                ).count()
            else:
                count = Vacante.query.filter_by(prioridad=prioridad).count()
            vacantes_por_prioridad[prioridad] = count
        
        for modalidad in ['presencial', 'remoto', 'hibrido']:
            if current_user.rol == 'reclutador':
                count = Vacante.query.filter_by(
                    reclutador_id=current_user.id, 
                    modalidad=modalidad
                ).count()
            else:
                count = Vacante.query.filter_by(modalidad=modalidad).count()
            vacantes_por_modalidad[modalidad] = count
        
        for status in ['postulado', 'en_proceso', 'rechazado', 'aceptado', 'contratado']:
            if current_user.rol == 'reclutador':
                count = db.session.query(CandidatosPositions).join(Candidato).filter(
                    Candidato.reclutador_id == current_user.id,
                    CandidatosPositions.status == status
                ).count()
            else:
                count = CandidatosPositions.query.filter_by(status=status).count()
            candidatos_por_estado[status] = count
        
        for tipo in ['telefonica', 'video', 'presencial', 'tecnica', 'operativa', 'definitiva']:
            if current_user.rol == 'reclutador':
                count = db.session.query(Entrevista).join(Candidato).filter(
                    Candidato.reclutador_id == current_user.id,
                    Entrevista.tipo == tipo
                ).count()
            else:
                count = Entrevista.query.filter_by(tipo=tipo).count()
            entrevistas_por_tipo[tipo] = count
        
        # === COMPILAR RESPUESTA SIMPLIFICADA ===
        stats = {
            # Métricas principales
            'total_vacantes': total_vacantes,
            'vacantes_abiertas': vacantes_abiertas,
            'vacantes_cerradas': vacantes_cerradas,
            'vacantes_pausadas': vacantes_pausadas,
            'vacantes_canceladas': vacantes_canceladas,
            
            'total_candidatos': total_candidatos,
            'candidatos_activos': candidatos_activos,
            'candidatos_inactivos': candidatos_inactivos,
            'candidatos_blacklist': candidatos_blacklist,
            
            'total_entrevistas': total_entrevistas,
            'entrevistas_pendientes': entrevistas_pendientes,
            'entrevistas_aprobadas': entrevistas_aprobadas,
            'entrevistas_rechazadas': entrevistas_rechazadas,
            
            # Distribuciones
            'vacantes_por_prioridad': vacantes_por_prioridad,
            'vacantes_por_modalidad': vacantes_por_modalidad,
            'candidatos_por_estado': candidatos_por_estado,
            'entrevistas_por_tipo': entrevistas_por_tipo,
            
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
            'fecha_actualizacion': datetime.utcnow().isoformat(),
            'tipo_usuario': current_user.rol,
            'usuario_nombre': current_user.nombre
        }
        
        print(f"✅ Estadísticas generadas exitosamente para {current_user.nombre}")
        return jsonify(stats), 200
        
    except Exception as e:
        print(f"❌ Error en dashboard: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'message': f'Error obteniendo estadísticas: {str(e)}'}), 500

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
        
        # Candidatos por estado usando consultas simples
        candidatos_por_estado = {}
        for status in ['postulado', 'en_proceso', 'rechazado', 'aceptado', 'contratado']:
            count = CandidatosPositions.query.filter_by(
                vacante_id=vacante_id, 
                status=status
            ).count()
            candidatos_por_estado[status] = count
        
        reporte['resumen']['candidatos_por_estado'] = candidatos_por_estado
        
        # Entrevistas por resultado usando consultas simples
        entrevistas_por_resultado = {}
        for resultado in ['pendiente', 'aprobada', 'rechazada', 'reprogramar']:
            count = Entrevista.query.filter_by(
                vacante_id=vacante_id, 
                resultado=resultado
            ).count()
            entrevistas_por_resultado[resultado] = count
        
        reporte['resumen']['entrevistas_por_resultado'] = entrevistas_por_resultado
        
        # Lista de candidatos con detalles - SIMPLIFICADO
        candidatos_detalle = []
        candidatos_posiciones = CandidatosPositions.query.filter_by(vacante_id=vacante_id).all()
        
        for cp in candidatos_posiciones:
            candidato_dict = cp.candidato.to_dict()
            candidato_dict.update({
                'status_vacante': cp.status,
                'nota_vacante': cp.nota_reclutador,
                'aceptado': cp.aceptado,
                'contratado_status': cp.contratado_status,
                'fecha_asignacion': cp.fecha_asignacion.isoformat() if cp.fecha_asignacion else None,
                'fecha_envio_candidato': cp.fecha_envio_candidato.isoformat() if cp.fecha_envio_candidato else None,
                'fecha_entrevista_ejecutivo': cp.fecha_entrevista_ejecutivo.isoformat() if cp.fecha_entrevista_ejecutivo else None,
                'fecha_decision_final': cp.fecha_decision_final.isoformat() if cp.fecha_decision_final else None
            })
            
            # Agregar entrevistas para esta vacante
            entrevistas_candidato = Entrevista.query.filter_by(
                candidato_id=cp.candidato_id,
                vacante_id=vacante_id
            ).all()
            
            candidato_dict['entrevistas'] = [e.to_dict() for e in entrevistas_candidato]
            candidatos_detalle.append(candidato_dict)
        
        reporte['candidatos'] = candidatos_detalle
        
        return jsonify(reporte), 200
        
    except Exception as e:
        print(f"❌ Error en reporte de vacante: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'message': f'Error generando reporte: {str(e)}'}), 500

# === ENDPOINT ADICIONAL PARA ESTADÍSTICAS DE USUARIOS ===
@reports_bp.route('/usuarios/estadisticas', methods=['GET'])
@role_required('ejecutivo', 'reclutador_lider', 'administrador')
def get_user_stats(current_user):
    try:
        # Estadísticas generales de usuarios
        total_usuarios = Usuario.query.filter_by(activo=True).count()
        usuarios_inactivos = Usuario.query.filter_by(activo=False).count()
        
        # Usuarios por rol - SIMPLIFICADO
        usuarios_por_rol = {}
        for rol in ['ejecutivo', 'reclutador', 'reclutador_lider', 'administrador']:
            count = Usuario.query.filter_by(rol=rol, activo=True).count()
            usuarios_por_rol[rol] = count
        
        # Usuarios creados en los últimos 30 días
        fecha_limite = datetime.utcnow() - timedelta(days=30)
        usuarios_recientes = Usuario.query.filter(
            Usuario.fecha_creacion >= fecha_limite,
            Usuario.activo == True
        ).count()
        
        # Actividad por reclutador (últimos 30 días) - SIMPLIFICADO
        actividad_reclutadores = []
        reclutadores = Usuario.query.filter(
            Usuario.rol.in_(['reclutador', 'reclutador_lider']),
            Usuario.activo == True
        ).all()
        
        for reclutador in reclutadores:
            candidatos_mes = Candidato.query.filter(
                Candidato.reclutador_id == reclutador.id,
                Candidato.fecha_creacion >= fecha_limite
            ).count()
            
            entrevistas_mes = db.session.query(Entrevista).join(Candidato).filter(
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
        
        # Ordenar por actividad total
        actividad_reclutadores.sort(
            key=lambda x: x['candidatos_mes'] + x['entrevistas_mes'], 
            reverse=True
        )
        
        stats = {
            'total_usuarios': total_usuarios,
            'usuarios_inactivos': usuarios_inactivos,
            'usuarios_por_rol': usuarios_por_rol,
            'usuarios_recientes': usuarios_recientes,
            'actividad_reclutadores': actividad_reclutadores,
            'fecha_actualizacion': datetime.utcnow().isoformat()
        }
        
        return jsonify(stats), 200
        
    except Exception as e:
        print(f"❌ Error en estadísticas de usuarios: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'message': f'Error obteniendo estadísticas de usuarios: {str(e)}'}), 500
