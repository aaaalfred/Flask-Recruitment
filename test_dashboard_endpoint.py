#!/usr/bin/env python3
"""
Script de prueba para verificar que el endpoint del dashboard funciona correctamente
"""

import requests
import json
from datetime import datetime

# Configuración
BASE_URL = 'http://localhost:5000/api'
headers = {'Content-Type': 'application/json'}

def test_health():
    """Test de conectividad básica"""
    try:
        print("🔍 1. Probando conectividad básica...")
        response = requests.get(f'{BASE_URL}/health', headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ Backend está corriendo correctamente")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Backend responde pero con error: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: No se puede conectar al backend")
        print("   ¿Está corriendo el servidor Flask en localhost:5000?")
        return False
    except requests.exceptions.Timeout:
        print("❌ ERROR: Timeout conectando al backend")
        return False
    except Exception as e:
        print(f"❌ ERROR inesperado: {str(e)}")
        return False

def test_login():
    """Test de login para obtener token"""
    try:
        print("\n🔍 2. Probando login...")
        
        # Intentar con Sofia Rueda (ejecutivo)
        login_data = {
            'email': 'sofia@empresa.com',
            'password': 'sofia123'  # Asumiendo password común
        }
        
        response = requests.post(f'{BASE_URL}/auth/login', 
                               json=login_data, 
                               headers=headers,
                               timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            user_info = data.get('user')
            print(f"✅ Login exitoso para: {user_info.get('nombre')} ({user_info.get('rol')})")
            print(f"   Token recibido: {token[:50]}...")
            return token, user_info
        else:
            print(f"❌ Login falló: {response.status_code}")
            print(f"   Response: {response.text}")
            
            # Intentar con admin como fallback
            print("   Intentando con admin...")
            admin_login = {
                'email': 'admin@empresa.com',
                'password': 'admin123'
            }
            
            response = requests.post(f'{BASE_URL}/auth/login', 
                                   json=admin_login, 
                                   headers=headers,
                                   timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                token = data.get('access_token')
                user_info = data.get('user')
                print(f"✅ Login exitoso con admin: {user_info.get('nombre')} ({user_info.get('rol')})")
                return token, user_info
            else:
                print(f"❌ Login con admin también falló: {response.status_code}")
                return None, None
                
    except Exception as e:
        print(f"❌ ERROR en login: {str(e)}")
        return None, None

def test_dashboard_endpoint(token, user_info):
    """Test del endpoint del dashboard"""
    try:
        print(f"\n🔍 3. Probando endpoint del dashboard para {user_info.get('nombre')}...")
        
        auth_headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        
        print("   Enviando request a /api/reports/dashboard...")
        response = requests.get(f'{BASE_URL}/reports/dashboard', 
                              headers=auth_headers,
                              timeout=45)  # 45 segundos timeout
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Dashboard endpoint funciona correctamente!")
            print("\n📊 ESTADÍSTICAS RECIBIDAS:")
            print(f"   Total Vacantes: {data.get('total_vacantes')}")
            print(f"   Vacantes Abiertas: {data.get('vacantes_abiertas')}")
            print(f"   Total Candidatos: {data.get('total_candidatos')}")
            print(f"   Entrevistas Pendientes: {data.get('entrevistas_pendientes')}")
            print(f"   Tipo Usuario: {data.get('tipo_usuario')}")
            print(f"   Usuario: {data.get('usuario_nombre')}")
            print(f"   Filtrado por reclutador: {data.get('filtrado_por_reclutador')}")
            print(f"   Fecha actualización: {data.get('fecha_actualizacion')}")
            
            # Mostrar algunos detalles adicionales
            if data.get('candidatos_por_status'):
                print("\n   Candidatos por status:")
                for status, count in data['candidatos_por_status'].items():
                    print(f"     {status}: {count}")
                    
            if data.get('vacantes_por_prioridad'):
                print("\n   Vacantes por prioridad:")
                for prioridad, count in data['vacantes_por_prioridad'].items():
                    print(f"     {prioridad}: {count}")
            
            return True
        else:
            print(f"❌ Dashboard endpoint falló: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ ERROR: Timeout en dashboard endpoint (>45 segundos)")
        print("   El endpoint puede estar ejecutándose muy lento o bloqueado")
        return False
    except Exception as e:
        print(f"❌ ERROR en dashboard endpoint: {str(e)}")
        return False

def test_manual_query():
    """Test manual de una query simple"""
    try:
        print(f"\n🔍 4. Verificación manual de datos...")
        
        # Este test requiere una conexión directa a la DB
        # Solo para mostrar que los datos existen
        print("   (Esta verificación requiere acceso directo a la DB)")
        print("   Confirma que tienes:")
        print("   - 18 vacantes totales en la DB")
        print("   - 3 vacantes para Sofia Rueda (ejecutivo_id = 15)")
        print("   - El servidor Flask está corriendo en localhost:5000")
        print("   - Los modelos están importados correctamente")
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

def main():
    """Función principal de prueba"""
    print("🚀 DIAGNÓSTICO DEL DASHBOARD - SISTEMA RH")
    print("=" * 50)
    
    # 1. Test de conectividad
    if not test_health():
        print("\n❌ FALLO CRÍTICO: Backend no disponible")
        print("   SOLUCIÓN: Ejecuta 'python app.py' en otra terminal")
        return
    
    # 2. Test de login
    token, user_info = test_login()
    if not token:
        print("\n❌ FALLO CRÍTICO: No se puede obtener token de autenticación")
        print("   SOLUCIÓN: Verifica credenciales de usuarios en la DB")
        return
    
    # 3. Test del dashboard
    if test_dashboard_endpoint(token, user_info):
        print("\n✅ DIAGNÓSTICO COMPLETO: Todo funciona correctamente!")
        print("   El problema puede estar en el frontend o en el browser")
        print("   Verifica la consola del navegador (F12)")
    else:
        print("\n❌ PROBLEMA DETECTADO: Dashboard endpoint no funciona")
        print("   Revisa los logs del servidor Flask para más detalles")
    
    # 4. Verificación manual
    test_manual_query()
    
    print("\n" + "=" * 50)
    print("🏁 DIAGNÓSTICO COMPLETADO")
    print(f"   Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == '__main__':
    main()
