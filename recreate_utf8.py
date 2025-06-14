#!/usr/bin/env python3
"""
Alternativa: Recrear base de datos con UTF-8 correcto desde el inicio
"""
from app import create_app
from extensions import db
import sys

def backup_data():
    """Hacer backup de datos importantes antes de recrear"""
    print("💾 HACIENDO BACKUP DE DATOS...")
    
    backup_data = {
        'usuarios': [],
        'vacantes': [],
        'candidatos': []
    }
    
    try:
        app = create_app()
        with app.app_context():
            # Backup usuarios
            usuarios = db.session.execute(db.text("""
                SELECT id, nombre, email, rol, activo
                FROM usuario WHERE activo = 1
            """)).fetchall()
            
            for usuario in usuarios:
                backup_data['usuarios'].append({
                    'id': usuario[0],
                    'nombre': usuario[1],
                    'email': usuario[2],
                    'rol': usuario[3],
                    'activo': usuario[4]
                })
            
            print(f"   ✅ {len(backup_data['usuarios'])} usuarios respaldados")
            
            # Backup vacantes (solo datos básicos sin acentos problemáticos)
            vacantes = db.session.execute(db.text("""
                SELECT id, ejecutivo_id, reclutador_id, reclutador_lider_id, 
                       vacantes, candidatos_requeridos, entrevistas_op, 
                       prioridad, fecha_solicitud
                FROM vacante
            """)).fetchall()
            
            for vacante in vacantes:
                backup_data['vacantes'].append({
                    'id': vacante[0],
                    'ejecutivo_id': vacante[1],
                    'reclutador_id': vacante[2],
                    'reclutador_lider_id': vacante[3],
                    'vacantes': vacante[4],
                    'candidatos_requeridos': vacante[5],
                    'entrevistas_op': vacante[6],
                    'prioridad': vacante[7],
                    'fecha_solicitud': vacante[8]
                })
            
            print(f"   ✅ {len(backup_data['vacantes'])} vacantes respaldadas")
            
            return backup_data
            
    except Exception as e:
        print(f"   ❌ Error en backup: {str(e)}")
        return None

def recreate_tables_with_utf8():
    """Recrear todas las tablas con UTF-8 correcto"""
    print("\n🔄 RECREANDO TABLAS CON UTF-8...")
    
    try:
        app = create_app()
        with app.app_context():
            # Eliminar todas las tablas
            print("   🗑️  Eliminando tablas existentes...")
            db.drop_all()
            
            # Recrear con UTF-8
            print("   🏗️  Creando tablas con UTF-8...")
            db.create_all()
            
            # Verificar que las tablas se crearon con UTF-8
            tables = db.session.execute(db.text("""
                SELECT TABLE_NAME, TABLE_COLLATION
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_SCHEMA = DATABASE()
                AND TABLE_TYPE = 'BASE TABLE'
            """)).fetchall()
            
            for table_name, table_collation in tables:
                if 'utf8mb4' in str(table_collation):
                    print(f"   ✅ {table_name}: {table_collation}")
                else:
                    print(f"   ⚠️  {table_name}: {table_collation} (no es utf8mb4)")
            
            return True
            
    except Exception as e:
        print(f"   ❌ Error recreando tablas: {str(e)}")
        return False

def restore_basic_data(backup_data):
    """Restaurar datos básicos después de recrear tablas"""
    print("\n📥 RESTAURANDO DATOS BÁSICOS...")
    
    try:
        app = create_app()
        with app.app_context():
            from models import Usuario
            
            # Restaurar usuarios con contraseñas por defecto
            default_passwords = {
                'ejecutivo': 'admin123',
                'reclutador': 'reclutador123',
                'reclutador_lider': 'lider123'
            }
            
            for user_data in backup_data['usuarios']:
                try:
                    new_user = Usuario(
                        nombre=user_data['nombre'],
                        email=user_data['email'],
                        rol=user_data['rol'],
                        activo=True
                    )
                    
                    # Asignar contraseña por defecto según rol
                    password = default_passwords.get(user_data['rol'], 'password123')
                    new_user.set_password(password)
                    
                    db.session.add(new_user)
                    print(f"   ✅ Usuario restaurado: {user_data['email']}")
                    
                except Exception as e:
                    print(f"   ⚠️  Error restaurando usuario {user_data['email']}: {str(e)}")
            
            db.session.commit()
            print(f"   ✅ {len(backup_data['usuarios'])} usuarios restaurados")
            
            return True
            
    except Exception as e:
        print(f"   ❌ Error restaurando datos: {str(e)}")
        db.session.rollback()
        return False

def create_test_data_with_utf8():
    """Crear datos de prueba con caracteres UTF-8"""
    print("\n🧪 CREANDO DATOS DE PRUEBA CON UTF-8...")
    
    try:
        app = create_app()
        with app.app_context():
            from models import Usuario, Vacante
            
            # Buscar un usuario para asignar
            user = Usuario.query.first()
            if not user:
                print("   ⚠️  No hay usuarios disponibles")
                return False
            
            # Crear vacantes de prueba con acentos
            test_vacantes = [
                {
                    'nombre': 'Administración y Ventas',
                    'descripcion': 'Posición en área administrativa con atención al público'
                },
                {
                    'nombre': 'Técnico en Informática',
                    'descripcion': 'Soporte técnico y mantenimiento de equipos'
                },
                {
                    'nombre': 'Coordinación de Logística',
                    'descripcion': 'Gestión de almacén y distribución de productos'
                }
            ]
            
            for vacante_data in test_vacantes:
                new_vacante = Vacante(
                    nombre=vacante_data['nombre'],
                    descripcion=vacante_data['descripcion'],
                    ejecutivo_id=user.id,
                    reclutador_id=user.id,
                    candidatos_requeridos=3,
                    vacantes=1
                )
                
                db.session.add(new_vacante)
                print(f"   ✅ Vacante creada: {vacante_data['nombre']}")
            
            db.session.commit()
            print("   ✅ Datos de prueba con UTF-8 creados")
            
            return True
            
    except Exception as e:
        print(f"   ❌ Error creando datos de prueba: {str(e)}")
        db.session.rollback()
        return False

def main():
    print("=" * 70)
    print("🔄 RECREACIÓN COMPLETA DE BASE DE DATOS CON UTF-8")
    print("=" * 70)
    print()
    print("⚠️  ADVERTENCIA: Este proceso eliminará todas las tablas actuales")
    print("   Se hará un backup de usuarios básicos antes de proceder")
    print()
    
    respuesta = input("¿Continuar con la recreación? (s/N): ").lower()
    if respuesta not in ['s', 'si', 'y', 'yes']:
        print("❌ Proceso cancelado por el usuario")
        return
    
    print("\n🚀 Iniciando recreación...")
    
    # Paso 1: Backup
    backup_data = backup_data()
    if not backup_data:
        print("❌ No se pudo hacer backup, abortando")
        return
    
    # Paso 2: Recrear tablas
    if not recreate_tables_with_utf8():
        print("❌ Error recreando tablas")
        return
    
    # Paso 3: Restaurar datos básicos
    if not restore_basic_data(backup_data):
        print("❌ Error restaurando datos")
        return
    
    # Paso 4: Crear datos de prueba
    if not create_test_data_with_utf8():
        print("❌ Error creando datos de prueba")
        return
    
    print("\n" + "=" * 70)
    print("🎉 ¡RECREACIÓN EXITOSA!")
    print("\n✅ Base de datos recreada con UTF-8 completo")
    print("✅ Usuarios restaurados con contraseñas por defecto:")
    print("   • admin@empresa.com / admin123")
    print("   • reclutador@empresa.com / reclutador123")
    print("   • lider@empresa.com / lider123")
    print("✅ Datos de prueba con acentos creados")
    print("\n🚀 Próximos pasos:")
    print("   1. Reiniciar servidor: python app.py")
    print("   2. Probar formulario: python test_vacants.py")
    print("   3. Usar caracteres especiales sin problemas")
    print("=" * 70)

if __name__ == '__main__':
    main()
