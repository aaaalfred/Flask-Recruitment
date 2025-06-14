#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para instalar dependencias faltantes y verificar el sistema
"""

import subprocess
import sys
import os

def print_header(title):
    """Imprime un header estilizado"""
    print("\n" + "="*60)
    print(f"🔧 {title}")
    print("="*60)

def install_requirements():
    """Instala las dependencias de requirements.txt"""
    print_header("INSTALANDO DEPENDENCIAS PYTHON")
    
    try:
        print("📦 Instalando paquetes desde requirements.txt...")
        
        # Ejecutar pip install
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ], capture_output=True, text=True, check=True)
        
        print("✅ Dependencias instaladas exitosamente")
        print(result.stdout[-200:] if len(result.stdout) > 200 else result.stdout)
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias:")
        print(e.stderr)
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def verify_flask_packages():
    """Verifica específicamente los paquetes de Flask"""
    print_header("VERIFICANDO PAQUETES FLASK")
    
    flask_packages = [
        ('flask', 'Flask'),
        ('flask_sqlalchemy', 'Flask-SQLAlchemy'),
        ('flask_jwt_extended', 'Flask-JWT-Extended'),
        ('flask_cors', 'Flask-CORS'),
        ('flask_migrate', 'Flask-Migrate'),
        ('pymysql', 'PyMySQL'),
        ('requests', 'requests')
    ]
    
    all_installed = True
    
    for import_name, package_name in flask_packages:
        try:
            # Intentar importar usando diferentes métodos
            if import_name == 'flask_sqlalchemy':
                from flask_sqlalchemy import SQLAlchemy
            elif import_name == 'flask_jwt_extended':
                from flask_jwt_extended import JWTManager
            elif import_name == 'flask_cors':
                from flask_cors import CORS
            elif import_name == 'flask_migrate':
                from flask_migrate import Migrate
            else:
                __import__(import_name)
            
            print(f"   ✅ {package_name}")
            
        except ImportError as e:
            print(f"   ❌ {package_name} - {e}")
            all_installed = False
    
    return all_installed

def test_imports():
    """Prueba imports específicos del proyecto"""
    print_header("PROBANDO IMPORTS DEL PROYECTO")
    
    try:
        print("🧪 Probando import de app...")
        from app import create_app
        print("   ✅ app.create_app")
        
        print("🧪 Probando import de extensions...")
        from extensions import db, jwt
        print("   ✅ extensions.db, jwt")
        
        print("🧪 Probando import de models...")
        from models import Usuario
        print("   ✅ models.Usuario")
        
        print("🧪 Probando import de routes...")
        from routes.usuario_routes import usuario_bp
        print("   ✅ routes.usuario_routes")
        
        print("\n✅ Todos los imports del proyecto funcionan correctamente")
        return True
        
    except ImportError as e:
        print(f"❌ Error de import: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def test_app_creation():
    """Prueba la creación de la aplicación Flask"""
    print_header("PROBANDO CREACIÓN DE APP")
    
    try:
        from app import create_app
        
        print("🏗️ Creando aplicación Flask...")
        app = create_app()
        
        print("🔧 Verificando configuración...")
        with app.app_context():
            from extensions import db
            from models import Usuario
            
            print("   ✅ Contexto de aplicación")
            print("   ✅ Base de datos conectada")
            print("   ✅ Modelos cargados")
            
        print("\n✅ Aplicación Flask creada exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error creando app: {e}")
        return False

def main():
    """Función principal"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    🔧 INSTALADOR DE DEPENDENCIAS                            ║
║                                                              ║
║    Resolviendo problemas de paquetes faltantes              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists('requirements.txt'):
        print("❌ Error: No se encuentra requirements.txt")
        print("   Asegúrate de estar en C:\\Users\\ADMIN\\code\\rh\\")
        return
    
    success = True
    
    # Paso 1: Instalar dependencias
    if not install_requirements():
        success = False
    
    # Paso 2: Verificar paquetes Flask
    if not verify_flask_packages():
        success = False
    
    # Paso 3: Probar imports del proyecto
    if not test_imports():
        success = False
    
    # Paso 4: Probar creación de app
    if not test_app_creation():
        success = False
    
    # Resultado final
    print("\n" + "="*60)
    if success:
        print("🎉 ¡TODAS LAS DEPENDENCIAS INSTALADAS CORRECTAMENTE!")
        print("✅ El sistema está listo para usar")
        print("\n🚀 Próximos pasos:")
        print("   1. python verify_users_system.py")
        print("   2. python setup_users.py --backend")
        print("   3. python setup_users.py --frontend")
    else:
        print("⚠️ ALGUNOS PROBLEMAS PERSISTEN")
        print("❌ Revisa los errores anteriores")
        print("\n💡 Posibles soluciones:")
        print("   - Actualizar pip: python -m pip install --upgrade pip")
        print("   - Reinstalar entorno virtual")
        print("   - Verificar conexión a internet")
    
    print("="*60)

if __name__ == '__main__':
    main()
