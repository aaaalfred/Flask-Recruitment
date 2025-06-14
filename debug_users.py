#!/usr/bin/env python3
"""
Script para verificar usuarios existentes y el login
"""
from app import create_app
from extensions import db
from models import Usuario
import requests
import json

def check_users():
    """Verificar usuarios existentes"""
    app = create_app()
    
    with app.app_context():
        try:
            print("👥 Verificando usuarios en la base de datos...")
            
            # Obtener todos los usuarios
            all_users = Usuario.query.all()
            active_users = Usuario.query.filter_by(activo=True).all()
            
            print(f"📊 Total usuarios: {len(all_users)}")
            print(f"📊 Usuarios activos: {len(active_users)}")
            print()
            
            if active_users:
                print("📋 Usuarios activos encontrados:")
                for user in active_users:
                    print(f"   • ID: {user.id}")
                    print(f"     Email: {user.email}")
                    print(f"     Nombre: {user.nombre}")
                    print(f"     Rol: {user.rol}")
                    print(f"     Activo: {user.activo}")
                    print()
            else:
                print("⚠️  No se encontraron usuarios activos")
                
            return active_users
            
        except Exception as e:
            print(f"❌ Error verificando usuarios: {str(e)}")
            return []

def test_password_verification():
    """Probar verificación de contraseñas directamente"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🔐 Probando verificación de contraseñas...")
            
            # Buscar usuario admin
            admin_user = Usuario.query.filter_by(email='admin@empresa.com').first()
            
            if admin_user:
                print(f"✅ Usuario admin encontrado: {admin_user.email}")
                
                # Probar contraseña
                if admin_user.check_password('admin123'):
                    print("✅ Contraseña 'admin123' es correcta")
                else:
                    print("❌ Contraseña 'admin123' es incorrecta")
                    
                    # Intentar resetear la contraseña
                    print("🔄 Reseteando contraseña...")
                    admin_user.set_password('admin123')
                    db.session.commit()
                    print("✅ Contraseña reseteada a 'admin123'")
                    
                    # Probar de nuevo
                    if admin_user.check_password('admin123'):
                        print("✅ Verificación exitosa después del reset")
                    else:
                        print("❌ Aún hay problemas con la contraseña")
            else:
                print("❌ Usuario admin no encontrado")
                
        except Exception as e:
            print(f"❌ Error verificando contraseñas: {str(e)}")

def test_api_login():
    """Probar login vía API"""
    print("🌐 Probando login vía API...")
    
    BASE_URL = 'http://localhost:5000/api'
    headers = {'Content-Type': 'application/json'}
    
    # Primero verificar que el servidor esté respondiendo
    try:
        health_response = requests.get(f'{BASE_URL}/health', timeout=5)
        print(f"🏥 Health check: {health_response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Servidor no responde: {e}")
        print("💡 Asegúrate de que el servidor esté corriendo con: python app.py")
        return None
    
    # Probar diferentes combinaciones de login
    test_credentials = [
        ('admin@empresa.com', 'admin123'),
        ('reclutador@empresa.com', 'reclutador123'),
        ('lider@empresa.com', 'lider123')
    ]
    
    for email, password in test_credentials:
        try:
            login_data = {'email': email, 'password': password}
            response = requests.post(f'{BASE_URL}/auth/login', 
                                   json=login_data, 
                                   headers=headers,
                                   timeout=10)
            
            print(f"🔐 Login {email}: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Login exitoso")
                print(f"   👤 Usuario: {data.get('user', {}).get('nombre', 'N/A')}")
                print(f"   🎭 Rol: {data.get('user', {}).get('rol', 'N/A')}")
                return data['access_token']
            else:
                print(f"   ❌ Error: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Error de conexión: {e}")
    
    return None

def main():
    print("=" * 60)
    print("🔍 DIAGNÓSTICO DE USUARIOS Y LOGIN")
    print("=" * 60)
    print()
    
    # Paso 1: Verificar usuarios en base de datos
    users = check_users()
    print()
    
    # Paso 2: Verificar contraseñas directamente
    test_password_verification()
    print()
    
    # Paso 3: Probar login vía API
    token = test_api_login()
    
    print()
    print("=" * 60)
    
    if token:
        print("✅ DIAGNÓSTICO EXITOSO")
        print("🎯 El login funciona correctamente")
        print(f"🔑 Token obtenido: {token[:50]}...")
    else:
        print("❌ PROBLEMAS DETECTADOS")
        print("💡 Sugerencias:")
        print("   1. Ejecutar: python init_users.py")
        print("   2. Verificar que el servidor esté corriendo")
        print("   3. Verificar la configuración de la base de datos")
    
    print("=" * 60)

if __name__ == '__main__':
    main()
