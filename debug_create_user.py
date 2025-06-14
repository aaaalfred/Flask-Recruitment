#!/usr/bin/env python3
"""
Script específico para debuggear la creación de usuarios
Identifica exactamente por qué falla
"""

import requests
import json

def test_login():
    """Test del login para obtener token"""
    print("🔐 Testing login...")
    
    login_data = {
        'email': 'admin@empresa.com',
        'password': 'password123'
    }
    
    try:
        response = requests.post(
            'http://localhost:5000/api/auth/login',
            json=login_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            user = data.get('user')
            
            print(f"✅ Login exitoso")
            print(f"   Usuario: {user.get('nombre')} ({user.get('rol')})")
            print(f"   ID: {user.get('id')}")
            print(f"   Token: {token[:50]}...")
            
            return token, user
        else:
            print(f"❌ Login falló: {response.text}")
            return None, None
            
    except Exception as e:
        print(f"❌ Error en login: {str(e)}")
        return None, None

def test_get_usuarios(token):
    """Test GET usuarios (debería funcionar)"""
    print("\n📋 Testing GET /api/usuarios...")
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(
            'http://localhost:5000/api/usuarios?page=1&per_page=10',
            headers=headers,
            timeout=10
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ GET usuarios exitoso")
            print(f"   Total usuarios: {data.get('total', 0)}")
            return True
        else:
            print(f"❌ GET usuarios falló: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error en GET usuarios: {str(e)}")
        return False

def test_create_usuario_detailed(token):
    """Test detallado de creación de usuario"""
    print("\n👤 Testing POST /api/usuarios (DETALLADO)...")
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Datos de prueba
    user_data = {
        'nombre': 'Usuario Test Debug',
        'email': 'debug.test.nuevo@empresa.com',
        'password': 'debug123',
        'rol': 'reclutador'
    }
    
    print(f"URL: http://localhost:5000/api/usuarios")
    print(f"Headers: {json.dumps(headers, indent=2)}")
    print(f"Data: {json.dumps(user_data, indent=2)}")
    
    try:
        response = requests.post(
            'http://localhost:5000/api/usuarios',
            json=user_data,
            headers=headers,
            timeout=10
        )
        
        print(f"\nRespuesta:")
        print(f"Status Code: {response.status_code}")
        print(f"Headers de respuesta: {dict(response.headers)}")
        print(f"Content-Type: {response.headers.get('Content-Type', 'N/A')}")
        
        try:
            response_data = response.json()
            print(f"Response JSON: {json.dumps(response_data, indent=2)}")
        except:
            print(f"Response Text: {response.text}")
        
        if response.status_code == 201:
            print(f"✅ Usuario creado exitosamente")
            return True, response_data
        elif response.status_code == 400:
            print(f"❌ Error 400 - Datos inválidos")
            return False, None
        elif response.status_code == 403:
            print(f"❌ Error 403 - Sin permisos")
            return False, None
        elif response.status_code == 422:
            print(f"❌ Error 422 - Datos no procesables")
            return False, None
        elif response.status_code == 500:
            print(f"❌ Error 500 - Error interno del servidor")
            return False, None
        else:
            print(f"❌ Error inesperado - Status: {response.status_code}")
            return False, None
            
    except Exception as e:
        print(f"❌ Excepción en creación de usuario: {str(e)}")
        return False, None

def test_permissions_specifically(token):
    """Test específico de permisos"""
    print("\n🔒 Testing permisos específicos...")
    
    # Intentar sin Authorization header
    print("\n1. Probando SIN header Authorization:")
    try:
        response = requests.post(
            'http://localhost:5000/api/usuarios',
            json={'nombre': 'test', 'email': 'test@test.com', 'password': '123', 'rol': 'reclutador'},
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        print(f"   Status: {response.status_code} - {response.text[:100]}")
    except Exception as e:
        print(f"   Error: {str(e)}")
    
    # Intentar con token malformado
    print("\n2. Probando con token MALFORMADO:")
    try:
        response = requests.post(
            'http://localhost:5000/api/usuarios',
            json={'nombre': 'test', 'email': 'test@test.com', 'password': '123', 'rol': 'reclutador'},
            headers={
                'Authorization': 'Bearer TOKEN_FALSO',
                'Content-Type': 'application/json'
            },
            timeout=5
        )
        print(f"   Status: {response.status_code} - {response.text[:100]}")
    except Exception as e:
        print(f"   Error: {str(e)}")
    
    # Intentar con token correcto pero datos inválidos
    print("\n3. Probando con token CORRECTO pero datos INVÁLIDOS:")
    try:
        response = requests.post(
            'http://localhost:5000/api/usuarios',
            json={'nombre': ''},  # Nombre vacío, debería dar error 400
            headers={
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            },
            timeout=5
        )
        print(f"   Status: {response.status_code} - {response.text[:100]}")
    except Exception as e:
        print(f"   Error: {str(e)}")

def cleanup_test_user(token):
    """Limpiar usuario de prueba si se creó"""
    print("\n🧹 Limpiando usuarios de prueba...")
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Buscar usuario de prueba
    try:
        response = requests.get(
            'http://localhost:5000/api/usuarios?page=1&per_page=50',
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            usuarios = data.get('usuarios', [])
            
            for usuario in usuarios:
                if 'debug.test' in usuario.get('email', ''):
                    user_id = usuario.get('id')
                    print(f"   Eliminando usuario de prueba ID: {user_id}")
                    
                    delete_response = requests.delete(
                        f'http://localhost:5000/api/usuarios/{user_id}',
                        headers=headers
                    )
                    
                    if delete_response.status_code == 200:
                        print(f"   ✅ Usuario eliminado")
                    else:
                        print(f"   ⚠️ No se pudo eliminar: {delete_response.text}")
                        
    except Exception as e:
        print(f"   Error limpiando: {str(e)}")

def main():
    """Función principal de debugging"""
    print("🔧 DEBUGGING ESPECÍFICO - CREACIÓN DE USUARIOS")
    print("=" * 60)
    
    # 1. Test login
    token, user = test_login()
    if not token:
        print("\n❌ PROBLEMA: Login falla")
        return
    
    # 2. Verificar que GET funciona
    if not test_get_usuarios(token):
        print("\n❌ PROBLEMA: GET usuarios falla")
        return
    
    print(f"\n✅ Login y GET funcionan. Usuario: {user.get('rol')}")
    
    # 3. Test específico de permisos
    test_permissions_specifically(token)
    
    # 4. Test detallado de creación
    success, data = test_create_usuario_detailed(token)
    
    # 5. Limpiar
    cleanup_test_user(token)
    
    # 6. Diagnóstico final
    print("\n" + "=" * 60)
    print("📋 DIAGNÓSTICO:")
    
    if success:
        print("✅ CREACIÓN DE USUARIOS FUNCIONA CORRECTAMENTE")
        print("   El problema podría estar en el frontend")
    else:
        print("❌ CREACIÓN DE USUARIOS FALLA EN EL BACKEND")
        print("   Revisar logs del servidor Flask para más detalles")

if __name__ == '__main__':
    main()
