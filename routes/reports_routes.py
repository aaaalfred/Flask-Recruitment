from flask import Blueprint, request, jsonify
from services.auth_service import token_required, role_required
from models import Vacante, Candidato, Entrevista, CandidatosPositions, Usuario, Cliente, db
from sqlalchemy import func, desc, case, text
from datetime import datetime, timedelta

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/dashboard', methods=['GET'])
@token_required
def get_dashboard_stats(current_user):
    try:
        print(f"🔍 Generando estadísticas mejoradas para: {current_user.nombre} ({current_user.rol})")
        
        # === ESTADÍSTICAS PRINCIPALES (SIN COMPLICACIONES) ===
        
        # Vacantes con filtros por rol - SIMPLIFICADO
        print("📊 Calculando vacantes...")
        if current_user.rol == 'reclutador':
            total_vacantes = db.session.query(func.count(Vacante.id)).filter(Vacante.reclutador_id == current_user.id).scalar()
            vacantes_abiertas = db.session.query(func.count(Vacante.id)).filter(
                Vacante.reclutador_id == current_user.id,
                Vacante.estado == 'abierta'
            ).scalar()
        elif current_user.rol == 'ejecutivo':
            total_vacantes = db.session.query(func.count(Vacante.id)).filter(Vacante.ejecutivo_id == current_user.id).scalar()
            vacantes_abiertas = db.session.query(func.count(Vacante.id)).filter(
                Vacante.ejecutivo_id == current_user.id,
                Vacante.estado == 'abierta'
            ).scalar()
        else:
            total_vacantes = db.session.query(func.count(Vacante.id)).scalar()
            vacantes_abiertas = db.session.query(func.count(Vacante.id)).filter(Vacante.estado == 'abierta').scalar()
        
        print(f"✅ Vacantes calculadas: {total_vacantes} total, {vacantes_abiertas} abiertas")
        
        # Candidatos con filtros por rol - SIMPLIFICADO
        print("👥 Calculando candidatos...")
        if current_user.rol == 'reclutador':
            total_candidatos = db.session.query(func.count(Candidato.id)).filter(Candidato.reclutador_id == current_user.id).scalar()
        elif current_user.rol == 'ejecutivo':
            # Para ejecutivos: candidatos de sus vacantes
            total_candidatos = db.session.query(func.count(Candidato.id.distinct())).join(
                CandidatosPositions, Candidato.id == CandidatosPositions.candidato_id
            ).join(
                Vacante, CandidatosPositions.vacante_id == Vacante.id
            ).filter(Vacante.ejecutivo_id == current_user.id).scalar()
        else:
            total_candidatos = db.session.query(func.count(Candidato.id)).scalar()
        
        print(f"✅ Candidatos calculados: {total_candidatos}")
        
        # Entrevistas - SIMPLIFICADO
        print("📅 Calculando entrevistas...")
        if current_user.rol == 'reclutador':
            total_entrevistas = db.session.query(func.count(Entrevista.id)).join(
                Candidato, Entrevista.candidato_id == Candidato.id
            ).filter(Candidato.reclutador_id == current_user.id).scalar()
            
            entrevistas_pendientes = db.session.query(func.count(Entrevista.id)).join(
                Candidato, Entrevista.candidato_id == Candidato.id
            ).filter(
                Candidato.reclutador_id == current_user.id,
                Entrevista.resultado == 'pendiente'
            ).scalar()
        elif current_user.rol == 'ejecutivo':
            total_entrevistas = db.session.query(func.count(Entrevista.id)).join(
                Vacante, Entrevista.vacante_id == Vacante.id
            ).filter(Vacante.ejecutivo_id == current_user.id).scalar()
            
            entrevistas_pendientes = db.session.query(func.count(Entrevista.id)).join(
                Vacante, Entrevista.vacante_id == Vacante.id
            ).filter(
                Vacante.ejecutivo_id == current_user.id,
                Entrevista.resultado == 'pendiente'
            ).scalar()
        else:
            total_entrevistas = db.session.query(func.count(Entrevista.id)).scalar()
            entrevistas_pendientes = db.session.query(func.count(Entrevista.id)).filter(Entrevista.resultado == 'pendiente').scalar()
        
        print(f"✅ Entrevistas calculadas: {total_entrevistas} total, {entrevistas_pendientes} pendientes")
        
        # Métricas adicionales básicas
        print("📈 Calculando métricas adicionales...")
        
        # Usando queries SQL más simples para evitar errores de atributos
        try:
            if current_user.rol == 'reclutador':
                vacantes_cubiertas = db.session.execute(text("""
                    SELECT COUNT(*) FROM vacante 
                    WHERE reclutador_id = :user_id AND status_final = 'cubierta'
                """), {'user_id': current_user.id}).scalar()
            elif current_user.rol == 'ejecutivo':
                vacantes_cubiertas = db.session.execute(text("""
                    SELECT COUNT(*) FROM vacante 
                    WHERE ejecutivo_id = :user_id AND status_final = 'cubierta'
                """), {'user_id': current_user.id}).scalar()
            else:
                vacantes_cubiertas = db.session.execute(text("""
                    SELECT COUNT(*) FROM vacante WHERE status_final = 'cubierta'
                """)).scalar()
        except Exception as e:
            print(f"⚠️ Error calculando vacantes cubiertas: {e}")
            vacantes_cubiertas = 0
        
        print(f"✅ Vacantes cubiertas: {vacantes_cubiertas}")
        
        # Candidatos aceptados - usando SQL directo para evitar errores
        try:
            if current_user.rol == 'reclutador':
                candidatos_aceptados = db.session.execute(text("""
                    SELECT COUNT(*) FROM candidatos_posiciones cp
                    JOIN candidato c ON cp.candidato_id = c.id
                    WHERE c.reclutador_id = :user_id AND cp.aceptado = 1
                """), {'user_id': current_user.id}).scalar()
            elif current_user.rol == 'ejecutivo':
                candidatos_aceptados = db.session.execute(text("""
                    SELECT COUNT(*) FROM candidatos_posiciones cp
                    JOIN vacante v ON cp.vacante_id = v.id
                    WHERE v.ejecutivo_id = :user_id AND cp.aceptado = 1
                """), {'user_id': current_user.id}).scalar()
            else:
                candidatos_aceptados = db.session.execute(text("""
                    SELECT COUNT(*) FROM candidatos_posiciones WHERE aceptado = 1
                """)).scalar()
        except Exception as e:
            print(f"⚠️ Error calculando candidatos aceptados: {e}")
            candidatos_aceptados = 0
        
        print(f"✅ Candidatos aceptados: {candidatos_aceptados}")
        
        # Actividad reciente (simplificada)
        fecha_limite_7_dias = datetime.utcnow() - timedelta(days=7)
        
        try:
            candidatos_recientes = db.session.query(func.count(Candidato.id)).filter(
                Candidato.fecha_creacion >= fecha_limite_7_dias
            ).scalar() or 0
            
            entrevistas_recientes = db.session.query(func.count(Entrevista.id)).filter(
                Entrevista.fecha >= fecha_limite_7_dias
            ).scalar() or 0
            
            vacantes_recientes = db.session.query(func.count(Vacante.id)).filter(
                Vacante.fecha_solicitud >= fecha_limite_7_dias
            ).scalar() or 0
        except Exception as e:
            print(f"⚠️ Error calculando actividad reciente: {e}")
            candidatos_recientes = entrevistas_recientes = vacantes_recientes = 0
        
        # === DISTRIBUCIONES BÁSICAS ===
        candidatos_por_status = {}
        candidatos_por_contratacion = {}
        vacantes_por_prioridad = {}
        vacantes_por_modalidad = {}
        entrevistas_por_tipo = {}
        
        try:
            # Candidatos por status usando SQL directo
            if current_user.rol == 'reclutador':
                status_results = db.session.execute(text("""
                    SELECT cp.status, COUNT(*) as count 
                    FROM candidatos_posiciones cp
                    JOIN candidato c ON cp.candidato_id = c.id
                    WHERE c.reclutador_id = :user_id
                    GROUP BY cp.status
                """), {'user_id': current_user.id}).fetchall()
            elif current_user.rol == 'ejecutivo':
                status_results = db.session.execute(text("""
                    SELECT cp.status, COUNT(*) as count 
                    FROM candidatos_posiciones cp
                    JOIN vacante v ON cp.vacante_id = v.id
                    WHERE v.ejecutivo_id = :user_id
                    GROUP BY cp.status
                """), {'user_id': current_user.id}).fetchall()
            else:
                status_results = db.session.execute(text("""
                    SELECT status, COUNT(*) as count 
                    FROM candidatos_posiciones 
                    GROUP BY status
                """)).fetchall()
            
            candidatos_por_status = {row[0]: row[1] for row in status_results}
            
        except Exception as e:
            print(f"⚠️ Error calculando distribuciones: {e}")
        
        # === RESPUESTA FINAL SIMPLIFICADA ===
        stats = {
            # Métricas principales
            'total_vacantes': total_vacantes or 0,
            'vacantes_abiertas': vacantes_abiertas or 0,
            'vacantes_cerradas': 0,  # Calculamos después si es necesario
            'vacantes_pausadas': 0,
            'vacantes_canceladas': 0,
            'vacantes_cubiertas': vacantes_cubiertas or 0,
            
            'total_candidatos': total_candidatos or 0,
            'candidatos_activos': total_candidatos or 0,  # Simplificado
            'candidatos_inactivos': 0,
            'candidatos_blacklist': 0,
            
            'total_entrevistas': total_entrevistas or 0,
            'entrevistas_pendientes': entrevistas_pendientes or 0,
            'entrevistas_aprobadas': 0,
            'entrevistas_rechazadas': 0,
            
            # Métricas de proceso
            'candidatos_por_status': candidatos_por_status,
            'candidatos_por_contratacion': candidatos_por_contratacion,
            'candidatos_aceptados_supervisor': candidatos_aceptados or 0,
            
            # Distribuciones
            'vacantes_por_prioridad': vacantes_por_prioridad,
            'vacantes_por_modalidad': vacantes_por_modalidad,
            'entrevistas_por_tipo': entrevistas_por_tipo,
            
            # Métricas de rendimiento
            'tiempo_promedio_resolucion': 0,  # Calculamos después
            'tasa_conversion_global': round((candidatos_aceptados / total_candidatos * 100), 1) if total_candidatos > 0 else 0,
            
            # Actividad reciente
            'candidatos_recientes': candidatos_recientes,
            'entrevistas_recientes': entrevistas_recientes,
            'vacantes_recientes': vacantes_recientes,
            
            # Análisis por cliente (vacío por ahora)
            'clientes_stats': [],
            
            # Alertas y atención (vacío por ahora)
            'vacantes_antiguas': [],
            
            # Rendimiento del equipo (vacío por ahora)
            'rendimiento_reclutadores': [],
            
            # Usuarios (vacío por ahora)
            'usuarios': {},
            
            # Metadatos
            'fecha_actualizacion': datetime.utcnow().isoformat(),
            'tipo_usuario': current_user.rol,
            'usuario_nombre': current_user.nombre,
            'filtrado_por_reclutador': current_user.rol == 'reclutador'
        }
        
        print(f"✅ Estadísticas generadas exitosamente para {current_user.nombre}")
        print(f"📊 Resumen: {total_vacantes} vacantes, {total_candidatos} candidatos, {total_entrevistas} entrevistas")
        
        return jsonify(stats), 200
        
    except Exception as e:
        print(f"❌ Error en dashboard: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'message': f'Error obteniendo estadísticas: {str(e)}',
            'error_type': type(e).__name__,
            'debug_info': 'Versión simplificada del dashboard'
        }), 500
