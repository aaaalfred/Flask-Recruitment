#!/usr/bin/env python3
"""
Script para iniciar el backend y verificar que funcione correctamente
Resuelve el error HTTP 422
"""

import subprocess
import time
import requests
import sys
import os

def check_backend_running():
    """Verificar si el backend está corriendo"""
    try:
        response = requests.get('http://localhost:5000/api/auth/login', timeout=3)
        return True
    except:
        return False

def start_backend():
    """Intentar iniciar el backend"""
    print("🚀 Iniciando backend...")
    
    backend_dir = r"C:\Users\ADMIN\code\rh"
    
    if not os.path.exists(backend_dir):
        print(f"❌ Directorio del backend no encontrado: {backend_dir}")
        return False
    
    try:
        # Cambiar al directorio del backend
        os.chdir(backend_dir)
        
        print(f"📁 Directorio actual: {os.getcwd()}")
        print("⏳ Ejecutando 'python app.py'...")
        
        # Para debugging, vamos a mostrar información del entorno
        print(f"Python path: {sys.executable}")
        
        # Ejecutar el backend en un proceso separado
        # Nota: Este script debe ejecutarse desde una terminal separada
        process = subprocess.Popen(
            [sys.executable, 'app.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Esperar un poco para que el servidor inicie
        print("⏳ Esperando que el servidor inicie...")
        time.sleep(5)
        
        # Verificar si el proceso sigue vivo
        if process.poll() is None:
            print("✅ Proceso iniciado correctamente")
            
            # Verificar si responde
            for i in range(10):
                if check_backend_running():
                    print(f"✅ Backend respondiendo en http://localhost:5000")
                    return True
                print(f"   Intento {i+1}/10 - Esperando respuesta...")
                time.sleep(2)
            
            print("❌ Backend no responde después de 20 segundos")
            return False
        else:
            print("❌ El proceso terminó inesperadamente")
            stdout, stderr = process.communicate()
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error iniciando backend: {str(e)}")
        return False

def show_manual_instructions():
    """Mostrar instrucciones manuales para iniciar el backend"""
    print("\n📝 INSTRUCCIONES MANUALES:")
    print("=" * 50)
    print("1. Abrir una nueva terminal/CMD")
    print("2. Ejecutar los siguientes comandos:")
    print()
    print("   cd C:\\Users\\ADMIN\\code\\rh")
    print("   python app.py")
    print()
    print("3. Deberías ver algo como:")
    print("   * Running on http://127.0.0.1:5000")
    print("   * Debug mode: on")
    print()
    print("4. Una vez que veas eso, ejecutar este script de nuevo:")
    print("   python test_422_specific.py")
    print()
    print("5. O ir directamente al frontend:")
    print("   http://localhost:3000/users")

def main():
    """Función principal"""
    print("🔧 SOLUCIONANDO ERROR HTTP 422")
    print("Verificando y iniciando backend si es necesario")
    print("=" * 60)
    
    # Verificar si ya está corriendo
    if check_backend_running():
        print("✅ Backend ya está corriendo")
        print("Ejecutar: python test_422_specific.py")
        return True
    
    print("⚠️  Backend no está corriendo")
    
    # Intentar iniciarlo automáticamente
    print("\n🔄 Intentando iniciar backend automáticamente...")
    if start_backend():
        print("✅ Backend iniciado exitosamente")
        print("Ejecutar: python test_422_specific.py")
        return True
    
    # Si falla, mostrar instrucciones manuales
    print("❌ No se pudo iniciar automáticamente")
    show_manual_instructions()
    return False

if __name__ == '__main__':
    main()
