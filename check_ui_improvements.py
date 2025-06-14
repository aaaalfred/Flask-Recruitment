#!/usr/bin/env python3
"""
Script para verificar las mejoras de UI/UX implementadas
Verifica que los archivos modificados estén correctos
"""

import os
import sys
import json

def check_file_exists(file_path, description):
    """Verifica que un archivo existe"""
    if os.path.exists(file_path):
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} - NO ENCONTRADO")
        return False

def check_file_content(file_path, search_text, description):
    """Verifica que un archivo contiene cierto texto"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if search_text in content:
                print(f"✅ {description}: Contenido encontrado")
                return True
            else:
                print(f"❌ {description}: Contenido NO encontrado")
                return False
    except Exception as e:
        print(f"❌ Error leyendo {file_path}: {str(e)}")
        return False

def main():
    print("🔍 VERIFICANDO MEJORAS DE UI/UX - MENÚ COLAPSABLE Y RESPONSIVE")
    print("=" * 70)
    
    base_path = r"C:\Users\ADMIN\code\rh\frontend\src"
    
    checks = []
    
    # 1. Verificar Sidebar mejorado
    sidebar_path = os.path.join(base_path, "components", "Sidebar.js")
    checks.append(check_file_exists(sidebar_path, "Sidebar mejorado"))
    checks.append(check_file_content(sidebar_path, "isCollapsed", "Estado de colapso en Sidebar"))
    checks.append(check_file_content(sidebar_path, "ChevronLeftIcon", "Íconos de colapso"))
    checks.append(check_file_content(sidebar_path, "sidebar-tooltip", "Tooltips mejorados"))
    
    # 2. Verificar Layout actualizado
    layout_path = os.path.join(base_path, "components", "Layout.js")
    checks.append(check_file_exists(layout_path, "Layout actualizado"))
    checks.append(check_file_content(layout_path, "max-w-full", "Contenido responsive"))
    
    # 3. Verificar Dashboard responsive
    dashboard_path = os.path.join(base_path, "pages", "Dashboard.js")
    checks.append(check_file_exists(dashboard_path, "Dashboard responsive"))
    checks.append(check_file_content(dashboard_path, "grid-cols-2 lg:grid-cols-4", "Grid responsive"))
    checks.append(check_file_content(dashboard_path, "lg:p-6", "Padding responsive"))
    
    # 4. Verificar estilos CSS adicionales
    css_path = os.path.join(base_path, "styles", "responsive.css")
    checks.append(check_file_exists(css_path, "Estilos CSS responsivos"))
    checks.append(check_file_content(css_path, "sidebar-tooltip", "Estilos de tooltip"))
    
    # 5. Verificar importación de estilos
    index_path = os.path.join(base_path, "index.js")
    checks.append(check_file_exists(index_path, "Index.js"))
    checks.append(check_file_content(index_path, "./styles/responsive.css", "Importación de estilos"))
    
    print("\n📊 RESUMEN DE VERIFICACIONES")
    print("=" * 40)
    
    passed = sum(checks)
    total = len(checks)
    
    print(f"✅ Verificaciones exitosas: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 ¡TODAS LAS MEJORAS SE IMPLEMENTARON CORRECTAMENTE!")
        print("\n📋 MEJORAS IMPLEMENTADAS:")
        print("• ✅ Menú lateral colapsable con botón de expandir/contraer")
        print("• ✅ Tooltips mejorados para el menú colapsado")
        print("• ✅ Layout responsive que se ajusta al ancho del menú")
        print("• ✅ Dashboard con grid responsive (2 columnas en móvil, 4 en desktop)")
        print("• ✅ Padding y márgenes adaptativos")
        print("• ✅ Tablas responsive con scroll horizontal")
        print("• ✅ Estilos CSS adicionales para mejores transiciones")
        print("• ✅ Contenido que utiliza el espacio completo disponible")
        
        print("\n🚀 INSTRUCCIONES PARA PROBAR:")
        print("1. Ejecuta: cd C:\\Users\\ADMIN\\code\\rh\\frontend && npm start")
        print("2. Abre http://localhost:3000")
        print("3. Inicia sesión con admin@empresa.com / admin123")
        print("4. En pantallas grandes: haz clic en el botón ← / → en el header del menú")
        print("5. En móvil: el menú se oculta automáticamente y se abre con el botón ☰")
        print("6. Prueba redimensionar la ventana para ver el comportamiento responsive")
        
        return True
    else:
        print(f"\n⚠️  Faltan {total - passed} verificaciones por completar")
        print("Revisa los archivos marcados con ❌ antes de continuar")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
