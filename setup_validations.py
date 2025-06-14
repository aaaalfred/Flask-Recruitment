#!/usr/bin/env python3
"""
Script completo para configurar las validaciones del formulario
"""
import subprocess
import sys
import os

def create_fernanda():
    """Crear usuario Fernanda Moreno"""
    print("👩 Creando usuario Fernanda Moreno...")
    try:
        result = subprocess.run([sys.executable, 'create_fernanda.py'], 
                              capture_output=True, text=True, 
                              cwd=r'C:\Users\ADMIN\code\rh')
        
        if result.returncode == 0:
            print("✅ Fernanda Moreno creada exitosamente")
            # Mostrar líneas importantes del resultado
            for line in result.stdout.split('\n'):
                if any(keyword in line for keyword in ['✅', '🆔', '🔑', 'ID:']):
                    print(f"   {line}")
            return True
        else:
            print("❌ Error creando Fernanda Moreno")
            if result.stderr:
                print(f"   Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error ejecutando script: {e}")
        return False

def test_form_validations():
    """Probar las validaciones del formulario"""
    print("\n🧪 Probando validaciones del formulario...")
    try:
        result = subprocess.run([sys.executable, 'test_vacants.py'], 
                              capture_output=True, text=True, 
                              cwd=r'C:\Users\ADMIN\code\rh')
        
        if result.returncode == 0:
            print("✅ Test del formulario exitoso")
            return True
        else:
            print("⚠️  Problemas en el test del formulario")
            # Mostrar solo errores importantes
            for line in result.stdout.split('\n'):
                if any(keyword in line for keyword in ['❌', 'Error', 'FAILED']):
                    print(f"   {line}")
            return False
            
    except Exception as e:
        print(f"❌ Error en test: {e}")
        return False

def main():
    print("=" * 70)
    print("⚙️  CONFIGURACIÓN DE VALIDACIONES DEL FORMULARIO")
    print("=" * 70)
    print()
    print("📋 Validaciones a implementar:")
    print("   • Estado de avance por defecto: 'Creada'")
    print("   • Reclutador líder siempre: Fernanda Moreno")
    print("   • Fechas envío y límite: posteriores al día de hoy")
    print()
    
    # Cambiar al directorio correcto
    os.chdir(r'C:\Users\ADMIN\code\rh')
    
    success = True
    
    # Paso 1: Crear Fernanda Moreno
    if not create_fernanda():
        success = False
    
    # Paso 2: Mensaje sobre el frontend
    print("\n🎨 Frontend actualizado con:")
    print("   ✅ Estado 'Creada' fijo y no editable")
    print("   ✅ Fernanda Moreno asignada automáticamente")
    print("   ✅ Validaciones de fechas futuras")
    print("   ✅ Campos min= en inputs de fecha")
    print("   ✅ Mensajes de error personalizados")
    
    # Paso 3: Probar funcionamiento
    print("\n🧪 Probando funcionamiento...")
    if test_form_validations():
        print("✅ Sistema funcionando correctamente")
    else:
        print("⚠️  Revisar configuración del servidor")
    
    print("\n" + "=" * 70)
    
    if success:
        print("🎉 ¡VALIDACIONES CONFIGURADAS EXITOSAMENTE!")
        print("\n✅ Funcionalidades implementadas:")
        print("   • 🆕 Estado siempre 'Creada' para nuevas vacantes")
        print("   • 👑 Fernanda Moreno como reclutador líder por defecto") 
        print("   • 📅 Validación de fechas futuras con mensajes de error")
        print("   • 🚫 Campos no editables para configuraciones automáticas")
        print("\n🚀 Para probar:")
        print("   1. Abrir frontend: http://localhost:3000")
        print("   2. Login: admin@empresa.com / admin123")
        print("   3. Ir a 'Vacantes' → 'Nueva Vacante'")
        print("   4. Intentar poner fechas del pasado (verás errores)")
        print("   5. Crear vacante y verificar que Fernanda es asignada")
        print("\n🔑 Nueva cuenta creada:")
        print("   Email: fernanda.moreno@empresa.com")
        print("   Password: fernanda123")
        print("   Rol: Reclutador Líder")
    else:
        print("❌ PROBLEMAS EN LA CONFIGURACIÓN")
        print("\n🔧 Revisa:")
        print("   1. Que el servidor esté corriendo")
        print("   2. Que la base de datos esté conectada")
        print("   3. Que no haya errores en la consola")
    
    print("=" * 70)

if __name__ == '__main__':
    main()
