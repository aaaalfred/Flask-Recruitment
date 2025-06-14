#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simplificado para crear datos de ejemplo sin problemas de codificación
"""

from app import create_app
from extensions import db
from datetime import datetime, timedelta

def create_simple_data():
    """Crear datos de ejemplo simplificados"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🎯 CREANDO DATOS DE EJEMPLO SIMPLIFICADOS")
            print("=" * 50)
            
            # Importar modelos
            from models import Usuario, Vacante, Candidato, CandidatosPositions
            
            # Eliminar datos existentes
            print("🗑️  Limpiando datos existentes...")
            CandidatosPositions.query.delete()
            Candidato.query.delete()
            Vacante.query.delete()
            Usuario.query.delete()
            db.session.commit()
            
            # 1. Crear usuarios
            print("\n👥 Creando usuarios...")
            usuarios = [
                Usuario(nombre='Admin Sistema', email='admin@empresa.com', rol='ejecutivo'),
                Usuario(nombre='Alfredo Ambriz', email='alfredo@empresa.com', rol='ejecutivo'),
                Usuario(nombre='Sofia Rueda', email='sofia@empresa.com', rol='ejecutivo'),
                Usuario(nombre='Diego Quintanar', email='diego@empresa.com', rol='reclutador'),
                Usuario(nombre='Erick Cervantes', email='erick@empresa.com', rol='reclutador'),
                Usuario(nombre='Fernanda Moreno', email='fernanda@empresa.com', rol='reclutador_lider')
            ]
            
            for usuario in usuarios:
                usuario.set_password('password123')
                db.session.add(usuario)
                print(f"   ✅ {usuario.nombre}")
            
            db.session.commit()
            
            # 2. Crear vacantes simples
            print("\n📋 Creando vacantes...")
            alfredo = Usuario.query.filter_by(email='alfredo@empresa.com').first()
            sofia = Usuario.query.filter_by(email='sofia@empresa.com').first()
            diego = Usuario.query.filter_by(email='diego@empresa.com').first()
            erick = Usuario.query.filter_by(email='erick@empresa.com').first()
            fernanda = Usuario.query.filter_by(email='fernanda@empresa.com').first()
            
            vacantes = [
                Vacante(
                    nombre='2210 ACC FELIX CUEVAS',
                    descripcion='Posicion para centro comercial Felix Cuevas',
                    ejecutivo_id=alfredo.id,
                    reclutador_id=diego.id,
                    reclutador_lider_id=fernanda.id,
                    fecha_solicitud=datetime.now() - timedelta(days=54),
                    candidatos_requeridos=3,
                    entrevistas_op=3,
                    vacantes=1,
                    avance='En proceso',
                    status_final='cubierta',
                    ubicacion='Felix Cuevas CDMX',
                    estado='cerrada',
                    dias_transcurridos=54
                ),
                Vacante(
                    nombre='2120 ACC CANCUN',
                    descripcion='Posicion para centro comercial Cancun',
                    ejecutivo_id=sofia.id,
                    reclutador_id=erick.id,
                    reclutador_lider_id=fernanda.id,
                    fecha_solicitud=datetime.now() - timedelta(days=80),
                    candidatos_requeridos=3,
                    entrevistas_op=3,
                    vacantes=1,
                    avance='En proceso',
                    status_final='cubierta',
                    ubicacion='Cancun QR',
                    estado='cerrada',
                    dias_transcurridos=80
                ),
                Vacante(
                    nombre='2121 ASESORA MONTERREY',
                    descripcion='Posicion de asesora en Monterrey',
                    ejecutivo_id=sofia.id,
                    reclutador_id=erick.id,
                    reclutador_lider_id=fernanda.id,
                    fecha_solicitud=datetime.now() - timedelta(days=90),
                    candidatos_requeridos=3,
                    entrevistas_op=3,
                    vacantes=1,
                    avance='En proceso',
                    status_final='cubierta',
                    ubicacion='Monterrey NL',
                    estado='cerrada',
                    dias_transcurridos=90
                ),
                Vacante(
                    nombre='2136 ACC LEON',
                    descripcion='Posicion para centro comercial Leon',
                    ejecutivo_id=alfredo.id,
                    reclutador_id=erick.id,
                    reclutador_lider_id=fernanda.id,
                    fecha_solicitud=datetime.now() - timedelta(days=120),
                    candidatos_requeridos=3,
                    entrevistas_op=3,
                    vacantes=1,
                    avance='En proceso',
                    status_final='cubierta',
                    ubicacion='Leon GTO',
                    estado='cerrada',
                    dias_transcurridos=120
                )
            ]
            
            for vacante in vacantes:
                db.session.add(vacante)
                print(f"   ✅ {vacante.nombre}")
            
            db.session.commit()
            
            # 3. Crear candidatos
            print("\n👤 Creando candidatos...")
            candidatos = [
                Candidato(
                    nombre='ALEJANDRA ALARCON DE LA CRUZ',
                    email='alejandra.alarcon@email.com',
                    reclutador_id=erick.id,
                    telefono='+52 998 123 4567',
                    estado='activo',
                    disponibilidad='inmediata',
                    experiencia_anos=2
                ),
                Candidato(
                    nombre='ALICIA RODRIGUEZ VELEZ',
                    email='alicia.rodriguez@email.com',
                    reclutador_id=erick.id,
                    telefono='+52 81 234 5678',
                    estado='activo',
                    disponibilidad='inmediata',
                    experiencia_anos=3
                ),
                Candidato(
                    nombre='ADELA CAMPOS GUERRERO',
                    email='adela.campos@email.com',
                    reclutador_id=erick.id,
                    telefono='+52 477 345 6789',
                    estado='activo',
                    disponibilidad='inmediata',
                    experiencia_anos=1
                ),
                Candidato(
                    nombre='ADRIANA PILAR MORENO MARTINEZ',
                    email='adriana.moreno@email.com',
                    reclutador_id=fernanda.id,
                    telefono='+52 55 456 7890',
                    estado='activo',
                    disponibilidad='inmediata',
                    experiencia_anos=4
                )
            ]
            
            for candidato in candidatos:
                db.session.add(candidato)
                print(f"   ✅ {candidato.nombre}")
            
            db.session.commit()
            
            # 4. Crear asignaciones candidato-vacante
            print("\n🔗 Creando asignaciones candidato-vacante...")
            
            # Obtener objetos para las asignaciones
            alejandra = Candidato.query.filter_by(email='alejandra.alarcon@email.com').first()
            alicia = Candidato.query.filter_by(email='alicia.rodriguez@email.com').first()
            adela = Candidato.query.filter_by(email='adela.campos@email.com').first()
            adriana = Candidato.query.filter_by(email='adriana.moreno@email.com').first()
            
            cancun = Vacante.query.filter_by(nombre='2120 ACC CANCUN').first()
            monterrey = Vacante.query.filter_by(nombre='2121 ASESORA MONTERREY').first()
            leon = Vacante.query.filter_by(nombre='2136 ACC LEON').first()
            
            asignaciones = [
                CandidatosPositions(
                    candidato_id=alejandra.id,
                    vacante_id=cancun.id,
                    status='rechazado',
                    aceptado=False,
                    contratado_status='rechazado',
                    comentarios_finales='CANDIDATA DESCARTA POR NO CONTAR CON EXPERIENCIA EN AUTOSERVICIO',
                    archivo_cv='CV_2_(5).pdf',
                    se_presento=True,
                    fecha_decision_final=datetime.now() - timedelta(days=10)
                ),
                CandidatosPositions(
                    candidato_id=alicia.id,
                    vacante_id=monterrey.id,
                    status='rechazado',
                    aceptado=True,  # Fue aceptada por supervisor
                    contratado_status='rechazado',
                    comentarios_finales='CANDIDATA ACEPTADA POR SUPERVISOR, PERO NO SE PRESENTO A TIENDA',
                    archivo_cv='Alicia_Rodriguez_Velez.pdf',
                    se_presento=False,
                    fecha_decision_final=datetime.now() - timedelta(days=15)
                ),
                CandidatosPositions(
                    candidato_id=adela.id,
                    vacante_id=leon.id,
                    status='rechazado',
                    aceptado=False,
                    contratado_status='rechazado',
                    comentarios_finales='CANDIDATA NO CONTESTO LLAMADAS Y MENSAJES PARA LLEVAR A CABO ENTREVISTA',
                    archivo_cv='CVAdelaCampos.pdf',
                    se_presento=True,
                    fecha_decision_final=datetime.now() - timedelta(days=20)
                ),
                CandidatosPositions(
                    candidato_id=adriana.id,
                    vacante_id=leon.id,
                    status='rechazado',
                    aceptado=True,
                    contratado_status='no_contratable',
                    comentarios_finales='CANDIDATA ACEPTADA POR SUPERVISOR, PERO NO SE PRESENTO A TIENDA',
                    archivo_cv='ADRIANA_PILAR_MORENO_MTZ.pdf',
                    se_presento=False,
                    fecha_decision_final=datetime.now() - timedelta(days=5)
                )
            ]
            
            for asignacion in asignaciones:
                db.session.add(asignacion)
            
            db.session.commit()
            
            # Ahora mostrar las asignaciones creadas
            print("   Asignaciones creadas:")
            for cp in CandidatosPositions.query.all():
                print(f"   ✅ {cp.candidato.nombre} → {cp.vacante.nombre}")
            
            # 5. Actualizar resúmenes de vacantes
            print("\n🔄 Actualizando resúmenes...")
            for vacante in Vacante.query.all():
                vacante.resumen_ia = f"Vacante {vacante.nombre} en {vacante.ubicacion}. " \
                                   f"Ejecutivo: {vacante.ejecutivo.nombre}. " \
                                   f"Reclutador: {vacante.reclutador.nombre}. " \
                                   f"Dias transcurridos: {vacante.dias_transcurridos}."
            
            db.session.commit()
            
            print("\n📊 ESTADÍSTICAS FINALES:")
            print("=" * 30)
            print(f"👥 Usuarios: {Usuario.query.count()}")
            print(f"📋 Vacantes: {Vacante.query.count()}")
            print(f"👤 Candidatos: {Candidato.query.count()}")
            print(f"🔗 Asignaciones: {CandidatosPositions.query.count()}")
            
            # Estadísticas específicas
            aceptados = CandidatosPositions.query.filter_by(aceptado=True).count()
            rechazados = CandidatosPositions.query.filter_by(contratado_status='rechazado').count()
            no_contratables = CandidatosPositions.query.filter_by(contratado_status='no_contratable').count()
            no_presentados = CandidatosPositions.query.filter_by(se_presento=False).count()
            
            print(f"\n📈 Estadísticas del proceso:")
            print(f"✅ Aceptados por supervisor: {aceptados}")
            print(f"❌ Rechazados: {rechazados}")
            print(f"🚫 No contratables: {no_contratables}")
            print(f"🏃 No se presentaron: {no_presentados}")
            
            print("\n🎉 ¡DATOS CREADOS EXITOSAMENTE!")
            print("=" * 40)
            print("🔑 CREDENCIALES DE ACCESO:")
            print("admin@empresa.com / password123 (Admin)")
            print("alfredo@empresa.com / password123 (Ejecutivo)")
            print("erick@empresa.com / password123 (Reclutador)")
            print("fernanda@empresa.com / password123 (Reclutador Líder)")
            
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    create_simple_data()
