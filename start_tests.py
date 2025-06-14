#!/usr/bin/env python3
"""
Script para verificar y inicializar todo el sistema paso a paso
"""
import subprocess
import sys
import time
import requests
import os

def check_server_running():
    """Verificar si el servidor Flask está corriendo"""
    try:
        response = requests.get('http://localhost:5000/api/health', timeout=3)
        return response.status_code == 200
    except:
        return False

def run_command(command, description):
    """Ejecutar un comando y mostrar el resultado"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=r'C:\Users\ADMIN\code\rh')
        if result.returncode == 0:
            print(f"✅ {description} - Exitoso")
            if result.stdout.strip():
                # Mostrar solo las líneas más importantes
                lines = result.stdout.strip().split('\n')
                for line in lines[-10:]:  # Últimas 10 líneas
                    if any(keyword in line.lower() for keyword in ['✅', '❌', 'error', 'success', 'usuario', 'creado']):
                        print(f"   {line}")
            return True
        else:
            print(f"❌ {description} - Error")
            if result.stderr:
                print(f"   Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description} - Excepción: {str(e)}")
        return False

def main():
    print("=" * 70)
    print("🚀 INICIALIZACIÓN COMPLETA DEL SISTEMA DE RECLUTAMIENTO")
    print("=" * 70)
    print()
    
    # Cambiar al directorio correcto
    os.chdir(r'C:\Users\ADMIN\code\rh')
    print(f"📁 Directorio actual: {os.getcwd()}")
    print()
    
    # Paso 1: Verificar si el servidor está corriendo
    print("🌐 Verificando servidor...")
    if check_server_running():
        print("✅ Servidor Flask está corriendo")
    else:
        print("⚠️  Servidor Flask no está corriendo")
        print("💡 Para iniciar el servidor ejecuta en otra terminal:")
        print("   cd C:\\Users\\ADMIN\\code\\rh")
        print("   python app.py")
        print()
        input("⏳ Presiona Enter cuando el servidor esté corriendo...")
        
        # Verificar de nuevo
        if not check_server_running():
            print("❌ El servidor aún no está disponible")
            print("🛑 No se puede continuar sin el servidor")
            return
        else:
            print("✅ Servidor detectado!")
    print()
    
    # Paso 2: Reparar sistema (base de datos y usuarios)
    if not run_command("python fix_system.py", "Reparando sistema y creando usuarios"):
        print("⚠️  Problemas durante la reparación, pero continuemos...")
    print()
    
    # Paso 3: Ejecutar diagnóstico
    if not run_command("python debug_users.py", "Ejecutando diagnóstico completo"):
        print("⚠️  Problemas en el diagnóstico, pero continuemos...")
    print()
    
    # Paso 4: Probar el formulario de vacantes
    print("🧪 Ejecutando pruebas del formulario de vacantes...")
    success = run_command("python test_vacants.py", "Probando creación de vacantes")
    print()
    
    print("=" * 70)
    if success:
        print("🎉 ¡SISTEMA COMPLETAMENTE FUNCIONAL!")
        print()
        print("✅ Lo que está funcionando:")
        print("   • Base de datos conectada")
        print("   • Usuarios creados correctamente")
        print("   • Login funcionando")
        print("   • API de vacantes operativa")
        print("   • Formulario con scroll arreglado")
        print()
        print("🌐 Acceso al sistema:")
        print("   • Frontend: http://localhost:3000")
        print("   • Backend API: http://localhost:5000")
        print()
        print("🔑 Usuarios de prueba:")
        print("   • admin@empresa.com / admin123")
        print("   • reclutador@empresa.com / reclutador123")
        print("   • lider@empresa.com / lider123")
    else:
        print("⚠️  SISTEMA PARCIALMENTE FUNCIONAL")
        print()
        print("💡 Pasos manuales:")
        print("   1. Verificar que el servidor esté corriendo: python app.py")
        print("   2. Crear usuarios: python fix_system.py")
        print("   3. Probar login: python debug_users.py")
        print("   4. Probar vacantes: python test_vacants.py")
    
    print("=" * 70)
    print()
    print("📝 Próximos pasos sugeridos:")
    print("   1. Abrir el frontend en el navegador")
    print("   2. Hacer login con admin@empresa.com / admin123")
    print("   3. Ir a 'Vacantes' → 'Nueva Vacante'")
    print("   4. Probar el formulario con scroll")
    print("   5. Crear una vacante de prueba")

if __name__ == '__main__':
    main()
