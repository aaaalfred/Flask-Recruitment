#!/usr/bin/env python3
"""
Script para actualizar el modelo a la estructura real del negocio
basado en los datos de candidatos reales
"""

from app import create_app
from extensions import db
from sqlalchemy import text

def update_database_structure():
    """Actualizar estructura para reflejar el flujo real de candidatos"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🔄 ACTUALIZANDO ESTRUCTURA PARA FLUJO REAL DE CANDIDATOS")
            print("=" * 60)
            
            # Agregar nuevas columnas a candidatos_posiciones
            print("📋 Actualizando tabla candidatos_posiciones...")
            
            new_columns_cp = [
                "ALTER TABLE candidatos_posiciones ADD COLUMN aceptado BOOLEAN DEFAULT FALSE",
                "ALTER TABLE candidatos_posiciones ADD COLUMN contratado_status ENUM('pendiente', 'rechazado', 'contratado', 'no_contratable') DEFAULT 'pendiente'",
                "ALTER TABLE candidatos_posiciones ADD COLUMN comentarios_finales TEXT",
                "ALTER TABLE candidatos_posiciones ADD COLUMN archivo_cv VARCHAR(200)",
                "ALTER TABLE candidatos_posiciones ADD COLUMN cv_url_especifico VARCHAR(500)",
                "ALTER TABLE candidatos_posiciones ADD COLUMN fecha_decision_final DATETIME",
                "ALTER TABLE candidatos_posiciones ADD COLUMN entrevista_realizada BOOLEAN DEFAULT FALSE",
                "ALTER TABLE candidatos_posiciones ADD COLUMN se_presento BOOLEAN DEFAULT TRUE",
                "ALTER TABLE candidatos_posiciones ADD COLUMN motivo_rechazo VARCHAR(200)"
            ]
            
            for sql in new_columns_cp:
                try:
                    db.session.execute(text(sql))
                    print(f"   ✅ {sql.split('ADD COLUMN')[1].split()[0]}")
                except Exception as e:
                    if "Duplicate column name" not in str(e):
                        print(f"   ⚠️  Error: {e}")
            
            # Agregar nuevas columnas a vacante
            print("\n📋 Actualizando tabla vacante...")
            
            new_columns_vacante = [
                "ALTER TABLE vacante ADD COLUMN status_final ENUM('abierta', 'cubierta', 'cancelada', 'pausada') DEFAULT 'abierta'",
                "ALTER TABLE vacante ADD COLUMN fecha_cierre DATETIME"
            ]
            
            for sql in new_columns_vacante:
                try:
                    db.session.execute(text(sql))
                    print(f"   ✅ {sql.split('ADD COLUMN')[1].split()[0]}")
                except Exception as e:
                    if "Duplicate column name" not in str(e):
                        print(f"   ⚠️  Error: {e}")
            
            # Agregar columna a candidato
            print("\n📋 Actualizando tabla candidato...")
            
            new_columns_candidato = [
                "ALTER TABLE candidato ADD COLUMN comentarios_generales TEXT"
            ]
            
            for sql in new_columns_candidato:
                try:
                    db.session.execute(text(sql))
                    print(f"   ✅ {sql.split('ADD COLUMN')[1].split()[0]}")
                except Exception as e:
                    if "Duplicate column name" not in str(e):
                        print(f"   ⚠️  Error: {e}")
            
            db.session.commit()
            print("\n✅ Estructura actualizada exitosamente!")
            
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error actualizando estructura: {str(e)}")
            return False

def create_sample_real_data():
    """Crear datos de ejemplo que reflejen el flujo real"""
    app = create_app()
    
    with app.app_context():
        try:
            from models import Usuario, Vacante, Candidato, CandidatosPositions
            
            print("\n📝 CREANDO DATOS DE EJEMPLO REALES")
            print("=" * 40)
            
            # Crear candidatos basados en los ejemplos reales
            candidatos_reales = [
                {
                    'nombre': 'ALEJANDRA ALARCON DE LA CRUZ',
                    'email': 'alejandra.alarcon@email.com',
                    'archivo_cv': 'CV_2_(5).pdf',
                    'reclutador_email': 'erick.cervantes@empresa.com'
                },
                {
                    'nombre': 'ALICIA RODRIGUEZ VELEZ',
                    'email': 'alicia.rodriguez@email.com',
                    'archivo_cv': 'Alicia_Rodriguez_Velez.pdf',
                    'reclutador_email': 'erick.cervantes@empresa.com'
                },
                {
                    'nombre': 'ADELA CAMPOS GUERRERO',
                    'email': 'adela.campos@email.com',
                    'archivo_cv': 'CVAdelaCampos.pdf',
                    'reclutador_email': 'erick.cervantes@empresa.com'
                },
                {
                    'nombre': 'ADRIANA PILAR MORENO MARTINEZ',
                    'email': 'adriana.moreno@email.com',
                    'archivo_cv': 'ADRIANA_PILAR_MORENO_MTZ.pdf',
                    'reclutador_email': 'fernanda.moreno@empresa.com'
                }
            ]
            
            # Crear candidatos
            for candidato_data in candidatos_reales:
                reclutador = Usuario.query.filter_by(email=candidato_data['reclutador_email']).first()
                if reclutador:
                    existing = Candidato.query.filter_by(email=candidato_data['email']).first()
                    if not existing:
                        nuevo_candidato = Candidato(
                            nombre=candidato_data['nombre'],
                            email=candidato_data['email'],
                            reclutador_id=reclutador.id,
                            telefono='+52 55 1234 5678',
                            estado='activo',
                            disponibilidad='inmediata'
                        )
                        db.session.add(nuevo_candidato)
                        print(f"   ✅ Candidato: {candidato_data['nombre']}")
            
            db.session.commit()
            
            # Crear asignaciones candidato-vacante con datos reales
            print("\n🔗 Creando asignaciones candidato-vacante...")
            
            asignaciones_reales = [
                {
                    'candidato_email': 'alejandra.alarcon@email.com',
                    'vacante_nombre': '2210 ACC FELIX CUEVAS',  # Crear si no existe
                    'aceptado': False,
                    'contratado_status': 'rechazado',
                    'comentarios_finales': 'CANDIDATA DESCARTA POR NO CONTAR CON EXPERIENCIA EN AUTOSERVICIO',
                    'archivo_cv': 'CV_2_(5).pdf'
                },
                {
                    'candidato_email': 'alicia.rodriguez@email.com',
                    'vacante_nombre': '2121 ASESORA MONTERREY',
                    'aceptado': True,  # Fue aceptada por supervisor
                    'contratado_status': 'rechazado',
                    'comentarios_finales': 'CANDIDATA ACEPTADA POR SUPERVISOR, PERO NO SE PRESENTO A TIENDA',
                    'archivo_cv': 'Alicia_Rodriguez_Velez.pdf',
                    'se_presento': False
                },
                {
                    'candidato_email': 'adela.campos@email.com',
                    'vacante_nombre': '2136 ACC LEON',
                    'aceptado': False,
                    'contratado_status': 'rechazado',
                    'comentarios_finales': 'CANDIDATA NO CONTESTO LLAMADAS Y MENSAJES PARA LLEVAR A CABO ENTREVISTA CON EJECUTIVO',
                    'archivo_cv': 'CVAdelaCampos.pdf'
                },
                {
                    'candidato_email': 'adriana.moreno@email.com',
                    'vacante_nombre': '2137 ACC GUADALAJARA',
                    'aceptado': True,
                    'contratado_status': 'no_contratable',
                    'comentarios_finales': 'CANDIDATA ACEPTADA POR SUPERVISOR, PERO NO SE PRESENTO A TIENDA',
                    'archivo_cv': 'ADRIANA_PILAR_MORENO_MTZ.pdf',
                    'se_presento': False
                }
            ]
            
            # Crear vacantes si no existen y asignar candidatos
            ejecutivo = Usuario.query.filter_by(rol='ejecutivo').first()
            reclutador = Usuario.query.filter_by(rol='reclutador').first()
            lider = Usuario.query.filter_by(rol='reclutador_lider').first()
            
            for asignacion in asignaciones_reales:
                # Crear vacante si no existe
                vacante = Vacante.query.filter_by(nombre=asignacion['vacante_nombre']).first()
                if not vacante:
                    vacante = Vacante(
                        nombre=asignacion['vacante_nombre'],
                        descripcion=f"Vacante {asignacion['vacante_nombre']}",
                        ejecutivo_id=ejecutivo.id,
                        reclutador_id=reclutador.id,
                        reclutador_lider_id=lider.id,
                        candidatos_requeridos=3,
                        entrevistas_op=3,
                        avance='En proceso',
                        status_final='cubierta'  # Todas están cubiertas según los datos
                    )
                    db.session.add(vacante)
                    db.session.commit()  # Commit para obtener ID
                
                # Buscar candidato
                candidato = Candidato.query.filter_by(email=asignacion['candidato_email']).first()
                
                if candidato and vacante:
                    # Verificar si ya existe la asignación
                    existing_cp = CandidatosPositions.query.filter_by(
                        candidato_id=candidato.id,
                        vacante_id=vacante.id
                    ).first()
                    
                    if not existing_cp:
                        nueva_asignacion = CandidatosPositions(
                            candidato_id=candidato.id,
                            vacante_id=vacante.id,
                            status='rechazado' if asignacion['contratado_status'] == 'rechazado' else 'evaluado',
                            aceptado=asignacion['aceptado'],
                            contratado_status=asignacion['contratado_status'],
                            comentarios_finales=asignacion['comentarios_finales'],
                            archivo_cv=asignacion['archivo_cv'],
                            se_presento=asignacion.get('se_presento', True)
                        )
                        db.session.add(nueva_asignacion)
                        print(f"   ✅ Asignación: {candidato.nombre} → {vacante.nombre}")
            
            db.session.commit()
            
            print("\n📊 DATOS REALES CREADOS:")
            print("=" * 30)
            print(f"Candidatos: {Candidato.query.count()}")
            print(f"Vacantes: {Vacante.query.count()}")
            print(f"Asignaciones: {CandidatosPositions.query.count()}")
            
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error creando datos reales: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

def main():
    """Ejecutar actualización completa"""
    print("🎯 SINCRONIZACIÓN CON FLUJO REAL DE CANDIDATOS")
    print("=" * 55)
    
    # Paso 1: Actualizar estructura
    if update_database_structure():
        print("\n✅ Estructura actualizada")
    else:
        print("\n❌ Error en estructura")
        return False
    
    # Paso 2: Crear datos reales
    if create_sample_real_data():
        print("\n✅ Datos reales creados")
    else:
        print("\n❌ Error en datos")
        return False
    
    print("\n🎉 ¡SINCRONIZACIÓN COMPLETADA!")
    print("El sistema ahora refleja el flujo real:")
    print("• Estados específicos de candidatos por vacante")
    print("• Comentarios finales del proceso")
    print("• Control de aceptación por supervisor")
    print("• Seguimiento de presentación del candidato")
    print("• Status final de vacantes (CUBIERTA)")
    
    return True

if __name__ == '__main__':
    main()
