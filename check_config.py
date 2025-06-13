#!/usr/bin/env python3
"""
Script para verificar la configuración del sistema antes de ejecutar
"""

import os
import sys
from dotenv import load_dotenv

def check_env_variables():
    """Verificar variables de entorno necesarias"""
    print("🔍 Verificando variables de entorno...")
    
    load_dotenv()
    
    required_vars = [
        'MYSQL_HOST',
        'MYSQL_USER', 
        'MYSQL_PASSWORD',
        'MYSQL_DB',
        'SECRET_KEY',
        'JWT_SECRET_KEY'
    ]
    
    optional_vars = [
        'AWS_ACCESS_KEY_ID',
        'AWS_SECRET_ACCESS_KEY',
        'AWS_S3_BUCKET',
        'AWS_S3_REGION'
    ]
    
    missing_required = []
    missing_optional = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_required.append(var)
        else:
            print(f"✅ {var}: {os.getenv(var)[:10]}..." if len(os.getenv(var)) > 10 else f"✅ {var}: {os.getenv(var)}")
    
    for var in optional_vars:
        if not os.getenv(var):
            missing_optional.append(var)
        else:
            print(f"✅ {var}: {os.getenv(var)[:10]}..." if len(os.getenv(var)) > 10 else f"✅ {var}: {os.getenv(var)}")
    
    if missing_required:
        print(f"❌ Variables requeridas faltantes: {', '.join(missing_required)}")
        return False
    
    if missing_optional:
        print(f"⚠️  Variables opcionales faltantes (para S3): {', '.join(missing_optional)}")
        print("   Las funciones de subida de archivos no funcionarán")
    
    return True

def check_database_config():
    """Verificar configuración de base de datos"""
    print("\n🗄️  Verificando configuración de base de datos...")
    
    try:
        from config import Config
        
        host = Config.MYSQL_HOST
        user = Config.MYSQL_USER
        db = Config.MYSQL_DB
        
        print(f"✅ Host: {host}")
        print(f"✅ Usuario: {user}")
        print(f"✅ Base de datos: {db}")
        
        # Verificar cadena de conexión
        uri = Config.SQLALCHEMY_DATABASE_URI
        if 'mysql+pymysql://' in uri:
            print("✅ Driver MySQL configurado correctamente")
        else:
            print("❌ Driver MySQL no configurado correctamente")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Error en configuración: {str(e)}")
        return False

def check_dependencies():
    """Verificar dependencias instaladas"""
    print("\n📦 Verificando dependencias...")
    
    required_packages = [
        ('flask', 'flask'),
        ('flask_sqlalchemy', 'flask_sqlalchemy'),
        ('flask_login', 'flask_login'),
        ('flask_jwt_extended', 'flask_jwt_extended'),
        ('flask_cors', 'flask_cors'),
        ('flask_migrate', 'flask_migrate'),
        ('pymysql', 'pymysql'),
        ('boto3', 'boto3'),
        ('python_dotenv', 'dotenv'),
        ('werkzeug', 'werkzeug')
    ]
    
    missing_packages = []
    
    for display_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"✅ {display_name}")
        except ImportError:
            missing_packages.append(display_name)
            print(f"❌ {display_name}")
    
    if missing_packages:
        print(f"\n❌ Paquetes faltantes: {', '.join(missing_packages)}")
        print("Ejecuta: pip install -r requirements.txt")
        return False
    
    return True

def test_database_connection():
    """Probar conexión a la base de datos"""
    print("\n🔌 Probando conexión a la base de datos...")
    
    try:
        from app import create_app, db
        app = create_app()
        
        with app.app_context():
            result = db.session.execute(db.text('SELECT 1'))
            print("✅ Conexión exitosa")
            return True
            
    except Exception as e:
        print(f"❌ Error de conexión: {str(e)}")
        print("\nPosibles soluciones:")
        print("1. Verificar que MySQL esté ejecutándose")
        print("2. Verificar credenciales en .env")
        print("3. Verificar que la base de datos exista")
        print("4. Verificar conectividad de red")
        return False

def main():
    """Función principal de verificación"""
    print("🔧 VERIFICACIÓN DE CONFIGURACIÓN")
    print("=" * 50)
    
    checks = [
        ("Variables de entorno", check_env_variables),
        ("Configuración de BD", check_database_config),
        ("Dependencias", check_dependencies),
        ("Conexión a BD", test_database_connection)
    ]
    
    all_passed = True
    
    for name, check_func in checks:
        try:
            if not check_func():
                all_passed = False
        except Exception as e:
            print(f"❌ Error en {name}: {str(e)}")
            all_passed = False
        
        print("-" * 30)
    
    print("=" * 50)
    if all_passed:
        print("✅ TODAS LAS VERIFICACIONES PASARON")
        print("\nPuedes continuar con:")
        print("1. flask db init")
        print("2. flask db migrate -m 'Initial migration'")
        print("3. flask db upgrade")
        print("4. python init_data.py")
        print("5. python app.py")
    else:
        print("❌ ALGUNAS VERIFICACIONES FALLARON")
        print("Corrige los errores antes de continuar")
        sys.exit(1)

if __name__ == '__main__':
    main()
