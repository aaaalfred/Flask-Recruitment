#!/usr/bin/env python3
"""
Script de diagnóstico y reparación completa del sistema
"""
from app import create_app
from extensions import db
from models import Usuario
import sys
import os

def check_database_connection():
    """Verificar conexión a la base de datos"""
    print("🔌 Verificando conexión a la base de datos...")
    
    try:
        app = create_app()
        with app.app_context():
            # Intentar una consulta simple
            result = db.session.execute(db.text('SELECT 1')).fetchone()
            if result:
                print("✅ Conexión a la base de datos exitosa")
                return True
            else:
                print("❌ Problema con la consulta a la base de datos")
                return False
    except Exception as e:
        print(f"❌ Error de conexión a la base de datos: {str(e)}")
        return False

def check_tables_exist():
    """Verificar que las tablas existan"""
    print("📋 Verificando tablas de la base de datos...")
    
    try:
        app = create_app()
        with app.app_context():
            # Verificar tabla de usuarios
            result = db.session.execute(db.text("SHOW TABLES LIKE 'usuario'")).fetchone()
            if result:
                print("✅ Tabla 'usuario' existe")
                
                # Verificar estructura
                columns = db.session.execute(db.text("DESCRIBE usuario")).fetchall()
                print(f"   📊 Columnas encontradas: {len(columns)}")
                for col in columns:
                    print(f"      • {col[0]} ({col[1]})")
                return True
            else:
                print("❌ Tabla 'usuario' no existe")
                return False
    except Exception as e:
        print(f"❌ Error verificando tablas: {str(e)}")
        return False

def create_tables():
    """Crear tablas si no existen"""
    print("🏗️  Creando tablas...")
    
    try:
        app = create_app()
        with app.app_context():
            db.create_all()
            print("✅ Tablas creadas/verificadas exitosamente")
            return True
    except Exception as e:
        print(f"❌ Error creando tablas: {str(e)}")
        return False

def create_admin_user():
    """Crear usuario administrador"""
    print("👤 Creando usuario administrador...")
    
    try:
        app = create_app()
        with app.app_context():
            # Verificar si ya existe
            existing_admin = Usuario.query.filter_by(email='admin@empresa.com').first()
            
            if existing_admin:
                print("ℹ️  Usuario admin ya existe, actualizando contraseña...")
                existing_admin.set_password('admin123')
                existing_admin.activo = True
                db.session.commit()
                print("✅ Contraseña del admin actualizada")
            else:
                admin_user = Usuario(
                    nombre='Admin Sistema',
                    email='admin@empresa.com',
                    rol='ejecutivo',
                    activo=True
                )
                admin_user.set_password('admin123')
                db.session.add(admin_user)
                db.session.commit()
                print("✅ Usuario admin creado")
            
            # Verificar que funcione
            admin_check = Usuario.query.filter_by(email='admin@empresa.com').first()
            if admin_check and admin_check.check_password('admin123'):
                print("✅ Verificación de contraseña exitosa")
                return True
            else:
                print("❌ Error en la verificación de contraseña")
                return False
                
    except Exception as e:
        print(f"❌ Error creando usuario admin: {str(e)}")
        return False

def create_test_users():
    """Crear usuarios de prueba adicionales"""
    print("👥 Creando usuarios de prueba...")
    
    try:
        app = create_app()
        with app.app_context():
            users_to_create = [
                {
                    'nombre': 'Reclutador Prueba',
                    'email': 'reclutador@empresa.com',
                    'password': 'reclutador123',
                    'rol': 'reclutador'
                },
                {
                    'nombre': 'Líder Reclutamiento',
                    'email': 'lider@empresa.com', 
                    'password': 'lider123',
                    'rol': 'reclutador_lider'
                }
            ]
            
            created_count = 0
            
            for user_data in users_to_create:
                existing = Usuario.query.filter_by(email=user_data['email']).first()
                
                if existing:
                    print(f"   ℹ️  {user_data['email']} ya existe, actualizando...")
                    existing.set_password(user_data['password'])
                    existing.activo = True
                    existing.nombre = user_data['nombre']
                    existing.rol = user_data['rol']
                else:
                    new_user = Usuario(
                        nombre=user_data['nombre'],
                        email=user_data['email'],
                        rol=user_data['rol'],
                        activo=True
                    )
                    new_user.set_password(user_data['password'])
                    db.session.add(new_user)
                    created_count += 1
                    print(f"   ✅ {user_data['email']} creado")
            
            db.session.commit()
            print(f"✅ {created_count} usuarios nuevos creados/actualizados")
            return True
            
    except Exception as e:
        print(f"❌ Error creando usuarios de prueba: {str(e)}")
        return False

def verify_all_users():
    """Verificar todos los usuarios"""
    print("🔍 Verificando todos los usuarios...")
    
    try:
        app = create_app()
        with app.app_context():
            users = Usuario.query.filter_by(activo=True).all()
            
            print(f"📊 Total usuarios activos: {len(users)}")
            
            test_credentials = [
                ('admin@empresa.com', 'admin123'),
                ('reclutador@empresa.com', 'reclutador123'),
                ('lider@empresa.com', 'lider123')
            ]
            
            all_working = True
            
            for email, password in test_credentials:
                user = Usuario.query.filter_by(email=email).first()
                if user:
                    if user.check_password(password):
                        print(f"   ✅ {email} - Contraseña correcta")
                    else:
                        print(f"   ❌ {email} - Contraseña incorrecta")
                        all_working = False
                else:
                    print(f"   ❌ {email} - Usuario no encontrado")
                    all_working = False
            
            return all_working
            
    except Exception as e:
        print(f"❌ Error verificando usuarios: {str(e)}")
        return False

def main():
    print("=" * 70)
    print("🛠️  DIAGNÓSTICO Y REPARACIÓN COMPLETA DEL SISTEMA")
    print("=" * 70)
    print()
    
    success = True
    
    # Paso 1: Verificar conexión DB
    if not check_database_connection():
        print("❌ No se puede continuar sin conexión a la base de datos")
        sys.exit(1)
    print()
    
    # Paso 2: Verificar/crear tablas
    if not check_tables_exist():
        print("⚠️  Tablas no existen, creándolas...")
        if not create_tables():
            success = False
    print()
    
    # Paso 3: Crear usuario admin
    if not create_admin_user():
        success = False
    print()
    
    # Paso 4: Crear usuarios de prueba
    if not create_test_users():
        success = False
    print()
    
    # Paso 5: Verificar todos los usuarios
    if not verify_all_users():
        success = False
    print()
    
    print("=" * 70)
    if success:
        print("✅ SISTEMA REPARADO Y LISTO")
        print()
        print("🔑 Credenciales de acceso:")
        print("   👤 admin@empresa.com / admin123 (Ejecutivo)")
        print("   👤 reclutador@empresa.com / reclutador123 (Reclutador)")
        print("   👤 lider@empresa.com / lider123 (Líder)")
        print()
        print("🚀 Ahora puedes ejecutar:")
        print("   python test_vacants.py")
    else:
        print("❌ ALGUNOS PROBLEMAS PERSISTEN")
        print("💡 Revisa los errores anteriores")
    print("=" * 70)

if __name__ == '__main__':
    main()
