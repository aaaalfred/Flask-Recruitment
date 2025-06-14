#!/usr/bin/env python3
"""
Script para crear las tablas del sistema de reclutamiento en la base de datos correcta
Soluciona el error 422 creando la estructura necesaria
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from extensions import db
from models import Usuario, Vacante, Candidato, Documento, Entrevista, CandidatosPositions

def create_database_and_tables():
    """Crear base de datos y todas las tablas necesarias"""
    print("🗄️ INICIALIZANDO BASE DE DATOS DEL SISTEMA DE RECLUTAMIENTO")
    print("=" * 70)
    
    try:
        app = create_app()
        
        with app.app_context():
            print("📊 Configuración de base de datos:")
            print(f"   Host: {app.config['MYSQL_HOST']}")
            print(f"   Usuario: {app.config['MYSQL_USER']}")
            print(f"   Base de datos: {app.config['MYSQL_DB']}")
            print(f"   URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
            
            # Crear todas las tablas
            print("\n🔨 Creando tablas...")
            db.create_all()
            print("✅ Tablas creadas exitosamente")
            
            # Verificar que las tablas existen
            print("\n🔍 Verificando tablas creadas:")
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            expected_tables = ['usuario', 'vacante', 'candidato', 'documento', 'entrevista', 'candidatos_posiciones']
            
            for table in expected_tables:
                if table in tables:
                    print(f"   ✅ {table}")
                else:
                    print(f"   ❌ {table} - NO ENCONTRADA")
            
            print(f"\n📋 Total de tablas encontradas: {len(tables)}")
            print(f"   Tablas: {', '.join(tables)}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error creando base de datos: {str(e)}")
        return False

def create_initial_users():
    """Crear usuarios iniciales del sistema"""
    print("\n👥 CREANDO USUARIOS INICIALES...")
    
    try:
        app = create_app()
        
        with app.app_context():
            # Verificar si ya existe el usuario admin
            existing_admin = Usuario.query.filter_by(email='admin@empresa.com').first()
            if existing_admin:
                print("⚠️  Usuario admin ya existe")
                print(f"   ID: {existing_admin.id}")
                print(f"   Nombre: {existing_admin.nombre}")
                print(f"   Rol: {existing_admin.rol}")
                return True
            
            # Crear usuario administrador
            admin_user = Usuario(
                nombre='Administrador Sistema',
                email='admin@empresa.com',
                rol='ejecutivo',
                activo=True
            )
            admin_user.set_password('password123')
            
            # Crear reclutador líder
            lider_user = Usuario(
                nombre='Ana García - Líder',
                email='ana.lider@empresa.com',
                rol='reclutador_lider',
                activo=True
            )
            lider_user.set_password('demo123')
            
            # Crear reclutador
            reclutador_user = Usuario(
                nombre='María González',
                email='maria.gonzalez@empresa.com',
                rol='reclutador',
                activo=True
            )
            reclutador_user.set_password('demo123')
            
            # Crear ejecutivo
            ejecutivo_user = Usuario(
                nombre='Roberto Ejecutivo',
                email='roberto.ejecutivo@empresa.com',
                rol='ejecutivo',
                activo=True
            )
            ejecutivo_user.set_password('demo123')
            
            # Guardar usuarios
            db.session.add(admin_user)
            db.session.add(lider_user)
            db.session.add(reclutador_user)
            db.session.add(ejecutivo_user)
            db.session.commit()
            
            print("✅ Usuarios creados exitosamente:")
            print(f"   👑 Admin: admin@empresa.com / password123 (ejecutivo)")
            print(f"   🛡️  Líder: ana.lider@empresa.com / demo123 (reclutador_lider)")
            print(f"   👤 Reclutador: maria.gonzalez@empresa.com / demo123 (reclutador)")
            print(f"   💼 Ejecutivo: roberto.ejecutivo@empresa.com / demo123 (ejecutivo)")
            
            return True
            
    except Exception as e:
        print(f"❌ Error creando usuarios: {str(e)}")
        return False

def verify_system():
    """Verificar que el sistema esté funcionando correctamente"""
    print("\n🔍 VERIFICANDO SISTEMA...")
    
    try:
        app = create_app()
        
        with app.app_context():
            # Contar usuarios
            total_usuarios = Usuario.query.count()
            usuarios_activos = Usuario.query.filter_by(activo=True).count()
            
            print(f"✅ Sistema verificado:")
            print(f"   👥 Total usuarios: {total_usuarios}")
            print(f"   ✅ Usuarios activos: {usuarios_activos}")
            
            # Mostrar usuarios por rol
            for rol in ['ejecutivo', 'reclutador_lider', 'reclutador']:
                count = Usuario.query.filter_by(rol=rol, activo=True).count()
                print(f"   {rol}: {count}")
            
            # Verificar login del admin
            admin_user = Usuario.query.filter_by(email='admin@empresa.com').first()
            if admin_user and admin_user.check_password('password123'):
                print(f"✅ Login admin verificado correctamente")
            else:
                print(f"❌ Login admin FALLO")
            
            return True
            
    except Exception as e:
        print(f"❌ Error verificando sistema: {str(e)}")
        return False

def main():
    """Función principal"""
    print("🚀 SOLUCIONANDO ERROR HTTP 422 - INICIALIZACIÓN COMPLETA")
    print("=" * 70)
    
    # Paso 1: Crear base de datos y tablas
    if not create_database_and_tables():
        print("❌ FALLO: No se pudieron crear las tablas")
        return False
    
    # Paso 2: Crear usuarios iniciales
    if not create_initial_users():
        print("❌ FALLO: No se pudieron crear los usuarios")
        return False
    
    # Paso 3: Verificar sistema
    if not verify_system():
        print("❌ FALLO: No se pudo verificar el sistema")
        return False
    
    print("\n🎉 SISTEMA INICIALIZADO CORRECTAMENTE")
    print("=" * 70)
    print("Para probar el sistema:")
    print("1. Ejecutar backend: cd C:\\Users\\ADMIN\\code\\rh && python app.py")
    print("2. Ejecutar frontend: cd C:\\Users\\ADMIN\\code\\rh\\frontend && npm start")
    print("3. Ir a: http://localhost:3000/login")
    print("4. Login: admin@empresa.com / password123")
    print("5. Ir a: http://localhost:3000/users")
    
    return True

if __name__ == '__main__':
    success = main()
    if not success:
        sys.exit(1)
