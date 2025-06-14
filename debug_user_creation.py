#!/usr/bin/env python3
"""
Script para debuggear específicamente la creación de usuarios
El login funciona, pero la creación no
"""

import requests
import json
import time

def test_login_get_token():
    """Test login para obtener token válido"""
    print("🔐 Step 1: Testing login para obtener token...")
    
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
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            user = data.get('user')
            
            print(f"   ✅ Login exitoso")
            print(f"   Usuario: {user.get('nombre')} ({user.get('rol')})")
            print(f"   Token: {token[:30]}...")
            
            return token, user
        else:
            print(f"   ❌ Login falló: {response.text}")
            return None, None
            
    except Exception as e:
        print(f"   ❌ Error en login: {str(e)}")
        return None, None

def test_user_creation_detailed(token):
    """Test detallado de creación de usuario"""
    print(f"\n👤 Step 2: Testing creación de usuario (detallado)...")
    
    # Datos del usuario a crear
    user_data = {
        'nombre': 'Test Debug Usuario',
        'email': 'debug.test.usuario@empresa.com',
        'password': 'debug123',
        'rol': 'reclutador'
    }
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    print(f"   URL: http://localhost:5000/api/usuarios")
    print(f"   Method: POST")
    print(f"   Headers: {json.dumps(headers, indent=6)}")
    print(f"   Data: {json.dumps(user_data, indent=6)}")
    
    try:
        print(f"\n   📡 Enviando petición...")
        response = requests.post(
            'http://localhost:5000/api/usuarios',
            json=user_data,
            headers=headers,
            timeout=15
        )
        
        print(f"   📨 Respuesta recibida:")
        print(f"   Status Code: {response.status_code}")
        print(f"   Status Text: {response.reason}")
        print(f"   Response Headers: {dict(response.headers)}")
        
        # Intentar parsear la respuesta
        try:
            response_data = response.json()
            print(f"   Response Body (JSON):")
            print(f"   {json.dumps(response_data, indent=6, ensure_ascii=False)}")
        except:
            print(f"   Response Body (Text):")
            print(f"   {response.text}")
        
        # Análisis por código de estado
        if response.status_code == 201:
            print(f"\n   ✅ Usuario creado exitosamente!")
            return True, response_data
        elif response.status_code == 400:
            print(f"\n   ❌ Error 400: Datos inválidos o campos faltantes")
            return False, response_data
        elif response.status_code == 401:
            print(f"\n   ❌ Error 401: Token inválido o expirado")
            return False, None
        elif response.status_code == 403:
            print(f"\n   ❌ Error 403: Sin permisos suficientes")
            return False, None
        elif response.status_code == 422:
            print(f"\n   ❌ Error 422: Problema de validación")
            return False, response_data
        elif response.status_code == 500:
            print(f"\n   ❌ Error 500: Error interno del servidor")
            return False, None
        else:
            print(f"\n   ⚠️  Error inesperado: {response.status_code}")
            return False, None
            
    except requests.exceptions.Timeout:
        print(f"   ❌ Timeout: El servidor tardó más de 15 segundos en responder")
        return False, None
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Connection Error: No se puede conectar al servidor")
        return False, None
    except Exception as e:
        print(f"   ❌ Error inesperado: {str(e)}")
        return False, None

def test_user_permissions(user):
    """Verificar permisos del usuario logueado"""
    print(f"\n🔍 Step 3: Verificando permisos del usuario...")
    
    print(f"   Usuario: {user.get('nombre')}")
    print(f"   Email: {user.get('email')}")
    print(f"   Rol: {user.get('rol')}")
    print(f"   Activo: {user.get('activo')}")
    
    # Verificar si tiene permisos para crear usuarios
    allowed_roles = ['ejecutivo', 'reclutador_lider']
    user_role = user.get('rol')
    
    if user_role in allowed_roles:
        print(f"   ✅ El rol '{user_role}' TIENE permisos para crear usuarios")
        print(f"   Roles permitidos: {allowed_roles}")
        return True
    else:
        print(f"   ❌ El rol '{user_role}' NO tiene permisos para crear usuarios")
        print(f"   Roles permitidos: {allowed_roles}")
        return False

def test_email_uniqueness():
    """Verificar si el email que intentamos usar ya existe"""
    print(f"\n📧 Step 4: Verificando email único...")
    
    test_email = 'debug.test.usuario@empresa.com'
    
    # Simular consulta directa a la base de datos
    print(f"   Email a probar: {test_email}")
    print(f"   (Esto debería ser único en la base de datos)")
    
    # Nota: Esta verificación se hace en el backend automáticamente
    print(f"   ✅ El backend verificará automáticamente si el email es único")

def cleanup_test_user(token):
    """Limpiar usuario de prueba si fue creado"""
    print(f"\n🧹 Step 5: Limpieza de usuario de prueba...")
    
    # Intentar obtener lista de usuarios para encontrar el que creamos
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(
            'http://localhost:5000/api/usuarios?page=1&per_page=50',
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            usuarios = data.get('usuarios', [])
            
            # Buscar usuario de prueba
            test_user = next(
                (u for u in usuarios if u.get('email') == 'debug.test.usuario@empresa.com'),
                None
            )
            
            if test_user:
                user_id = test_user.get('id')
                print(f"   🗑️  Eliminando usuario de prueba ID: {user_id}")
                
                delete_response = requests.delete(
                    f'http://localhost:5000/api/usuarios/{user_id}',
                    headers=headers,
                    timeout=10
                )
                
                if delete_response.status_code == 200:
                    print(f"   ✅ Usuario de prueba eliminado exitosamente")
                else:
                    print(f"   ⚠️  No se pudo eliminar: {delete_response.text}")
            else:
                print(f"   ℹ️  No se encontró usuario de prueba para eliminar")
        else:
            print(f"   ⚠️  No se pudo obtener lista de usuarios para limpieza")
            
    except Exception as e:
        print(f"   ⚠️  Error en limpieza: {str(e)}")

def main():
    """Función principal de debugging"""
    print("🔧 DEBUGGING ESPECÍFICO - CREACIÓN DE USUARIOS")
    print("Login funciona ✅, pero creación de usuarios falla ❌")
    print("=" * 70)
    
    # Step 1: Login
    token, user = test_login_get_token()
    if not token:
        print("\n❌ PROBLEMA: No se puede obtener token JWT")
        return
    
    # Step 2: Verificar permisos
    has_permissions = test_user_permissions(user)
    if not has_permissions:
        print("\n❌ PROBLEMA: Usuario sin permisos para crear usuarios")
        return
    
    # Step 3: Verificar unicidad de email
    test_email_uniqueness()
    
    # Step 4: Intentar crear usuario
    success, result = test_user_creation_detailed(token)
    
    # Step 5: Análisis de resultados
    print(f"\n" + "=" * 70)
    print(f"📊 RESULTADO DEL DEBUGGING:")
    
    if success:
        print(f"✅ PROBLEMA RESUELTO: La creación de usuarios funciona correctamente")
        cleanup_test_user(token)
    else:
        print(f"❌ PROBLEMA PERSISTE: La creación de usuarios sigue fallando")
        
        if result and isinstance(result, dict):
            error_message = result.get('message', 'Error desconocido')
            print(f"   Error específico: {error_message}")
        
        print(f"\n🔍 PRÓXIMOS PASOS PARA INVESTIGAR:")
        print(f"   1. Revisar logs del servidor Flask en la terminal")
        print(f"   2. Verificar el decorador @role_required en usuario_routes.py")
        print(f"   3. Comprobar validaciones en el modelo Usuario")
        print(f"   4. Verificar configuración de la base de datos")

if __name__ == '__main__':
    main()
