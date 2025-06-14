#!/usr/bin/env python3
"""
Script básico para verificar la configuración sin dependencias externas
"""
import sys
import os
import subprocess

def check_python_version():
    """Verificar versión de Python"""
    print("🐍 Verificando versión de Python...")
    version = sys.version_info
    print(f"   Versión: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("✅ Versión de Python compatible")
        return True
    else:
        print("❌ Se requiere Python 3.8 o superior")
        return False

def check_directory():
    """Verificar directorio actual"""
    print("📁 Verificando directorio...")
    current_dir = os.getcwd()
    print(f"   Directorio actual: {current_dir}")
    
    required_files = ['app.py', 'requirements.txt', 'config.py']
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file} encontrado")
        else:
            print(f"   ❌ {file} no encontrado")
            missing_files.append(file)
    
    return len(missing_files) == 0

def check_venv():
    """Verificar entorno virtual"""
    print("🔧 Verificando entorno virtual...")
    
    venv_paths = [
        'venv/Scripts/activate.bat',  # Windows
        'venv/bin/activate',          # Linux/Mac
        '.venv/Scripts/activate.bat', # Windows alternativo
        '.venv/bin/activate'          # Linux/Mac alternativo
    ]
    
    venv_found = False
    for path in venv_paths:
        if os.path.exists(path):
            print(f"   ✅ Entorno virtual encontrado: {path}")
            venv_found = True
            break
    
    if not venv_found:
        print("   ⚠️  Entorno virtual no encontrado")
        
    return venv_found

def check_requirements():
    """Verificar archivo requirements.txt"""
    print("📋 Verificando requirements.txt...")
    
    if not os.path.exists('requirements.txt'):
        print("   ❌ requirements.txt no encontrado")
        return False
    
    try:
        with open('requirements.txt', 'r', encoding='utf-8') as f:
            requirements = f.read()
        
        essential_packages = [
            'Flask',
            'Flask-SQLAlchemy', 
            'PyMySQL',
            'Flask-Login',
            'Flask-JWT-Extended'
        ]
        
        missing_packages = []
        for package in essential_packages:
            if package.lower() in requirements.lower():
                print(f"   ✅ {package} en requirements")
            else:
                print(f"   ❌ {package} no encontrado en requirements")
                missing_packages.append(package)
        
        return len(missing_packages) == 0
        
    except Exception as e:
        print(f"   ❌ Error leyendo requirements.txt: {e}")
        return False

def install_packages():
    """Intentar instalar paquetes"""
    print("📦 Intentando instalar dependencias...")
    
    try:
        # Actualizar pip
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'], 
                      check=True, capture_output=True)
        print("   ✅ pip actualizado")
        
        # Instalar requirements
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✅ Dependencias instaladas correctamente")
            return True
        else:
            print("   ❌ Error instalando dependencias:")
            print(f"      {result.stderr}")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Error en subprocess: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Error inesperado: {e}")
        return False

def test_imports():
    """Probar imports básicos"""
    print("🧪 Probando imports...")
    
    test_modules = [
        ('flask', 'Flask'),
        ('flask_sqlalchemy', 'Flask-SQLAlchemy'),
        ('pymysql', 'PyMySQL'),
        ('flask_login', 'Flask-Login'),
        ('flask_jwt_extended', 'Flask-JWT-Extended')
    ]
    
    all_imported = True
    
    for module_name, display_name in test_modules:
        try:
            __import__(module_name)
            print(f"   ✅ {display_name} importado correctamente")
        except ImportError as e:
            print(f"   ❌ Error importando {display_name}: {e}")
            all_imported = False
    
    return all_imported

def create_simple_requirements():
    """Crear requirements.txt simple si no existe"""
    requirements_content = '''Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-Login==0.6.3
Flask-JWT-Extended==4.5.3
Flask-CORS==4.0.0
Flask-Migrate==4.0.5
PyMySQL==1.1.0
python-dotenv==1.0.0
Werkzeug==2.3.7
marshmallow==3.20.1
flask-marshmallow==0.15.0
marshmallow-sqlalchemy==0.29.0
'''
    
    try:
        with open('requirements.txt', 'w', encoding='utf-8') as f:
            f.write(requirements_content)
        print("✅ requirements.txt creado")
        return True
    except Exception as e:
        print(f"❌ Error creando requirements.txt: {e}")
        return False

def main():
    print("=" * 60)
    print("🔧 DIAGNÓSTICO DE ENTORNO DE DESARROLLO")
    print("=" * 60)
    print()
    
    success = True
    
    # Verificaciones básicas
    if not check_python_version():
        success = False
    print()
    
    if not check_directory():
        print("❌ No estás en el directorio correcto del proyecto")
        success = False
    print()
    
    venv_exists = check_venv()
    print()
    
    if not check_requirements():
        print("🔧 Creando requirements.txt...")
        create_simple_requirements()
    print()
    
    # Intentar instalación
    if not test_imports():
        print("🔧 Instalando dependencias faltantes...")
        if install_packages():
            print("✅ Instalación completada")
            print()
            print("🧪 Verificando imports después de la instalación...")
            if test_imports():
                print("✅ Todos los módulos funcionan correctamente")
            else:
                print("❌ Aún hay problemas con algunos módulos")
                success = False
        else:
            success = False
    
    print()
    print("=" * 60)
    
    if success:
        print("✅ ENTORNO CONFIGURADO CORRECTAMENTE")
        print()
        print("🚀 Puedes continuar con:")
        print("   python app.py")
        print("   python test_utf8_simple.py")
        print("   python solve_utf8.py")
        print()
        if not venv_exists:
            print("💡 Recomendación: Crear entorno virtual")
            print("   python -m venv venv")
            print("   venv\\Scripts\\activate  (Windows)")
            print("   source venv/bin/activate  (Linux/Mac)")
    else:
        print("❌ PROBLEMAS DETECTADOS")
        print()
        print("🔧 Pasos para solucionar:")
        print("   1. Crear entorno virtual: python -m venv venv")
        print("   2. Activar entorno: venv\\Scripts\\activate")
        print("   3. Instalar dependencias: pip install -r requirements.txt")
        print("   4. Ejecutar este script de nuevo")
    
    print("=" * 60)

if __name__ == '__main__':
    main()
