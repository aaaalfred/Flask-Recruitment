#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🔧 SCRIPT DE DIAGNÓSTICO DEL SISTEMA ATS
Verifica que todos los componentes estén funcionando correctamente
"""

import sys
import os
import requests
import json
from datetime import datetime

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_backend_health():
    """Probar el health check del backend"""
    try:
        print("🔍 Probando conexión con backend...")
        response = requests.get('http://localhost:5000/api/health', timeout=5)
        if response.status_code == 200:
            print("✅ Backend respondiendo correctamente")
            print(f"   Respuesta: {response.json()}")
            return True
        else:
            print(f"❌ Backend respondió con código {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al backend en localhost:5000")
        print("   💡 Asegúrate de que el servidor esté corriendo: python app.py")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        return False

def test_login_endpoints():
    """Probar los endpoints de login"""
    try:
        print("\n🔐 Probando endpoints de autenticación...")
        
        # Probar login con usuario administrador
        login_data = {
            'email': 'admin.principal@empresa.com',
            'password': 'password123'
        }
        
        response = requests.post(
            'http://localhost:5000/api/auth/login',
            json=login_data,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Login funcionando correctamente")
            data = response.json()
            if 'access_token' in data:
                print("✅ Token JWT generado correctamente")
                return data['access_token']
            else:
                print("❌ Respuesta de login sin token")
                return None
        else:
            print(f"❌ Login falló con código {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error en login: {str(e)}")
        return None

def test_dashboard_endpoint(token):
    """Probar el endpoint de dashboard"""
    if not token:
        print("❌ No hay token para probar dashboard")
        return False
        
    try:
        print("\n📊 Probando endpoint de dashboard...")
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(
            'http://localhost:5000/api/reports/dashboard',
            headers=headers,
            timeout=15
        )
        
        if response.status_code == 200:
            print("✅ Dashboard respondiendo correctamente")
            data = response.json()
            print(f"   Estadísticas cargadas: {len(data)} campos")
            return True
        else:
            print(f"❌ Dashboard falló con código {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error en dashboard: {str(e)}")
        return False

def test_models_import():
    """Probar que todos los modelos se importen correctamente"""
    try:
        print("\n📦 Probando imports de modelos...")
        
        from models import Usuario, Vacante, Candidato, Documento, Entrevista, CandidatosPositions, Cliente
        print("✅ Todos los modelos importados correctamente")
        
        # Verificar que los modelos tengan los métodos necesarios
        if hasattr(Usuario, 'to_dict'):
            print("✅ Método to_dict disponible en Usuario")
        if hasattr(Vacante, 'to_dict'):
            print("✅ Método to_dict disponible en Vacante")
        if hasattr(Cliente, 'to_dict'):
            print("✅ Método to_dict disponible en Cliente")
            
        return True
        
    except ImportError as e:
        print(f"❌ Error importando modelos: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado en modelos: {str(e)}")
        return False

def test_database_connection():
    """Probar conexión con la base de datos"""
    try:
        print("\n🗄️ Probando conexión con base de datos...")
        
        # Intentar importar la app y probar la DB
        from app import create_app
        from extensions import db
        
        app = create_app()
        with app.app_context():
            # Probar una consulta simple
            from models import Usuario
            total_users = Usuario.query.count()
            print(f"✅ Conexión DB exitosa - {total_users} usuarios en la base")
            return True
            
    except Exception as e:
        print(f"❌ Error de conexión DB: {str(e)}")
        return False

def main():
    """Función principal de diagnóstico"""
    print("🔧 DIAGNÓSTICO COMPLETO DEL SISTEMA ATS")
    print("=" * 50)
    print(f"⏰ Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Contadores de pruebas
    tests_passed = 0
    total_tests = 5
    
    # 1. Probar imports de modelos
    if test_models_import():
        tests_passed += 1
    
    # 2. Probar conexión a la base de datos
    if test_database_connection():
        tests_passed += 1
    
    # 3. Probar health del backend
    if test_backend_health():
        tests_passed += 1
    
    # 4. Probar login
    token = test_login_endpoints()
    if token:
        tests_passed += 1
    
    # 5. Probar dashboard
    if test_dashboard_endpoint(token):
        tests_passed += 1
    
    # Resumen final
    print("\n" + "=" * 50)
    print("📋 RESUMEN DEL DIAGNÓSTICO")
    print("=" * 50)
    print(f"✅ Pruebas pasadas: {tests_passed}/{total_tests}")
    print(f"❌ Pruebas fallidas: {total_tests - tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("\n🎉 ¡TODOS LOS COMPONENTES FUNCIONANDO CORRECTAMENTE!")
        print("🚀 El sistema está listo para usar")
    else:
        print(f"\n⚠️  HAY {total_tests - tests_passed} COMPONENTES CON PROBLEMAS")
        print("🔧 Revisa los errores anteriores y corrige los problemas")
    
    print("\n💡 CREDENCIALES DE PRUEBA:")
    print("   👤 Reclutador: test.reclutador@empresa.com / password123")
    print("   👥 Líder: fernanda@empresa.com / password123") 
    print("   🏢 Ejecutivo: admin@empresa.com / password123")
    print("   ⚡ Admin: admin.principal@empresa.com / password123")
    
    return tests_passed == total_tests

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
