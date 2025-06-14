#!/usr/bin/env python3
"""
Script corregido para sincronizar con el flujo real de candidatos
Recreando tablas completamente para evitar problemas de columnas
"""

from app import create_app
from extensions import db
from datetime import datetime, timedelta
import random

def recreate_database():
    """Recrear completamente la base de datos con la nueva estructura"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🔄 RECREANDO BASE DE DATOS COMPLETAMENTE")
            print("=" * 50)
            
            # Importar todos los modelos para asegurar que están disponibles
            from models import Usuario, Vacante, Candidato, Documento, Entrevista, CandidatosPositions
            
            # Eliminar todas las tablas
            print("🗑️  Eliminando tablas existentes...")
            db.drop_all()
            
            # Recrear todas las tablas con la nueva estructura
            print("🔨 Creando nuevas tablas...")
            db.create_all()
            
            print("✅ Base de datos recreada exitosamente!")
            return True
            
        except Exception as e:
            print(f"❌ Error recreando base de datos: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

def create_users():
    """Crear usuarios del sistema"""
    app = create_app()
    
    with app.app_context():
        try:
            from models import Usuario
            
            print("\n👥 CREANDO USUARIOS")
            print("=" * 30)
            
            usuarios_base = [
                {'nombre': 'Administrador Sistema', 'email': 'admin@empresa.com', 'rol': 'ejecutivo'},
                {'nombre': 'Alfredo Ambriz', 'email': 'alfredo.ambriz@empresa.com', 'rol': 'ejecutivo'},
                {'nombre': 'Sofia Rueda', 'email': 'sofia.rueda@empresa.com', 'rol': 'ejecutivo'},
                {'nombre': 'diego erandi quintanar contreras', 'email': 'diego.quintanar@empresa.com', 'rol': 'reclutador'},
                {'nombre': 'Erick Cervantes', 'email': 'erick.cervantes@empresa.com', 'rol': 'reclutador'},
                {'nombre': 'Fernanda Moreno', 'email': 'fernanda.moreno@empresa.com', 'rol': 'reclutador_lider'}
            ]
            
            for user_data in usuarios_base:
                new_user = Usuario(
                    nombre=user_data['nombre'],
                    email=user_data['email'],
                    rol=user_data['rol']
                )
                new_user.set_password('password123')
                db.session.add(new_user)
                print(f"   ✅ {user_data['nombre']} ({user_data['rol']})")
            
            db.session.commit()
            print(f"\n📊 Total usuarios creados: {Usuario.query.count()}")
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error creando usuarios: {str(e)}")
            return False

def create_vacantes():
    """Crear vacantes con la nueva estructura"""
    app = create_app()
    
    with app.app_context():
        try:
            from models import Usuario, Vacante
            
            print("\n📋 CREANDO VACANTES")
            print("=" * 30)
            
            # Obtener usuarios
            alfredo = Usuario.query.filter_by(email='alfredo.ambriz@empresa.com').first()
            sofia = Usuario.query.filter_by(email='sofia.rueda@empresa.com').first()
            diego = Usuario.query.filter_by(email='diego.quintanar@empresa.com').first()
            erick = Usuario.query.filter_by(email='erick.cervantes@empresa.com').first()
            fernanda = Usuario.query.filter_by(email='fernanda.moreno@empresa.com').first()
            
            vacantes_reales = [
                {
                    'nombre': '2210 ACC FELIX CUEVAS',
                    'descripcion': 'Posición para centro comercial Felix Cuevas',
                    'ejecutivo': alfredo,
                    'reclutador': diego,
                    'reclutador_lider': fernanda,
                    'dias_atras': 54,
                    'ubicacion': 'Felix Cuevas, CDMX'
                },
                {
                    'nombre': '2120 ACC CANCUN',
                    'descripcion': 'Posición para centro comercial Cancún',
                    'ejecutivo': sofia,
                    'reclutador': erick,
                    'reclutador_lider': fernanda,
                    'dias_atras': 80,
                    'ubicacion': 'Cancún, QR'
                },
                {
                    'nombre': '2121 ASESORA MONTERREY',
                    'descripcion': 'Posición de asesora en Monterrey',
                    'ejecutivo': sofia,
                    'reclutador': erick,
                    'reclutador_lider': fernanda,
                    'dias_atras': 90,
                    'ubicacion': 'Monterrey, NL'
                },
                {
                    'nombre': '2136 ACC LEON',
                    'descripcion': 'Posición para centro comercial León',
                    'ejecutivo': alfredo,
                    'reclutador': erick,
                    'reclutador_lider': fernanda,
                    'dias_atras': 120,
                    'ubicacion': 'León, GTO'
                }
            ]
            
            for vacante_data in vacantes_reales:
                fecha_solicitud = datetime.now() - timedelta(days=vacante_data['dias_atras'])
                
                nueva_vacante = Vacante(
                    nombre=vacante_data['nombre'],
                    descripcion=vacante_data['descripcion'],
                    ejecutivo_id=vacante_data['ejecutivo'].id,
                    reclutador_id=vacante_data['reclutador'].id,
                    reclutador_lider_id=vacante_data['reclutador_lider'].id,
                    fecha_solicitud=fecha_solicitud,
                    candidatos_requeridos=3,
                    entrevistas_op=3,
                    vacantes=1,
                    avance='En proceso',
                    status_final='cubierta',  # Según los datos, todas están cubiertas
                    ubicacion=vacante_data['ubicacion'],
                    estado='cerrada',
                    prioridad='media'
                )
                
                # Calcular días transcurridos
                nueva_vacante.dias_transcurridos = vacante_data['dias_atras']
                
                # Generar resumen (sin acceder a relaciones aún)
                nueva_vacante.resumen_ia = f"Vacante {nueva_vacante.nombre} en {nueva_vacante.ubicacion}. " \
                                          f"Días transcurridos: {nueva_vacante.dias_transcurridos}."
                
                db.session.add(nueva_vacante)
                print(f"   ✅ {vacante_data['nombre']}")
            
            db.session.commit()
            
            # Ahora actualizar los resúmenes con información completa
            print("\n🔄 Actualizando resúmenes con información completa...")
            for vacante in Vacante.query.all():
                vacante.resumen_ia = f"Vacante {vacante.nombre} en {vacante.ubicacion}. " \
                                   f"Ejecutivo: {vacante.ejecutivo.nombre}. " \
                                   f"Reclutador: {vacante.reclutador.nombre}. " \
                                   f"Días transcurridos: {vacante.dias_transcurridos}."
            
            db.session.commit()
            print(f"\n📊 Total vacantes creadas: {Vacante.query.count()}")
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error creando vacantes: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

def create_candidatos():
    """Crear candidatos"""
    app = create_app()
    
    with app.app_context():
        try:
            from models import Usuario, Candidato
            
            print("\n👤 CREANDO CANDIDATOS")
            print("=" * 30)
            
            # Obtener reclutadores
            diego = Usuario.query.filter_by(email='diego.quintanar@empresa.com').first()
            erick = Usuario.query.filter_by(email='erick.cervantes@empresa.com').first()
            fernanda = Usuario.query.filter_by(email='fernanda.moreno@empresa.com').first()
            
            candidatos_reales = [
                {
                    'nombre': 'ALEJANDRA ALARCON DE LA CRUZ',
                    'email': 'alejandra.alarcon@email.com',
                    'reclutador': erick,
                    'telefono': '+52 998 123 4567'
                },
                {
                    'nombre': 'ALICIA RODRIGUEZ VELEZ',
                    'email': 'alicia.rodriguez@email.com',
                    'reclutador': erick,
                    'telefono': '+52 81 234 5678'
                },
                {
                    'nombre': 'ADELA CAMPOS GUERRERO',
                    'email': 'adela.campos@email.com',
                    'reclutador': erick,
                    'telefono': '+52 477 345 6789'
                },
                {
                    'nombre': 'ADRIANA PILAR MORENO MARTINEZ',
                    'email': 'adriana.moreno@email.com',
                    'reclutador': fernanda,
                    'telefono': '+52 55 456 7890'
                }
            ]
            
            for candidato_data in candidatos_reales:
                nuevo_candidato = Candidato(
                    nombre=candidato_data['nombre'],
                    email=candidato_data['email'],
                    reclutador_id=candidato_data['reclutador'].id,
                    telefono=candidato_data['telefono'],
                    estado='activo',
                    disponibilidad='inmediata',
                    experiencia_anos=random.randint(1, 5),
                    ubicacion='México'
                )
                db.session.add(nuevo_candidato)
                print(f"   ✅ {candidato_data['nombre']}")
            
            db.session.commit()
            print(f"\n📊 Total candidatos creados: {Candidato.query.count()}")
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error creando candidatos: {str(e)}")
            return False

def create_asignaciones():
    """Crear asignaciones candidato-vacante con datos reales"""
    app = create_app()
    
    with app.app_context():
        try:
            from models import Candidato, Vacante, CandidatosPositions
            
            print("\n🔗 CREANDO ASIGNACIONES CANDIDATO-VACANTE")
            print("=" * 50)
            
            # Asignaciones basadas en los datos reales
            asignaciones_reales = [
                {
                    'candidato_email': 'alejandra.alarcon@email.com',
                    'vacante_nombre': '2120 ACC CANCUN',
                    'aceptado': False,
                    'contratado_status': 'rechazado',
                    'comentarios_finales': 'CANDIDATA DESCARTA POR NO CONTAR CON EXPERIENCIA EN AUTOSERVICIO',
                    'archivo_cv': 'CV_2_(5).pdf',
                    'status': 'rechazado'
                },
                {
                    'candidato_email': 'alicia.rodriguez@email.com',
                    'vacante_nombre': '2121 ASESORA MONTERREY',
                    'aceptado': True,  # Fue aceptada por supervisor
                    'contratado_status': 'rechazado',
                    'comentarios_finales': 'CANDIDATA ACEPTADA POR SUPERVISOR, PERO NO SE PRESENTO A TIENDA',
                    'archivo_cv': 'Alicia_Rodriguez_Velez.pdf',
                    'se_presento': False,
                    'status': 'rechazado'
                },
                {
                    'candidato_email': 'adela.campos@email.com',
                    'vacante_nombre': '2136 ACC LEON',
                    'aceptado': False,
                    'contratado_status': 'rechazado',
                    'comentarios_finales': 'CANDIDATA NO CONTESTO LLAMADAS Y MENSAJES PARA LLEVAR A CABO ENTREVISTA CON EJECUTIVO',
                    'archivo_cv': 'CVAdelaCampos.pdf',
                    'status': 'rechazado'
                },
                {
                    'candidato_email': 'adriana.moreno@email.com',
                    'vacante_nombre': '2136 ACC LEON',  # Misma vacante
                    'aceptado': True,
                    'contratado_status': 'no_contratable',
                    'comentarios_finales': 'CANDIDATA ACEPTADA POR SUPERVISOR, PERO NO SE PRESENTO A TIENDA',
                    'archivo_cv': 'ADRIANA_PILAR_MORENO_MTZ.pdf',
                    'se_presento': False,
                    'status': 'rechazado'
                }
            ]
            
            for asignacion_data in asignaciones_reales:
                candidato = Candidato.query.filter_by(email=asignacion_data['candidato_email']).first()
                vacante = Vacante.query.filter_by(nombre=asignacion_data['vacante_nombre']).first()
                
                if candidato and vacante:
                    nueva_asignacion = CandidatosPositions(
                        candidato_id=candidato.id,
                        vacante_id=vacante.id,
                        status=asignacion_data['status'],
                        aceptado=asignacion_data['aceptado'],
                        contratado_status=asignacion_data['contratado_status'],
                        comentarios_finales=asignacion_data['comentarios_finales'],
                        archivo_cv=asignacion_data['archivo_cv'],
                        se_presento=asignacion_data.get('se_presento', True),
                        fecha_asignacion=vacante.fecha_solicitud + timedelta(days=random.randint(1, 10)),
                        fecha_decision_final=datetime.now() - timedelta(days=random.randint(1, 30))
                    )
                    db.session.add(nueva_asignacion)
                    print(f"   ✅ {candidato.nombre} → {vacante.nombre}")
                else:
                    print(f"   ❌ No se encontró candidato o vacante para: {asignacion_data['candidato_email']} → {asignacion_data['vacante_nombre']}")
            
            db.session.commit()
            print(f"\n📊 Total asignaciones creadas: {CandidatosPositions.query.count()}")
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error creando asignaciones: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

def show_final_stats():
    """Mostrar estadísticas finales"""
    app = create_app()
    
    with app.app_context():
        try:
            from models import Usuario, Vacante, Candidato, CandidatosPositions
            
            print("\n📊 ESTADÍSTICAS FINALES")
            print("=" * 40)
            
            print(f"👥 Usuarios: {Usuario.query.count()}")
            print(f"📋 Vacantes: {Vacante.query.count()}")
            print(f"👤 Candidatos: {Candidato.query.count()}")
            print(f"🔗 Asignaciones: {CandidatosPositions.query.count()}")
            
            # Estadísticas por status
            print("\n📈 Por estado de contratación:")
            from sqlalchemy import func
            stats = db.session.query(
                CandidatosPositions.contratado_status,
                func.count(CandidatosPositions.id)
            ).group_by(CandidatosPositions.contratado_status).all()
            
            for status, count in stats:
                print(f"   {status}: {count}")
            
            # Estadísticas de aceptados
            aceptados = CandidatosPositions.query.filter_by(aceptado=True).count()
            no_presentados = CandidatosPositions.query.filter_by(se_presento=False).count()
            
            print(f"\n✅ Aceptados por supervisor: {aceptados}")
            print(f"❌ No se presentaron: {no_presentados}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error mostrando estadísticas: {str(e)}")
            return False

def main():
    """Función principal"""
    print("🎯 SINCRONIZACIÓN COMPLETA CON FLUJO REAL")
    print("🔄 Recreando base de datos desde cero")
    print("=" * 55)
    
    steps = [
        ("Recrear base de datos", recreate_database),
        ("Crear usuarios", create_users),
        ("Crear vacantes", create_vacantes),
        ("Crear candidatos", create_candidatos),
        ("Crear asignaciones", create_asignaciones),
        ("Mostrar estadísticas", show_final_stats)
    ]
    
    for step_name, step_func in steps:
        print(f"\n🔹 {step_name}...")
        if not step_func():
            print(f"❌ Error en: {step_name}")
            return False
    
    print("\n🎉 ¡SINCRONIZACIÓN COMPLETADA EXITOSAMENTE!")
    print("=" * 55)
    print("✅ El sistema ahora refleja el flujo real de candidatos")
    print("✅ Datos de ejemplo basados en casos reales")
    print("✅ Estados y comentarios del proceso real")
    
    print("\n🔑 CREDENCIALES DE ACCESO:")
    print("admin@empresa.com / password123 (Admin)")
    print("alfredo.ambriz@empresa.com / password123 (Ejecutivo)")
    print("erick.cervantes@empresa.com / password123 (Reclutador)")
    print("fernanda.moreno@empresa.com / password123 (Reclutador Líder)")
    
    return True

if __name__ == '__main__':
    main()
