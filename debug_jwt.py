#!/usr/bin/env python3
"""
Diagnóstico específico del problema JWT
"""

import requests
import json
import jwt
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_jwt_diagnosis():
    print("🔐 DIAGNÓSTICO JWT - SIGNATURE VERIFICATION FAILED")
    print("=" * 60)
    
    # 1. Test login para obtener token
    print("1️⃣ Obteniendo token del login...")
    login_response = requests.post(
        'http://localhost:5000/api/auth/login',
        json={'email': 'admin@empresa.com', 'password': 'password123'},
        headers={'Content-Type': 'application/json'}
    )
    
    if login_response.status_code != 200:
        print(f"❌ Login falló: {login_response.text}")
        return
    
    token = login_response.json()['access_token']
    user = login_response.json()['user']
    
    print(f"✅ Token obtenido:")
    print(f"   Length: {len(token)}")
    print(f"   Preview: {token[:50]}...")
    print(f"   User ID: {user['id']} (type: {type(user['id'])})")
    print(f"   User: {user['nombre']} ({user['rol']})")
    
    # 2. Decodificar token sin verificar para ver el contenido
    print(f"\n2️⃣ Decodificando token (sin verificar)...")
    try:
        # Decodificar sin verificar la firma
        decoded_unverified = jwt.decode(token, options={"verify_signature": False})
        print(f"✅ Token decodificado:")
        print(f"   Content: {json.dumps(decoded_unverified, indent=2)}")
        
        # Verificar el header
        header = jwt.get_unverified_header(token)
        print(f"   Header: {json.dumps(header, indent=2)}")
        
    except Exception as e:
        print(f"❌ Error decodificando token: {str(e)}")
        return
    
    # 3. Test GET usuarios (que debería funcionar)
    print(f"\n3️⃣ Probando GET usuarios (debería funcionar)...")
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    get_response = requests.get(
        'http://localhost:5000/api/usuarios?page=1&per_page=5',
        headers=headers
    )
    
    print(f"Status: {get_response.status_code}")
    if get_response.status_code == 200:
        print(f"✅ GET usuarios funciona correctamente")
        data = get_response.json()
        print(f"   Usuarios encontrados: {len(data.get('usuarios', []))}")
    else:
        print(f"❌ GET usuarios falló:")
        try:
            error = get_response.json()
            print(f"   Error: {json.dumps(error, indent=2)}")
        except:
            print(f"   Text: {get_response.text}")
    
    # 4. Test POST usuarios (el que falla)
    print(f"\n4️⃣ Probando POST usuarios (el que falla)...")
    
    user_data = {
        'nombre': 'Debug JWT User',
        'email': 'debug.jwt@empresa.com',
        'password': 'debug123',
        'rol': 'reclutador'
    }
    
    post_response = requests.post(
        'http://localhost:5000/api/usuarios',
        json=user_data,
        headers=headers
    )
    
    print(f"Status: {post_response.status_code}")
    if post_response.status_code == 201:
        print(f"✅ POST usuarios funciona correctamente")
        result = post_response.json()
        print(f"   Usuario creado: {result['usuario']['nombre']}")
        
        # Limpiar
        user_id = result['usuario']['id']
        delete_response = requests.delete(
            f'http://localhost:5000/api/usuarios/{user_id}',
            headers=headers
        )
        print(f"   Limpieza: {delete_response.status_code}")
        
    else:
        print(f"❌ POST usuarios falló:")
        try:
            error = post_response.json()
            print(f"   Error: {json.dumps(error, indent=2)}")
        except:
            print(f"   Text: {post_response.text}")
    
    # 5. Verificar configuración JWT desde el backend
    print(f"\n5️⃣ Verificando configuración JWT del backend...")
    try:
        from app import create_app
        app = create_app()
        with app.app_context():
            jwt_secret = app.config.get('JWT_SECRET_KEY')
            secret_key = app.config.get('SECRET_KEY')
            
            print(f"✅ Configuración JWT:")
            print(f"   JWT_SECRET_KEY: {'SET' if jwt_secret else 'NOT SET'}")
            print(f"   SECRET_KEY: {'SET' if secret_key else 'NOT SET'}")
            print(f"   JWT_SECRET_KEY length: {len(jwt_secret) if jwt_secret else 0}")
            
            # Verificar si ambos secrets son iguales
            if jwt_secret and secret_key:
                if jwt_secret == secret_key:
                    print(f"   ⚠️  JWT_SECRET_KEY y SECRET_KEY son iguales")
                else:
                    print(f"   ✅ JWT_SECRET_KEY y SECRET_KEY son diferentes")
    except Exception as e:
        print(f"❌ Error verificando configuración: {str(e)}")
    
    print(f"\n" + "=" * 60)
    print("📋 DIAGNÓSTICO FINAL:")
    
    if get_response.status_code == 200 and post_response.status_code != 201:
        print("✅ GET funciona, POST falla")
        print("🔍 El problema está específicamente en el decorador @role_required")
        print("   - El token es válido para @token_required")
        print("   - Falla en @role_required")
        print("   - Posible problema en la validación de roles")
    elif get_response.status_code != 200:
        print("❌ Ambos GET y POST fallan")
        print("🔍 El problema está en @token_required base")
        print("   - Problema de configuración JWT general")
    else:
        print("✅ Ambos GET y POST funcionan")
        print("🎉 El problema se resolvió!")

if __name__ == '__main__':
    test_jwt_diagnosis()
