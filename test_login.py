#!/usr/bin/env python3
"""
Script para probar el login directamente
"""

import requests
import json

def test_login_api():
    """Probar el endpoint de login"""
    
    url = 'http://localhost:5000/api/auth/login'
    
    # Credenciales de prueba
    test_credentials = [
        {'email': 'admin@empresa.com', 'password': 'admin123'},
        {'email': 'reclutador@empresa.com', 'password': 'reclutador123'}
    ]
    
    for creds in test_credentials:
        print(f"\n🧪 Probando login con {creds['email']}...")
        
        try:
            response = requests.post(
                url, 
                json=creds,
                headers={'Content-Type': 'application/json'}
            )
            
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Login exitoso para {creds['email']}")
                print(f"Usuario: {data.get('user', {}).get('nombre')}")
                print(f"Rol: {data.get('user', {}).get('rol')}")
            else:
                print(f"❌ Login fallido para {creds['email']}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Error: No se puede conectar al servidor Flask")
            print("💡 Asegúrate de que Flask esté corriendo con: python app.py")
            break
        except Exception as e:
            print(f"❌ Error inesperado: {str(e)}")

if __name__ == '__main__':
    print("🔧 Probando API de autenticación...")
    print("=" * 50)
    
    test_login_api()
