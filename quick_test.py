#!/usr/bin/env python3
"""
Test rápido para verificar la creación de usuarios
Ejecutar mientras el backend está corriendo
"""

import requests
import json

def quick_test():
    print("🔧 TEST RÁPIDO - CREACIÓN DE USUARIOS")
    print("=" * 50)
    
    # 1. Login
    print("1️⃣ Probando login...")
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
    print(f"✅ Login OK - Usuario: {user['nombre']} ({user['rol']})")
    
    # 2. Probar creación
    print("\n2️⃣ Probando creación de usuario...")
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    user_data = {
        'nombre': 'Test Usuario Rápido',
        'email': 'test.rapido@empresa.com',
        'password': 'test123',
        'rol': 'reclutador'
    }
    
    create_response = requests.post(
        'http://localhost:5000/api/usuarios',
        json=user_data,
        headers=headers
    )
    
    print(f"Status: {create_response.status_code}")
    
    if create_response.status_code == 201:
        result = create_response.json()
        print(f"✅ Usuario creado: {result['usuario']['nombre']}")
        
        # Limpiar
        user_id = result['usuario']['id']
        delete_response = requests.delete(
            f'http://localhost:5000/api/usuarios/{user_id}',
            headers=headers
        )
        if delete_response.status_code == 200:
            print(f"🧹 Usuario de prueba eliminado")
        
    else:
        print(f"❌ Error creando usuario:")
        try:
            error = create_response.json()
            print(f"   JSON: {json.dumps(error, indent=2)}")
        except:
            print(f"   Text: {create_response.text}")
    
    print("\n" + "=" * 50)
    if create_response.status_code == 201:
        print("✅ BACKEND FUNCIONA CORRECTAMENTE")
        print("   El problema está en el FRONTEND")
        print("   👉 Revisar DevTools del navegador")
        print("   👉 Usar el debug_frontend_handleSave.js")
    else:
        print("❌ BACKEND TIENE PROBLEMAS")
        print("   👉 Revisar logs del servidor Flask")

if __name__ == '__main__':
    quick_test()
