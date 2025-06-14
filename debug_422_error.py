#!/usr/bin/env python3
"""
Script para debuggear el error HTTP 422 en la gestión de usuarios
Analiza paso a paso dónde está el problema
"""

import requests
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import Usuario, db
from app import create_app

def test_login_and_get_token():
    """Test login y obtener token JWT"""
    print("🔐 Testing login...")
    
    login_data = {
        'email': 'admin@empresa.com',
        'password': 'password123'
    }
    
    try:
        response = requests.post('http://localhost:5000/api/auth/login', 
                               json=login_data, 
                               headers={'Content-Type': 'application/json'})
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            token = data['access_token']
            user = data['user']
            print(f"✅ Login exitoso")
            print(f"   Token: {token[:50]}...")
            print(f"   Usuario: {user['nombre']} ({user['rol']})")
            return token, user
        else:
            print(f"❌ Login falló: {response.text}")
            return None, None
            
    except Exception as e:
        print(f"❌ Error en login: {str(e)}")
        return None, None

def test_get_usuarios_endpoint(token):
    """Test endpoint GET /api/usuarios"""
    print("\n📋 Testing GET /api/usuarios...")
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get('http://localhost:5000/api/usuarios?page=1&per_page=10', 
                               headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print(f"Headers enviados: {headers}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ GET usuarios exitoso")
            print(f"   Total usuarios: {data.get('total', 0)}")
            print(f"   Usuarios en página: {len(data.get('usuarios', []))}")
            return True
        else:
            print(f"❌ GET usuarios falló")
            print(f"   Response: {response.text}")
            print(f"   Headers de respuesta: {dict(response.headers)}")
            return False
            
    except Exception as e:
        print(f"❌ Error en GET usuarios: {str(e)}")
        return False

def test_create_usuario_endpoint(token, user_data):
    """Test endpoint POST /api/usuarios"""
    print("\n👤 Testing POST /api/usuarios...")
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post('http://localhost:5000/api/usuarios', 
                                json=user_data,
                                headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print(f"Data enviada: {json.dumps(user_data, indent=2)}")
        print(f"Headers enviados: {headers}")
        
        if response.status_code == 201:
            data = response.json()
            print(f"✅ POST usuario exitoso")
            print(f"   Usuario creado: {data.get('usuario', {}).get('nombre')}")
            return True, data
        else:
            print(f"❌ POST usuario falló")
            print(f"   Response: {response.text}")
            print(f"   Headers de respuesta: {dict(response.headers)}")
            return False, None
            
    except Exception as e:
        print(f"❌ Error en POST usuario: {str(e)}")
        return False, None

def verify_user_permissions(user):
    """Verificar permisos del usuario"""
    print(f"\n🔍 Verificando permisos del usuario...")
    print(f"   Nombre: {user['nombre']}")
    print(f"   Email: {user['email']}")
    print(f"   Rol: {user['rol']}")
    print(f"   Activo: {user['activo']}")
    
    # Verificar si el rol permite crear usuarios
    allowed_roles = ['ejecutivo', 'reclutador_lider']
    if user['rol'] in allowed_roles:
        print(f"✅ El rol '{user['rol']}' TIENE permisos para crear usuarios")
        return True
    else:
        print(f"❌ El rol '{user['rol']}' NO tiene permisos para crear usuarios")
        print(f"   Roles permitidos: {allowed_roles}")
        return False

def test_direct_database_access():
    """Test acceso directo a la base de datos"""
    print(f"\n🗄️ Testing acceso directo a base de datos...")
    
    try:
        app = create_app()
        with app.app_context():
            # Verificar usuario admin
            admin_user = Usuario.query.filter_by(email='admin@empresa.com').first()
            if admin_user:
                print(f"✅ Usuario admin encontrado en DB")
                print(f"   ID: {admin_user.id}")
                print(f"   Nombre: {admin_user.nombre}")
                print(f"   Email: {admin_user.email}")
                print(f"   Rol: {admin_user.rol}")
                print(f"   Activo: {admin_user.activo}")
                
                # Verificar password
                if admin_user.check_password('password123'):
                    print(f"✅ Password correcto")
                else:
                    print(f"❌ Password incorrecto")
                
                return admin_user.to_dict()
            else:
                print(f"❌ Usuario admin NO encontrado en DB")
                return None
                
    except Exception as e:
        print(f"❌ Error accediendo a DB: {str(e)}")
        return None

def check_backend_running():
    """Verificar que el backend esté corriendo"""
    print(f"🚀 Verificando backend...")
    
    try:
        response = requests.get('http://localhost:5000/api/auth/login', timeout=5)
        print(f"✅ Backend corriendo en http://localhost:5000")
        return True
    except requests.exceptions.ConnectionError:
        print(f"❌ Backend NO está corriendo en http://localhost:5000")
        print(f"   Ejecutar: cd C:\\Users\\ADMIN\\code\\rh && python app.py")
        return False
    except Exception as e:
        print(f"❌ Error verificando backend: {str(e)}")
        return False

def main():
    """Función principal de debugging"""
    print("🔧 DEBUGGING ERROR HTTP 422 - GESTIÓN DE USUARIOS")
    print("=" * 60)
    
    # 1. Verificar backend
    if not check_backend_running():
        return
    
    # 2. Verificar acceso directo a DB
    db_user = test_direct_database_access()
    if not db_user:
        return
    
    # 3. Test login
    token, logged_user = test_login_and_get_token()
    if not token:
        return
    
    # 4. Verificar permisos
    has_permissions = verify_user_permissions(logged_user)
    if not has_permissions:
        print(f"\n⚠️  PROBLEMA ENCONTRADO: Usuario sin permisos suficientes")
        return
    
    # 5. Test GET usuarios (debería funcionar para cualquier usuario autenticado)
    get_success = test_get_usuarios_endpoint(token)
    if not get_success:
        print(f"\n⚠️  PROBLEMA ENCONTRADO: Error en GET /api/usuarios")
        return
    
    # 6. Test POST usuario (requiere permisos específicos)
    test_user_data = {
        'nombre': 'Usuario de Prueba Debug',
        'email': 'debug.test@empresa.com',
        'password': 'debug123',
        'rol': 'reclutador'
    }
    
    create_success, created_user = test_create_usuario_endpoint(token, test_user_data)
    if not create_success:
        print(f"\n⚠️  PROBLEMA ENCONTRADO: Error en POST /api/usuarios")
    else:
        print(f"\n✅ TODOS LOS TESTS PASARON EXITOSAMENTE")
        
        # Limpiar usuario de prueba
        print(f"\n🧹 Limpiando usuario de prueba...")
        if created_user and created_user.get('usuario'):
            user_id = created_user['usuario']['id']
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            delete_response = requests.delete(f'http://localhost:5000/api/usuarios/{user_id}', headers=headers)
            if delete_response.status_code == 200:
                print(f"✅ Usuario de prueba eliminado")
            else:
                print(f"⚠️  No se pudo eliminar usuario de prueba: {delete_response.text}")

if __name__ == '__main__':
    main()
