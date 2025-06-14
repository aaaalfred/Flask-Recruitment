#!/usr/bin/env python3
"""
Script completo para iniciar y verificar el sistema de RH
"""
import subprocess
import sys
import time
import requests
import os

def check_python_dependencies():
    """Verificar dependencias de Python"""
    print("🐍 Verificando dependencias de Python...")
    
    try:
        import flask
        import flask_sqlalchemy
        import flask_jwt_extended
        import flask_cors
        import pymysql
        import boto3
        print("✅ Todas las dependencias de Python están instaladas")
        return True
    except ImportError as e:
        print(f"❌ Dependencia faltante: {e}")
        print("💡 Ejecuta: pip install -r requirements.txt")
        return False

def check_database_connection():
    """Verificar conexión a la base de datos"""
    print("🗄️  Verificando conexión a la base de datos...")
    
    try:
        from app import create_app
        from extensions import db
        from sqlalchemy import text
        
        app = create_app()
        with app.app_context():
            # Usar la nueva sintaxis de SQLAlchemy 2.x
            result = db.session.execute(text('SELECT 1'))
            result.fetchone()
        
        print("✅ Conexión a la base de datos exitosa")
        return True
    except Exception as e:
        print(f"❌ Error de conexión a la base de datos: {e}")
        return False

def initialize_database():
    """Inicializar base de datos y crear usuarios de prueba"""
    print("🔧 Inicializando base de datos...")
    
    try:
        from app import create_app
        from extensions import db
        from models import Usuario
        
        app = create_app()
        with app.app_context():
            # Crear tablas
            db.create_all()
            print("✅ Tablas de base de datos creadas/verificadas")
            
            # Crear usuarios de prueba
            admin_exists = Usuario.query.filter_by(email='admin@empresa.com').first()
            if not admin_exists:
                admin_user = Usuario(
                    nombre='Administrador',
                    email='admin@empresa.com',
                    rol='ejecutivo',
                    activo=True
                )
                admin_user.set_password('admin123')
                db.session.add(admin_user)
                db.session.commit()
                print("✅ Usuario administrador creado: admin@empresa.com / admin123")
            else:
                print("ℹ️  Usuario administrador ya existe")
            
        return True
    except Exception as e:
        print(f"❌ Error inicializando base de datos: {e}")
        return False

def start_backend():
    """Iniciar el servidor backend"""
    print("🚀 Iniciando servidor backend...")
    
    try:
        # Verificar si ya está corriendo
        try:
            response = requests.get('http://localhost:5000/api/health', timeout=2)
            if response.status_code == 200:
                print("✅ El backend ya está corriendo")
                return True
        except:
            pass
        
        # Iniciar el servidor
        print("📡 Iniciando servidor Flask...")
        subprocess.Popen([sys.executable, 'app.py'], 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE)
        
        # Esperar a que inicie
        for i in range(10):
            try:
                time.sleep(2)
                response = requests.get('http://localhost:5000/api/health', timeout=2)
                if response.status_code == 200:
                    print("✅ Backend iniciado exitosamente")
                    return True
            except:
                print(f"⏳ Esperando backend... ({i+1}/10)")
        
        print("❌ El backend no pudo iniciar en 20 segundos")
        return False
        
    except Exception as e:
        print(f"❌ Error iniciando backend: {e}")
        return False

def check_frontend():
    """Verificar el frontend"""
    print("🌐 Verificando configuración del frontend...")
    
    # Verificar que existe package.json
    if not os.path.exists('frontend/package.json'):
        print("❌ No se encontró frontend/package.json")
        return False
    
    # Verificar .env
    if not os.path.exists('frontend/.env'):
        print("❌ No se encontró frontend/.env")
        return False
    
    with open('frontend/.env', 'r') as f:
        env_content = f.read()
    
    if 'REACT_APP_API_URL=http://localhost:5000/api' in env_content:
        print("✅ Configuración de frontend correcta")
        return True
    else:
        print("❌ Configuración de frontend incorrecta")
        return False

def test_full_system():
    """Probar el sistema completo"""
    print("🧪 Probando sistema completo...")
    
    try:
        # Test health check
        response = requests.get('http://localhost:5000/api/health', timeout=5)
        if response.status_code != 200:
            print("❌ Health check falló")
            return False
        
        print("✅ Health check exitoso")
        
        # Test login
        login_data = {
            "email": "admin@empresa.com",
            "password": "admin123"
        }
        
        response = requests.post('http://localhost:5000/api/auth/login',
                               json=login_data,
                               headers={'Content-Type': 'application/json'},
                               timeout=5)
        
        if response.status_code == 200:
            print("✅ Login de prueba exitoso")
            data = response.json()
            if 'access_token' in data:
                print("✅ Token JWT generado correctamente")
                return True
            else:
                print("❌ No se generó token JWT")
                return False
        else:
            print(f"❌ Login falló: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error probando sistema: {e}")
        return False

def main():
    """Función principal"""
    print("🎯 SISTEMA DE GESTIÓN RH - VERIFICACIÓN COMPLETA")
    print("=" * 60)
    
    success_count = 0
    total_tests = 6
    
    # Test 1: Dependencias Python
    if check_python_dependencies():
        success_count += 1
    
    # Test 2: Conexión DB
    if check_database_connection():
        success_count += 1
    
    # Test 3: Inicializar DB
    if initialize_database():
        success_count += 1
    
    # Test 4: Iniciar Backend
    if start_backend():
        success_count += 1
    
    # Test 5: Verificar Frontend
    if check_frontend():
        success_count += 1
    
    # Test 6: Prueba completa
    if test_full_system():
        success_count += 1
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN FINAL")
    print("=" * 60)
    print(f"Tests exitosos: {success_count}/{total_tests}")
    
    if success_count == total_tests:
        print("🎉 ¡SISTEMA COMPLETAMENTE FUNCIONAL!")
        print("\n📋 INFORMACIÓN DE ACCESO:")
        print("Backend: http://localhost:5000")
        print("API: http://localhost:5000/api")
        print("Health Check: http://localhost:5000/api/health")
        print("\n👤 USUARIO DE PRUEBA:")
        print("Email: admin@empresa.com")
        print("Password: admin123")
        print("\n🚀 INICIAR FRONTEND:")
        print("cd frontend && npm start")
    else:
        print("❌ El sistema tiene problemas que necesitan resolverse")
        print("\n🔧 PASOS SIGUIENTES:")
        
        if success_count < 1:
            print("1. Instalar dependencias: pip install -r requirements.txt")
        if success_count < 2:
            print("2. Verificar configuración de base de datos en .env")
        if success_count < 4:
            print("3. Revisar configuración del servidor")
        if success_count < 5:
            print("4. Verificar configuración del frontend")

if __name__ == '__main__':
    main()
