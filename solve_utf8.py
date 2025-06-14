#!/usr/bin/env python3
"""
Script completo para solucionar problemas de UTF-8 y sistema
"""
import subprocess
import sys
import os

def run_charset_fix():
    """Ejecutar corrección de charset"""
    print("🔤 Ejecutando corrección de charset UTF-8...")
    try:
        result = subprocess.run([sys.executable, 'fix_charset.py'], 
                              capture_output=True, text=True, 
                              cwd=r'C:\Users\ADMIN\code\rh')
        
        print("📋 Resultado de la corrección de charset:")
        if result.stdout:
            # Mostrar líneas importantes
            lines = result.stdout.split('\n')
            for line in lines:
                if any(keyword in line for keyword in ['✅', '❌', '🔧', '💡', 'ERROR', 'SUCCESS']):
                    print(f"   {line}")
        
        if result.stderr:
            print("⚠️  Errores:")
            print(f"   {result.stderr}")
            
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error ejecutando corrección de charset: {e}")
        return False

def restart_server_message():
    """Mostrar mensaje para reiniciar el servidor"""
    print("\n🔄 REINICIO REQUERIDO")
    print("=" * 50)
    print("Para que los cambios de UTF-8 tomen efecto:")
    print("1. 🛑 Detener el servidor Flask (Ctrl+C)")
    print("2. 🚀 Reiniciar el servidor: python app.py")
    print("3. 🧪 Probar de nuevo: python test_vacants.py")
    print("=" * 50)

def create_utf8_test():
    """Crear un test simple de UTF-8"""
    test_content = '''#!/usr/bin/env python3
"""
Test simple para verificar UTF-8
"""
from app import create_app
from extensions import db
from models import Vacante, Usuario

def test_utf8_simple():
    """Prueba simple de caracteres especiales"""
    app = create_app()
    
    with app.app_context():
        # Buscar un usuario
        user = Usuario.query.first()
        if not user:
            print("❌ No hay usuarios disponibles")
            return False
        
        # Texto con acentos
        test_descripcion = "Descripción con acentos: áéíóúñü ¡Hola! ¿Cómo estás?"
        
        try:
            # Crear vacante de prueba
            test_vacante = Vacante(
                nombre="Test UTF-8 áéíóú",
                descripcion=test_descripcion,
                ejecutivo_id=user.id,
                reclutador_id=user.id,
                candidatos_requeridos=3
            )
            
            db.session.add(test_vacante)
            db.session.commit()
            
            # Recuperar y verificar
            saved = Vacante.query.filter_by(nombre="Test UTF-8 áéíóú").first()
            if saved and saved.descripcion == test_descripcion:
                print("✅ UTF-8 funciona correctamente")
                print(f"   Guardado: {saved.descripcion}")
                
                # Limpiar
                db.session.delete(saved)
                db.session.commit()
                return True
            else:
                print("❌ Los caracteres no se guardaron correctamente")
                return False
                
        except Exception as e:
            print(f"❌ Error en test UTF-8: {str(e)}")
            db.session.rollback()
            return False

if __name__ == '__main__':
    test_utf8_simple()
'''
    
    with open(r'C:\Users\ADMIN\code\rh\test_utf8_simple.py', 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    print("✅ Test UTF-8 simple creado")

def main():
    print("=" * 70)
    print("🛠️  SOLUCIÓN COMPLETA PARA CARACTERES ESPECIALES")
    print("=" * 70)
    print()
    
    # Cambiar al directorio correcto
    os.chdir(r'C:\Users\ADMIN\code\rh')
    
    print("📁 Directorio actual:", os.getcwd())
    print()
    
    # Paso 1: Aplicar corrección de charset
    print("🔧 Paso 1: Corrigiendo configuración de UTF-8...")
    if run_charset_fix():
        print("✅ Corrección de charset completada")
    else:
        print("⚠️  Problemas en la corrección de charset")
    print()
    
    # Paso 2: Crear test simple
    print("🔧 Paso 2: Creando test de UTF-8...")
    create_utf8_test()
    print()
    
    # Paso 3: Mostrar instrucciones
    restart_server_message()
    print()
    
    print("🧪 Después de reiniciar el servidor, ejecuta:")
    print("   python test_utf8_simple.py")
    print("   python test_vacants.py")
    print()
    
    print("💡 Si los problemas persisten:")
    print("   1. Verificar permisos de MySQL")
    print("   2. Revisar configuración de my.cnf/my.ini")
    print("   3. Consultar con el administrador de la base de datos")
    print()
    
    print("=" * 70)
    print("✅ PROCESO COMPLETADO")
    print("🔄 ¡Ahora reinicia el servidor Flask!")
    print("=" * 70)

if __name__ == '__main__':
    main()
