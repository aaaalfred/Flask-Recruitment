#!/usr/bin/env python3
"""
Script de verificación rápida del sistema
"""
import requests
import sys

def quick_check():
    """Verificación rápida del sistema"""
    print("🎯 VERIFICACIÓN RÁPIDA DEL SISTEMA RH")
    print("=" * 45)
    
    tests = []
    
    # Test 1: Backend health check
    try:
        response = requests.get('http://localhost:5000/api/health', timeout=5)
        if response.status_code == 200:
            print("✅ Backend: FUNCIONANDO")
            data = response.json()
            print(f"   📡 {data.get('message', 'API OK')}")
            tests.append(True)
        else:
            print(f"❌ Backend: Error {response.status_code}")
            tests.append(False)
    except requests.exceptions.ConnectionError:
        print("❌ Backend: NO DISPONIBLE")
        print("   💡 Ejecuta: python app.py")
        tests.append(False)
    except Exception as e:
        print(f"❌ Backend: Error {e}")
        tests.append(False)
    
    # Test 2: Login test
    try:
        login_data = {"email": "admin@empresa.com", "password": "admin123"}
        response = requests.post('http://localhost:5000/api/auth/login',
                               json=login_data,
                               headers={'Content-Type': 'application/json'},
                               timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if 'access_token' in data:
                print("✅ Login: FUNCIONANDO")
                print(f"   👤 Usuario: {data['user']['nombre']} ({data['user']['rol']})")
                tests.append(True)
            else:
                print("❌ Login: Sin token")
                tests.append(False)
        else:
            print(f"❌ Login: Error {response.status_code}")
            tests.append(False)
    except Exception as e:
        print(f"❌ Login: Error {e}")
        tests.append(False)
    
    # Test 3: Database users
    try:
        from app import create_app
        from models import Usuario
        
        app = create_app()
        with app.app_context():
            user_count = Usuario.query.count()
            print(f"✅ Base de datos: {user_count} usuarios")
            tests.append(True)
    except Exception as e:
        print(f"❌ Base de datos: Error {e}")
        tests.append(False)
    
    # Test 4: Frontend config
    try:
        with open('frontend/.env', 'r') as f:
            content = f.read()
        
        if 'REACT_APP_API_URL=http://localhost:5000/api' in content:
            print("✅ Frontend: CONFIGURADO")
            tests.append(True)
        else:
            print("❌ Frontend: Configuración incorrecta")
            tests.append(False)
    except FileNotFoundError:
        print("❌ Frontend: Archivo .env no encontrado")
        tests.append(False)
    except Exception as e:
        print(f"❌ Frontend: Error {e}")
        tests.append(False)
    
    # Resumen
    passed = sum(tests)
    total = len(tests)
    
    print("\n" + "=" * 45)
    print(f"📊 RESULTADO: {passed}/{total} tests exitosos")
    
    if passed == total:
        print("🎉 ¡SISTEMA COMPLETAMENTE FUNCIONAL!")
        print("\n🚀 Para usar el sistema:")
        print("1. Backend ya está corriendo")
        print("2. Abrir nueva terminal y ejecutar:")
        print("   cd frontend && npm start")
        print("\n👤 Credenciales de prueba:")
        print("   Email: admin@empresa.com")
        print("   Password: admin123")
    elif passed >= 2:
        print("⚠️  Sistema mayormente funcional con problemas menores")
    else:
        print("❌ Sistema con problemas críticos")
        print("\n🔧 Para solucionarlo:")
        if not tests[0]:  # Backend
            print("- Ejecutar: python app.py")
        if not tests[2]:  # Database
            print("- Verificar configuración de base de datos en .env")
        if not tests[3]:  # Frontend
            print("- Verificar frontend/.env")
    
    return passed == total

if __name__ == '__main__':
    success = quick_check()
    sys.exit(0 if success else 1)
