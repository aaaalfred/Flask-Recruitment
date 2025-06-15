#!/usr/bin/env python3
"""
Script de prueba rápida para el dashboard optimizado
"""

import requests
import time
import json

BASE_URL = 'http://localhost:5000/api'
LOGIN_EMAIL = 'admin@empresa.com'
LOGIN_PASSWORD = 'password123'

def test_optimized_dashboard():
    print("🚀 PROBANDO DASHBOARD OPTIMIZADO")
    print("=" * 50)
    
    # Login
    login_data = {'email': LOGIN_EMAIL, 'password': LOGIN_PASSWORD}
    try:
        response = requests.post(f'{BASE_URL}/auth/login', json=login_data)
        if response.status_code == 200:
            token = response.json()['access_token']
            print("✅ Login exitoso")
        else:
            print("❌ Error en login")
            return
    except Exception as e:
        print(f"❌ Error de conexión: {str(e)}")
        return
    
    # Test dashboard con medición de tiempo
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    print("\n🔍 Probando endpoint optimizado...")
    
    start_time = time.time()
    
    try:
        response = requests.get(f'{BASE_URL}/reports/dashboard', headers=headers, timeout=60)
        end_time = time.time()
        
        response_time = end_time - start_time
        
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Dashboard cargado en {response_time:.2f} segundos")
            print(f"📊 Estadísticas obtenidas:")
            print(f"   • Total vacantes: {stats.get('total_vacantes', 0)}")
            print(f"   • Total candidatos: {stats.get('total_candidatos', 0)}")
            print(f"   • Total entrevistas: {stats.get('total_entrevistas', 0)}")
            print(f"   • Rendimiento reclutadores: {len(stats.get('rendimiento_reclutadores', []))}")
            print(f"   • Vacantes antiguas: {len(stats.get('vacantes_antiguas', []))}")
            
            # Verificar que no hay valores None
            none_values = []
            for key, value in stats.items():
                if value is None:
                    none_values.append(key)
            
            if none_values:
                print(f"⚠️ Valores None encontrados: {none_values}")
            else:
                print("✅ No hay valores None")
            
            return True
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        end_time = time.time()
        response_time = end_time - start_time
        print(f"❌ Timeout después de {response_time:.2f} segundos")
        return False
    except Exception as e:
        end_time = time.time()
        response_time = end_time - start_time
        print(f"❌ Error después de {response_time:.2f} segundos: {str(e)}")
        return False

if __name__ == '__main__':
    success = test_optimized_dashboard()
    print("\n" + "=" * 50)
    if success:
        print("🎉 DASHBOARD OPTIMIZADO FUNCIONANDO")
        print("💡 Ahora prueba en el frontend: http://localhost:3000/dashboard")
    else:
        print("❌ Dashboard necesita más optimización")
