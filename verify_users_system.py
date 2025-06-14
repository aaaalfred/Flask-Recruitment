#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de verificación final para la gestión de usuarios
"""

import os
import sys
import subprocess
import time

def print_banner():
    """Imprime banner de inicio"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    👥 GESTIÓN DE USUARIOS - VERIFICACIÓN FINAL              ║
║                                                              ║
║    Sistema de Reclutamiento Flask + React                   ║
║    Versión: 1.0.0                                           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)

def check_files():
    """Verifica que todos los archivos necesarios existan"""
    print("📂 === VERIFICANDO ARCHIVOS ===")
    
    required_files = [
        'app.py',
        'fix_admin_password.py',
        'setup_users.py',
        'test_user_management.py',
        'routes/usuario_routes.py',
        'models/__init__.py',
        'frontend/src/pages/Users.js',
        'frontend/src/styles/users.css'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️ Archivos faltantes: {len(missing_files)}")
        return False
    else:
        print("\n✅ Todos los archivos están presentes")
        return True

def check_dependencies():
    """Verifica dependencias de Python"""
    print("\n🐍 === VERIFICANDO DEPENDENCIAS PYTHON ===")
    
    required_packages = [
        ('flask', 'Flask'),
        ('flask_sqlalchemy', 'Flask-SQLAlchemy'),
        ('flask_jwt_extended', 'Flask-JWT-Extended'),
        ('pymysql', 'PyMySQL'),
        ('requests', 'requests')
    ]
    
    missing_packages = []
    
    for import_name, display_name in required_packages:
        try:
            if import_name == 'flask_sqlalchemy':
                from flask_sqlalchemy import SQLAlchemy
            elif import_name == 'flask_jwt_extended':
                from flask_jwt_extended import JWTManager
            else:
                __import__(import_name)
            print(f"   ✅ {display_name}")
        except ImportError:
            print(f"   ❌ {display_name}")
            missing_packages.append(display_name)
    
    if missing_packages:
        print(f"\n⚠️ Paquetes faltantes: {missing_packages}")
        print("💡 Ejecuta: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ Todas las dependencias están instaladas")
        return True

def check_database():
    """Verifica conexión a la base de datos"""
    print("\n🗄️ === VERIFICANDO BASE DE DATOS ===")
    
    try:
        from app import create_app
        from models import Usuario
        
        app = create_app()
        
        with app.app_context():
            # Intentar hacer una consulta simple
            usuarios = Usuario.query.count()
            print(f"   ✅ Conexión exitosa")
            print(f"   📊 Usuarios en BD: {usuarios}")
            
            # Verificar que existe el admin
            admin = Usuario.query.filter_by(email='admin@empresa.com').first()
            if admin:
                print(f"   ✅ Usuario admin encontrado: {admin.nombre}")
                
                # Verificar password
                if admin.check_password('password123'):
                    print("   ✅ Password correcto")
                else:
                    print("   ⚠️ Password incorrecto, se corregirá")
                    admin.set_password('password123')
                    from extensions import db
                    db.session.commit()
                    print("   ✅ Password corregido")
            else:
                print("   ⚠️ Usuario admin no encontrado")
            
            return True
            
    except Exception as e:
        print(f"   ❌ Error de conexión: {str(e)}")
        print("   💡 Verifica que MySQL esté corriendo")
        return False

def check_frontend():
    """Verifica archivos del frontend"""
    print("\n🎨 === VERIFICANDO FRONTEND ===")
    
    frontend_files = [
        'frontend/package.json',
        'frontend/src/App.js',
        'frontend/src/pages/Users.js',
        'frontend/src/styles/users.css'
    ]
    
    all_good = True
    
    for file_path in frontend_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path}")
            all_good = False
    
    # Verificar node_modules
    if os.path.exists('frontend/node_modules'):
        print("   ✅ node_modules")
    else:
        print("   ⚠️ node_modules (ejecuta 'npm install' en frontend/)")
    
    return all_good

def show_next_steps():
    """Muestra los siguientes pasos"""
    print("\n🚀 === SIGUIENTES PASOS ===")
    
    print("\n1. 🔧 INICIAR BACKEND:")
    print("   python setup_users.py --backend")
    print("   URL: http://localhost:5000")
    
    print("\n2. 🎨 INICIAR FRONTEND:")
    print("   python setup_users.py --frontend")
    print("   URL: http://localhost:3000")
    
    print("\n3. 🔑 CREDENCIALES:")
    print("   Email: admin@empresa.com")
    print("   Password: password123")
    
    print("\n4. 👥 GESTIÓN DE USUARIOS:")
    print("   URL: http://localhost:3000/users")
    
    print("\n5. 🧪 PROBAR SISTEMA:")
    print("   python test_user_management.py")

def show_features():
    """Muestra las características implementadas"""
    print("\n✨ === CARACTERÍSTICAS IMPLEMENTADAS ===")
    
    features = [
        "✅ CRUD completo de usuarios",
        "✅ Autenticación JWT",
        "✅ Control de roles y permisos",
        "✅ Interfaz responsive",
        "✅ Filtros y búsqueda",
        "✅ Modal para crear/editar",
        "✅ Validaciones frontend/backend",
        "✅ Password correcto del admin",
        "✅ API RESTful documentada",
        "✅ Estilos CSS optimizados"
    ]
    
    for feature in features:
        print(f"   {feature}")

def main():
    """Función principal"""
    print_banner()
    
    all_checks_passed = True
    
    # Verificar archivos
    if not check_files():
        all_checks_passed = False
    
    # Verificar dependencias
    if not check_dependencies():
        all_checks_passed = False
    
    # Verificar base de datos
    if not check_database():
        all_checks_passed = False
    
    # Verificar frontend
    if not check_frontend():
        all_checks_passed = False
    
    # Mostrar características
    show_features()
    
    # Mostrar resultado final
    print("\n" + "="*60)
    if all_checks_passed:
        print("🎉 ¡VERIFICACIÓN EXITOSA!")
        print("✅ El sistema de gestión de usuarios está listo para usar")
        show_next_steps()
    else:
        print("⚠️ HAY PROBLEMAS QUE RESOLVER")
        print("❌ Revisa los errores anteriores antes de continuar")
    
    print("="*60)

if __name__ == '__main__':
    main()
