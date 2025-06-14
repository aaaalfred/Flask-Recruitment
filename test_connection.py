#!/usr/bin/env python3
"""
Script de diagnóstico para probar la conexión entre frontend y backend
"""
import requests
import json
from datetime import datetime

def test_backend_connection():
    """Probar si el backend está respondiendo"""
    print("🔍 Probando conexión al backend...")
    
    try:
        # Probar endpoint básico
        response = requests.get('http://localhost:5000/api/auth/login', 
                              timeout=5,
                              headers={'Content-Type': 'application/json'})
        
        print(f"✅ Backend responde - Status: {response.status_code}")
        
        if response.status_code == 405:  # Method not allowed es esperado para GET en login
            print("✅ Endpoint /api/auth/login existe (método POST requerido)")
            return True
        
        return response.status_code < 500
        
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al backend en http://localhost:5000")
        return False
    except requests.exceptions.Timeout:
        print("❌ Timeout al conectar con el backend")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def test_cors_headers():
    """Probar configuración de CORS"""
    print("\n🔍 Probando configuración CORS...")
    
    try:
        # Hacer una petición OPTIONS (preflight)
        response = requests.options('http://localhost:5000/api/auth/login',
                                  headers={
                                      'Origin': 'http://localhost:3000',
                                      'Access-Control-Request-Method': 'POST',
                                      'Access-Control-Request-Headers': 'Content-Type'
                                  },
                                  timeout=5)
        
        print(f"Status de preflight: {response.status_code}")
        
        # Verificar headers CORS
        cors_headers = {
            'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
            'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
            'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers')
        }
        
        print("Headers CORS encontrados:")
        for header, value in cors_headers.items():
            if value:
                print(f"  ✅ {header}: {value}")
            else:
                print(f"  ❌ {header}: No encontrado")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando CORS: {e}")
        return False

def test_login_endpoint():
    """Probar el endpoint de login específicamente"""
    print("\n🔍 Probando endpoint de login...")
    
    try:
        login_data = {
            "email": "admin@empresa.com",
            "password": "admin123"
        }
        
        response = requests.post('http://localhost:5000/api/auth/login',
                               json=login_data,
                               headers={'Content-Type': 'application/json'},
                               timeout=10)
        
        print(f"Status de login: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Login exitoso")
            data = response.json()
            if 'access_token' in data:
                print("✅ Token recibido correctamente")
                return True
            else:
                print("❌ No se recibió token en la respuesta")
        elif response.status_code == 401:
            print("⚠️  Credenciales incorrectas (pero endpoint funciona)")
        else:
            print(f"❌ Error en login: {response.text}")
        
        return False
        
    except Exception as e:
        print(f"❌ Error probando login: {e}")
        return False

def check_frontend_config():
    """Verificar configuración del frontend"""
    print("\n🔍 Verificando configuración del frontend...")
    
    try:
        with open('frontend/.env', 'r') as f:
            env_content = f.read()
            
        print("Contenido de frontend/.env:")
        print(env_content)
        
        if 'REACT_APP_API_URL=http://localhost:5000/api' in env_content:
            print("✅ URL de API configurada correctamente")
            return True
        else:
            print("❌ URL de API no configurada correctamente")
            return False
            
    except FileNotFoundError:
        print("❌ Archivo frontend/.env no encontrado")
        return False
    except Exception as e:
        print(f"❌ Error leyendo configuración: {e}")
        return False

def main():
    """Ejecutar todos los tests de diagnóstico"""
    print("🚀 DIAGNÓSTICO DE COMUNICACIÓN FRONTEND-BACKEND")
    print("=" * 50)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    results = []
    
    # Test 1: Conexión básica
    results.append(("Conexión Backend", test_backend_connection()))
    
    # Test 2: CORS
    results.append(("Configuración CORS", test_cors_headers()))
    
    # Test 3: Login endpoint
    results.append(("Endpoint Login", test_login_endpoint()))
    
    # Test 4: Configuración frontend
    results.append(("Config Frontend", check_frontend_config()))
    
    # Resumen
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE DIAGNÓSTICO")
    print("=" * 50)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<20} {status}")
    
    total_passed = sum(results)
    total_tests = len(results)
    
    print(f"\nTests exitosos: {total_passed}/{total_tests}")
    
    if total_passed == total_tests:
        print("🎉 ¡Todos los tests pasaron! La comunicación debería funcionar.")
    else:
        print("⚠️  Hay problemas que necesitan ser resueltos.")
        print("\n🔧 RECOMENDACIONES:")
        
        if not results[0][1]:  # Backend no responde
            print("- Asegúrate de que el backend esté corriendo con 'python app.py'")
            print("- Verifica que no haya otros procesos usando el puerto 5000")
        
        if not results[1][1]:  # CORS
            print("- Revisa la configuración de CORS en extensions.py")
            print("- Asegúrate de que CORS permita el origen http://localhost:3000")
        
        if not results[2][1]:  # Login
            print("- Verifica que los usuarios de prueba existan en la base de datos")
            print("- Revisa los logs del backend para errores específicos")
        
        if not results[3][1]:  # Frontend config
            print("- Verifica que el archivo frontend/.env tenga la URL correcta")
            print("- Asegúrate de reiniciar el frontend después de cambios en .env")

if __name__ == "__main__":
    main()
