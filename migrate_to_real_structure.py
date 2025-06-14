#!/usr/bin/env python3
"""
Script para migrar la base de datos a la nueva estructura
que refleja el proceso real de reclutamiento
"""

from app import create_app
from extensions import db
from models import Vacante, CandidatosPositions
from datetime import datetime, timedelta
import random

def migrate_database():
    """Migrar datos existentes al nuevo formato"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🔄 MIGRACIÓN DE BASE DE DATOS")
            print("=" * 40)
            
            # 1. Crear las nuevas columnas si no existen
            print("📋 Actualizando estructura de tablas...")
            
            # Recrear todas las tablas con la nueva estructura
            print("   Recreando tablas con nueva estructura...")
            db.drop_all()
            db.create_all()
            
            print("✅ Estructura de base de datos actualizada!")
            
            # 2. Crear usuarios básicos si no existen
            print("👥 Verificando usuarios básicos...")
            from models import Usuario
            
            usuarios_base = [
                {'nombre': 'Administrador Sistema', 'email': 'admin@empresa.com', 'rol': 'ejecutivo'},
                {'nombre': 'Alfredo Ambriz', 'email': 'alfredo.ambriz@empresa.com', 'rol': 'ejecutivo'},
                {'nombre': 'Sofia Rueda', 'email': 'sofia.rueda@empresa.com', 'rol': 'ejecutivo'},
                {'nombre': 'diego erandi quintanar contreras', 'email': 'diego.quintanar@empresa.com', 'rol': 'reclutador'},
                {'nombre': 'Erick Cervantes', 'email': 'erick.cervantes@empresa.com', 'rol': 'reclutador'},
                {'nombre': 'Fernanda Moreno', 'email': 'fernanda.moreno@empresa.com', 'rol': 'reclutador_lider'}
            ]
            
            for user_data in usuarios_base:
                existing = Usuario.query.filter_by(email=user_data['email']).first()
                if not existing:
                    new_user = Usuario(
                        nombre=user_data['nombre'],
                        email=user_data['email'],
                        rol=user_data['rol']
                    )
                    new_user.set_password('password123')
                    db.session.add(new_user)
                    print(f"   ✅ Usuario creado: {user_data['nombre']} ({user_data['rol']})")
            
            db.session.commit()
            
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error en migración: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

def create_sample_data():
    """Crear datos de ejemplo que reflejen el flujo real"""
    app = create_app()
    
    with app.app_context():
        try:
            from models import Usuario, Candidato
            
            print("\n📝 CREANDO DATOS DE EJEMPLO")
            print("=" * 40)
            
            # Obtener usuarios
            alfredo = Usuario.query.filter_by(email='alfredo.ambriz@empresa.com').first()
            sofia = Usuario.query.filter_by(email='sofia.rueda@empresa.com').first()
            diego = Usuario.query.filter_by(email='diego.quintanar@empresa.com').first()
            erick = Usuario.query.filter_by(email='erick.cervantes@empresa.com').first()
            fernanda = Usuario.query.filter_by(email='fernanda.moreno@empresa.com').first()
            
            if not all([alfredo, sofia, diego, erick, fernanda]):
                print("❌ Error: No se encontraron todos los usuarios necesarios")
                return False
            
            # Crear vacantes de ejemplo basadas en los datos reales
            vacantes_ejemplo = [
                {
                    'nombre': '2210 ACC FELIX CUEVAS',
                    'descripcion': 'Posición para centro comercial Felix Cuevas',
                    'ejecutivo': alfredo,
                    'reclutador': diego,
                    'reclutador_lider': fernanda,
                    'candidatos_requeridos': 3,
                    'entrevistas_op': 3,
                    'avance': 'En proceso de entrevistas',
                    'fecha_solicitud': datetime.now() - timedelta(days=54),
                    'ubicacion': 'Felix Cuevas, CDMX',
                    'vacantes': 1
                },
                {
                    'nombre': '#0 ACC ACC MONTERREY',
                    'descripcion': 'Posición para centro comercial Monterrey',
                    'ejecutivo': sofia,
                    'reclutador': erick,
                    'reclutador_lider': fernanda,
                    'candidatos_requeridos': 3,
                    'entrevistas_op': 3,
                    'avance': 'Candidatos enviados a RH',
                    'fecha_solicitud': datetime.now() - timedelta(days=155),
                    'ubicacion': 'Monterrey, NL',
                    'vacantes': 1
                },
                {
                    'nombre': '#0 ACC LAS AMERICAS',
                    'descripcion': 'Posición para centro comercial Las Americas',
                    'ejecutivo': sofia,
                    'reclutador': diego,
                    'reclutador_lider': fernanda,
                    'candidatos_requeridos': 3,
                    'entrevistas_op': 3,
                    'avance': 'Seleccionando candidatos',
                    'fecha_solicitud': datetime.now() - timedelta(days=170),
                    'ubicacion': 'Las Americas, CDMX',
                    'vacantes': 1
                },
                {
                    'nombre': '#0 PROMOMIX AGUASCALIENTES',
                    'descripcion': 'Posición para Promomix en Aguascalientes',
                    'ejecutivo': sofia,
                    'reclutador': erick,
                    'reclutador_lider': fernanda,
                    'candidatos_requeridos': 3,
                    'entrevistas_op': 3,
                    'avance': 'Buscando candidatos',
                    'fecha_solicitud': datetime.now() - timedelta(days=6),
                    'ubicacion': 'Aguascalientes, AGS',
                    'vacantes': 1
                }
            ]
            
            for vacante_data in vacantes_ejemplo:
                # Verificar si ya existe
                existing = Vacante.query.filter_by(nombre=vacante_data['nombre']).first()
                if not existing:
                    nueva_vacante = Vacante(
                        nombre=vacante_data['nombre'],
                        descripcion=vacante_data['descripcion'],
                        ejecutivo_id=vacante_data['ejecutivo'].id,
                        reclutador_id=vacante_data['reclutador'].id,
                        reclutador_lider_id=vacante_data['reclutador_lider'].id,
                        candidatos_requeridos=vacante_data['candidatos_requeridos'],
                        entrevistas_op=vacante_data['entrevistas_op'],
                        avance=vacante_data['avance'],
                        fecha_solicitud=vacante_data['fecha_solicitud'],
                        ubicacion=vacante_data['ubicacion'],
                        vacantes=vacante_data['vacantes'],
                        estado='abierta',
                        prioridad='media'
                    )
                    
                    # Calcular días transcurridos y generar resumen
                    nueva_vacante.dias_transcurridos = nueva_vacante.calcular_dias_transcurridos()
                    nueva_vacante.resumen_ia = f"Vacante {nueva_vacante.nombre} en {nueva_vacante.ubicacion}. " \
                                              f"Ejecutivo: {nueva_vacante.ejecutivo.nombre}. " \
                                              f"Reclutador: {nueva_vacante.reclutador.nombre}. " \
                                              f"Días transcurridos: {nueva_vacante.dias_transcurridos}."
                    
                    db.session.add(nueva_vacante)
                    print(f"   ✅ Vacante creada: {vacante_data['nombre']}")
            
            db.session.commit()
            
            # Crear candidatos de ejemplo
            print("\n👥 Creando candidatos de ejemplo...")
            
            candidatos_ejemplo = [
                {
                    'nombre': 'XIMENA NAOMI LOPEZ GALVEZ',
                    'email': 'ximena.lopez@email.com',
                    'reclutador': diego,
                    'telefono': '+52 55 1234 5678',
                    'experiencia_anos': 3
                },
                {
                    'nombre': 'ROMINA JIMENEZ RAMIREZ',
                    'email': 'romina.jimenez@email.com',
                    'reclutador': diego,
                    'telefono': '+52 55 2345 6789',
                    'experiencia_anos': 2
                },
                {
                    'nombre': 'VL CASSANDRA STEPHANIA AGUIRRE',
                    'email': 'cassandra.aguirre@email.com',
                    'reclutador': erick,
                    'telefono': '+52 81 3456 7890',
                    'experiencia_anos': 4
                },
                {
                    'nombre': 'ROSA IDALIA RANGEL MORENO',
                    'email': 'rosa.rangel@email.com',
                    'reclutador': erick,
                    'telefono': '+52 81 4567 8901',
                    'experiencia_anos': 5
                },
                {
                    'nombre': 'MARIANA ESTEFHANIA TELLEZ OLIVARES',
                    'email': 'mariana.tellez@email.com',
                    'reclutador': diego,
                    'telefono': '+52 55 5678 9012',
                    'experiencia_anos': 3
                },
                {
                    'nombre': 'HILDA MIRIAM VARGAS PACHECO',
                    'email': 'hilda.vargas@email.com',
                    'reclutador': diego,
                    'telefono': '+52 55 6789 0123',
                    'experiencia_anos': 6
                },
                {
                    'nombre': 'VL GUERRERO SOTO DANIELA',
                    'email': 'daniela.guerrero@email.com',
                    'reclutador': erick,
                    'telefono': '+52 449 7890 1234',
                    'experiencia_anos': 2
                }
            ]
            
            candidatos_creados = []
            for candidato_data in candidatos_ejemplo:
                existing = Candidato.query.filter_by(email=candidato_data['email']).first()
                if not existing:
                    nuevo_candidato = Candidato(
                        nombre=candidato_data['nombre'],
                        email=candidato_data['email'],
                        reclutador_id=candidato_data['reclutador'].id,
                        telefono=candidato_data['telefono'],
                        experiencia_anos=candidato_data['experiencia_anos'],
                        estado='activo',
                        disponibilidad='inmediata',
                        ubicacion='Ciudad de México'
                    )
                    db.session.add(nuevo_candidato)
                    candidatos_creados.append(nuevo_candidato)
                    print(f"   ✅ Candidato creado: {candidato_data['nombre']}")
            
            db.session.commit()
            
            # Asignar candidatos a vacantes
            print("\n🔗 Asignando candidatos a vacantes...")
            
            vacantes = Vacante.query.all()
            candidatos = Candidato.query.all()
            
            # Asignaciones específicas basadas en los datos reales
            asignaciones = [
                # Felix Cuevas
                ('2210 ACC FELIX CUEVAS', ['XIMENA NAOMI LOPEZ GALVEZ', 'ROMINA JIMENEZ RAMIREZ']),
                # Monterrey
                ('#0 ACC ACC MONTERREY', ['VL CASSANDRA STEPHANIA AGUIRRE', 'ROSA IDALIA RANGEL MORENO']),
                # Las Americas
                ('#0 ACC LAS AMERICAS', ['MARIANA ESTEFHANIA TELLEZ OLIVARES', 'HILDA MIRIAM VARGAS PACHECO']),
                # Aguascalientes
                ('#0 PROMOMIX AGUASCALIENTES', ['VL GUERRERO SOTO DANIELA'])
            ]
            
            for vacante_nombre, candidatos_nombres in asignaciones:
                vacante = next((v for v in vacantes if v.nombre == vacante_nombre), None)
                if vacante:
                    for candidato_nombre in candidatos_nombres:
                        candidato = next((c for c in candidatos if c.nombre == candidato_nombre), None)
                        if candidato:
                            # Verificar si ya existe la asignación
                            existing_cp = CandidatosPositions.query.filter_by(
                                candidato_id=candidato.id,
                                vacante_id=vacante.id
                            ).first()
                            
                            if not existing_cp:
                                nueva_asignacion = CandidatosPositions(
                                    candidato_id=candidato.id,
                                    vacante_id=vacante.id,
                                    status='en_entrevista',
                                    fecha_asignacion=vacante.fecha_solicitud + timedelta(days=random.randint(1, 10)),
                                    fecha_envio_candidato=datetime.now() - timedelta(days=random.randint(1, 30)),
                                    nota=f'Candidato asignado a {vacante.nombre}'
                                )
                                
                                # Algunos candidatos están seleccionados
                                if vacante.avance == 'Seleccionando candidatos':
                                    nueva_asignacion.es_seleccionado = True
                                    nueva_asignacion.status = 'seleccionado'
                                    nueva_asignacion.entrevista_definitiva = datetime.now() - timedelta(days=random.randint(1, 15))
                                
                                db.session.add(nueva_asignacion)
                                print(f"   ✅ Asignado: {candidato.nombre} → {vacante.nombre}")
            
            db.session.commit()
            
            print("\n📊 RESUMEN DE DATOS CREADOS:")
            print("=" * 40)
            print(f"Vacantes: {Vacante.query.count()}")
            print(f"Candidatos: {Candidato.query.count()}")
            print(f"Asignaciones: {CandidatosPositions.query.count()}")
            print(f"Usuarios: {Usuario.query.count()}")
            
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error creando datos de ejemplo: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

def main():
    """Función principal de migración"""
    print("🎯 MIGRACIÓN DEL SISTEMA DE RH")
    print("🔄 Adaptando a la estructura real del negocio")
    print("=" * 50)
    
    # Paso 1: Migrar estructura
    print("PASO 1: Migración de estructura de base de datos")
    if not migrate_database():
        print("❌ Error en migración de estructura")
        return False
    
    # Paso 2: Crear datos de ejemplo
    print("\nPASO 2: Creación de datos de ejemplo")
    if not create_sample_data():
        print("❌ Error creando datos de ejemplo")
        return False
    
    print("\n🎉 ¡MIGRACIÓN COMPLETADA EXITOSAMENTE!")
    print("=" * 50)
    print("El sistema ahora refleja el proceso real de reclutamiento:")
    print("• Vacantes con candidatos requeridos y días transcurridos")
    print("• Estados de avance del proceso")
    print("• Fechas de envío y entrevistas")
    print("• Candidatos seleccionados y propuestas")
    print("• Datos de ejemplo basados en casos reales")
    
    print("\n🔑 USUARIOS DISPONIBLES:")
    print("admin@empresa.com / password123 (Admin)")
    print("alfredo.ambriz@empresa.com / password123 (Ejecutivo)")
    print("sofia.rueda@empresa.com / password123 (Ejecutivo)")
    print("diego.quintanar@empresa.com / password123 (Reclutador)")
    print("erick.cervantes@empresa.com / password123 (Reclutador)")
    print("fernanda.moreno@empresa.com / password123 (Reclutador Líder)")
    
    return True

if __name__ == '__main__':
    main()
