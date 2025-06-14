#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para inicializar completamente la gestión de usuarios
"""

import os
import sys
import subprocess
import time
import argparse

def print_header(title):
    """Imprime un header estilizado"""
    print("\n" + "="*60)
    print(f"🎯 {title}")
    print("="*60)

def print_step(step, description):
    """Imprime un paso del proceso"""
    print(f"\n📋 PASO {step}: {description}")
    print("-" * 50)

def run_backend():
    """Inicia el servidor backend"""
    print_step(1, "INICIANDO SERVIDOR BACKEND")
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists('app.py'):
        print("❌ Error: No se encuentra app.py")
        print("   Asegúrate de estar en C:\\Users\\ADMIN\\code\\rh\\")
        return False
    
    # Activar entorno virtual y ejecutar servidor
    try:
        print("🔧 Corrigiendo password del admin...")
        subprocess.run([sys.executable, 'fix_admin_password.py'], check=True)
        
        print("\n🚀 Iniciando servidor Flask...")
        print("   URL: http://localhost:5000")
        print("   API: http://localhost:5000/api")
        print("   Usuarios: http://localhost:5000/api/usuarios")
        print("   Presiona Ctrl+C para detener")
        
        # Ejecutar servidor
        subprocess.run([sys.executable, 'app.py'])
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando comando: {e}")
        return False
    except KeyboardInterrupt:
        print("\n⏹️ Servidor detenido por el usuario")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def run_frontend():
    """Inicia el servidor frontend"""
    print_step(1, "INICIANDO SERVIDOR FRONTEND")
    
    frontend_dir = "frontend"
    original_dir = os.getcwd()
    
    # Verificar que existe el directorio frontend
    if not os.path.exists(frontend_dir):
        print("❌ Error: No se encuentra el directorio frontend")
        return False
    
    try:
        print("📦 Verificando dependencias...")
        
        # Cambiar al directorio frontend
        os.chdir(frontend_dir)
        
        # Verificar que existe package.json
        if not os.path.exists('package.json'):
            print("❌ Error: No se encuentra package.json")
            return False
        
        print("🚀 Iniciando servidor React...")
        print("   URL: http://localhost:3000")
        print("   Gestión de Usuarios: http://localhost:3000/users")
        print("   Presiona Ctrl+C para detener")
        
        # Ejecutar servidor React
        subprocess.run(['npm', 'start'], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando npm start: {e}")
        print("💡 Intenta ejecutar 'npm install' primero")
        return False
    except KeyboardInterrupt:
        print("\n⏹️ Servidor frontend detenido por el usuario")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        # Volver al directorio original
        os.chdir(original_dir)

def test_system():
    """Prueba que el sistema esté funcionando"""
    print_step(1, "PROBANDO CONEXIÓN AL SISTEMA")
    
    try:
        import requests
        
        # Probar backend
        print("🔍 Probando backend...")
        response = requests.get('http://localhost:5000/api/health', timeout=5)
        
        if response.status_code == 200:
            print("✅ Backend funcionando correctamente")
        else:
            print(f"⚠️ Backend responde pero con código: {response.status_code}")
            
    except ImportError:
        print("⚠️ Módulo 'requests' no disponible, saltando prueba de backend")
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar con el backend")
        print("   Asegúrate de que el servidor esté corriendo en localhost:5000")
    except Exception as e:
        print(f"❌ Error probando backend: {e}")

def test_login():
    """Prueba el login con el admin"""
    print_step(2, "PROBANDO LOGIN DE ADMIN")
    
    try:
        import requests
        
        login_data = {
            'email': 'admin@empresa.com',
            'password': 'password123'
        }
        
        response = requests.post('http://localhost:5000/api/auth/login', 
                               json=login_data,
                               headers={'Content-Type': 'application/json'},
                               timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Login de admin exitoso")
            print(f"   Token obtenido: {data['access_token'][:50]}...")
            return data['access_token']
        else:
            print(f"❌ Error en login: {response.text}")
            return None
            
    except ImportError:
        print("⚠️ Módulo 'requests' no disponible")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_users_api(token):
    """Prueba la API de usuarios"""
    print_step(3, "PROBANDO API DE USUARIOS")
    
    if not token:
        print("❌ No hay token disponible")
        return
    
    try:
        import requests
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get('http://localhost:5000/api/usuarios', 
                              headers=headers,
                              timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API de usuarios funcionando")
            print(f"   Usuarios encontrados: {len(data['usuarios'])}")
            
            for usuario in data['usuarios']:
                print(f"   - {usuario['nombre']} ({usuario['rol']})")
        else:
            print(f"❌ Error en API usuarios: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def show_credentials():
    """Muestra las credenciales de acceso"""
    print_header("CREDENCIALES DE ACCESO")
    
    print("🔑 USUARIO ADMINISTRADOR:")
    print("   Email: admin@empresa.com")
    print("   Password: password123")
    print("   Rol: ejecutivo")
    
    print("\n🌐 URLs DEL SISTEMA:")
    print("   Backend API: http://localhost:5000/api")
    print("   Frontend: http://localhost:3000")
    print("   Login: http://localhost:3000/login")
    print("   Gestión de Usuarios: http://localhost:3000/users")
    
    print("\n📋 FUNCIONALIDADES DISPONIBLES:")
    print("   ✅ Crear nuevos usuarios")
    print("   ✅ Editar usuarios existentes")
    print("   ✅ Desactivar usuarios")
    print("   ✅ Filtrar por rol y búsqueda")
    print("   ✅ Control de permisos por rol")

def setup_instructions():
    """Muestra las instrucciones de configuración"""
    print_header("INSTRUCCIONES DE USO")
    
    print("🚀 INICIAR SISTEMA COMPLETO:")
    print("   python setup_users.py --full")
    
    print("\n🔧 INICIAR SOLO BACKEND:")
    print("   python setup_users.py --backend")
    
    print("\n🎨 INICIAR SOLO FRONTEND:")
    print("   python setup_users.py --frontend")
    
    print("\n🧪 PROBAR SISTEMA:")
    print("   python setup_users.py --test")
    
    print("\n🔑 VER CREDENCIALES:")
    print("   python setup_users.py --credentials")
    
    print("\n📋 REQUISITOS:")
    print("   ✅ Python 3.9+ con Flask")
    print("   ✅ Node.js 16+ con React")
    print("   ✅ MySQL corriendo")
    print("   ✅ Variables de entorno configuradas")

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description='Setup del Sistema de Gestión de Usuarios')
    parser.add_argument('--backend', action='store_true', help='Iniciar solo backend')
    parser.add_argument('--frontend', action='store_true', help='Iniciar solo frontend')
    parser.add_argument('--full', action='store_true', help='Configuración completa')
    parser.add_argument('--test', action='store_true', help='Probar sistema')
    parser.add_argument('--credentials', action='store_true', help='Mostrar credenciales')
    parser.add_argument('--help-setup', action='store_true', help='Mostrar instrucciones')
    
    args = parser.parse_args()
    
    # Si no se especifica ningún argumento, mostrar ayuda
    if not any(vars(args).values()):
        print_header("SETUP DEL SISTEMA DE GESTIÓN DE USUARIOS")
        setup_instructions()
        return
    
    if args.help_setup:
        setup_instructions()
    elif args.credentials:
        show_credentials()
    elif args.test:
        test_system()
        token = test_login()
        test_users_api(token)
        show_credentials()
    elif args.backend:
        run_backend()
    elif args.frontend:
        run_frontend()
    elif args.full:
        print_header("CONFIGURACIÓN COMPLETA DEL SISTEMA")
        print("\n🎯 Este modo abrirá dos terminales:")
        print("   1. Terminal para Backend (Flask)")
        print("   2. Terminal para Frontend (React)")
        print("\n⚠️ Necesitarás abrir ambos manualmente:")
        print("\n🔧 TERMINAL 1 - Backend:")
        print("   cd C:\\Users\\ADMIN\\code\\rh")
        print("   python setup_users.py --backend")
        print("\n🎨 TERMINAL 2 - Frontend:")
        print("   cd C:\\Users\\ADMIN\\code\\rh")
        print("   python setup_users.py --frontend")
        
        print("\n¿Qué quieres hacer?")
        print("   1. Iniciar Backend ahora")
        print("   2. Iniciar Frontend ahora")
        print("   3. Ver credenciales")
        print("   4. Probar sistema")
        
        choice = input("\nSelecciona una opción (1-4): ").strip()
        
        if choice == '1':
            run_backend()
        elif choice == '2':
            run_frontend()
        elif choice == '3':
            show_credentials()
        elif choice == '4':
            test_system()
            token = test_login()
            test_users_api(token)
        else:
            print("Opción no válida")

if __name__ == '__main__':
    main()
