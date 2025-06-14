#!/usr/bin/env python3
"""
Script de testing directo para resolver el error HTTP 422
Con la base de datos correcta configurada
"""

import requests
import json

def test_backend_connection():
    """Verificar conexión básica al backend"""
    print("🔗 Testing conexión al backend...")
    
    try:
        # Test simple al endpoint de login (sin datos)
        response = requests.get('http://localhost:5000/api/auth/login', timeout=5)
        print(f"✅ Backend responde - Status: {response.status_code}")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Backend NO está corriendo en http://localhost:5000")
        print("   Ejecutar: cd C:\\Users\\ADMIN\\code\\rh && python app.py")
        return False
    except Exception as e:
        print(f"⚠️  Backend responde pero hay un error: {str(e)}")
        return True  # El backend está corriendo

def test_login():
    """Test del login para obtener token JWT"""
    print("\n🔐 Testing login...")
    
    login_data = {
        'email': 'admin@empresa.com',
        'password': 'password123'
    }
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(
            'http://localhost:5000/api/auth/login',
            json=login_data,
            headers=headers,
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            user = data.get('user')
            
            print(f"✅ Login exitoso")
            print(f"   Usuario: {user.get('nombre')} ({user.get('rol')})")
            print(f"   Token: {token[:50]}...")
            
            return token, user
        else:
            print(f"❌ Login falló")
            print(f"   Response: {response.text}")
            return None, None
            
    except Exception as e:
        print(f"❌ Error en login: {str(e)}")
        return None, None

def test_get_usuarios(token):
    """Test específico del endpoint GET usuarios que está fallando"""
    print("\n📋 Testing GET /api/usuarios (el que falla con 422)...")
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # URL exacta que usa el frontend
    url = 'http://localhost:5000/api/usuarios?page=1&per_page=10'
    
    print(f"URL: {url}")
    print(f"Headers: {json.dumps(headers, indent=2)}")
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ GET usuarios exitoso")
            print(f"   Total usuarios: {data.get('total', 0)}")
            print(f"   Usuarios en respuesta: {len(data.get('usuarios', []))}")
            return True, data
            
        elif response.status_code == 422:
            print(f"❌ ERROR 422 ENCONTRADO!")
            print(f"   Response body: {response.text}")
            
            # Intentar parsear como JSON para ver el error específico
            try:
                error_data = response.json()
                print(f"   Error JSON: {json.dumps(error_data, indent=2)}")
            except:
                print(f"   Error no es JSON válido")
            
            return False, None
            
        else:
            print(f"❌ Otro error - Status: {response.status_code}")
            print(f"   Response: {response.text}")
            return False, None
            
    except Exception as e:
        print(f"❌ Excepción en GET usuarios: {str(e)}")
        return False, None

def test_post_usuario(token):
    """Test específico del endpoint POST usuarios"""
    print("\n👤 Testing POST /api/usuarios (creación que también falla)...")
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Datos exactos como los envía el frontend
    user_data = {
        'nombre': 'Test Usuario 422',
        'email': 'test422@empresa.com',
        'password': 'test123',
        'rol': 'reclutador'
    }
    
    url = 'http://localhost:5000/api/usuarios'
    
    print(f"URL: {url}")
    print(f"Headers: {json.dumps(headers, indent=2)}")
    print(f"Data: {json.dumps(user_data, indent=2)}")
    
    try:
        response = requests.post(url, json=user_data, headers=headers, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 201:
            data = response.json()
            print(f"✅ POST usuario exitoso")
            print(f"   Usuario creado: {data.get('usuario', {}).get('nombre')}")
            
            # Limpiar usuario de prueba
            user_id = data.get('usuario', {}).get('id')
            if user_id:
                cleanup_user(token, user_id)
            
            return True, data
            
        elif response.status_code == 422:
            print(f"❌ ERROR 422 ENCONTRADO!")
            print(f"   Response body: {response.text}")
            
            try:
                error_data = response.json()
                print(f"   Error JSON: {json.dumps(error_data, indent=2)}")
            except:
                print(f"   Error no es JSON válido")
            
            return False, None
            
        else:
            print(f"❌ Otro error - Status: {response.status_code}")
            print(f"   Response: {response.text}")
            return False, None
            
    except Exception as e:
        print(f"❌ Excepción en POST usuario: {str(e)}")
        return False, None

def cleanup_user(token, user_id):
    """Limpiar usuario de prueba"""
    print(f"\n🧹 Limpiando usuario de prueba ID: {user_id}")
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.delete(f'http://localhost:5000/api/usuarios/{user_id}', headers=headers)
        if response.status_code == 200:
            print(f"✅ Usuario de prueba eliminado")
        else:
            print(f"⚠️  No se pudo eliminar usuario de prueba: {response.text}")
    except Exception as e:
        print(f"⚠️  Error eliminando usuario: {str(e)}")

def main():
    """Función principal de debugging específico para error 422"""
    print("🔧 DEBUGGING ESPECÍFICO - ERROR HTTP 422")
    print("Con base de datos recruitment_system correctamente configurada")
    print("=" * 70)
    
    # 1. Verificar backend
    if not test_backend_connection():
        return
    
    # 2. Test login
    token, user = test_login()
    if not token:
        print("\n❌ PROBLEMA: No se puede obtener token JWT")
        return
    
    print(f"\n📊 Usuario logueado:")
    print(f"   Nombre: {user.get('nombre')}")
    print(f"   Email: {user.get('email')}")
    print(f"   Rol: {user.get('rol')}")
    print(f"   Activo: {user.get('activo')}")
    
    # 3. Test GET usuarios (el que falla con 422)
    get_success, get_data = test_get_usuarios(token)
    
    # 4. Test POST usuario (también falla con 422)
    post_success, post_data = test_post_usuario(token)
    
    # 5. Diagnóstico final
    print("\n" + "=" * 70)
    print("📋 DIAGNÓSTICO FINAL:")
    
    if get_success and post_success:
        print("✅ PROBLEMA RESUELTO: Todos los endpoints funcionan correctamente")
    elif not get_success and not post_success:
        print("❌ PROBLEMA CONFIRMADO: Ambos endpoints fallan con 422")
        print("\n🔍 Posibles causas:")
        print("   1. Problema en el decorador @token_required")
        print("   2. Problema en el decorador @role_required")
        print("   3. Problema con la validación JWT")
        print("   4. Problema en el backend con SQLAlchemy")
        print("   5. Problema de CORS")
    elif get_success and not post_success:
        print("⚠️  Solo GET funciona, POST falla - Problema con @role_required")
    else:
        print("⚠️  Solo POST funciona, GET falla - Problema extraño")

if __name__ == '__main__':
    main()
