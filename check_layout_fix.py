#!/usr/bin/env python3
"""
Script de verificación rápida para el problema del layout
"""

import os

def check_layout_fixes():
    print("🔧 VERIFICANDO CORRECCIONES DEL LAYOUT")
    print("=" * 50)
    
    base_path = r"C:\Users\ADMIN\code\rh\frontend\src"
    
    # Verificar Layout.js
    layout_path = os.path.join(base_path, "components", "Layout.js")
    if os.path.exists(layout_path):
        with open(layout_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        checks = [
            ("Estado de colapso", "sidebarCollapsed" in content),
            ("Margin dinámico", "lg:ml-16" in content and "lg:ml-72" in content),
            ("Transición", "transition-all duration-300" in content),
            ("Props al Sidebar", "isCollapsed={sidebarCollapsed}" in content)
        ]
        
        print("📁 Layout.js:")
        for desc, check in checks:
            status = "✅" if check else "❌"
            print(f"  {status} {desc}")
    
    # Verificar Sidebar.js
    sidebar_path = os.path.join(base_path, "components", "Sidebar.js")
    if os.path.exists(sidebar_path):
        with open(sidebar_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        checks = [
            ("Props recibidas", "isCollapsed, setIsCollapsed" in content),
            ("Botón funcional", "setIsCollapsed(!isCollapsed)" in content),
            ("Ancho dinámico", "lg:w-16" in content and "lg:w-72" in content)
        ]
        
        print("\n📁 Sidebar.js:")
        for desc, check in checks:
            status = "✅" if check else "❌"
            print(f"  {status} {desc}")
    
    # Verificar CSS
    css_path = os.path.join(base_path, "styles", "responsive.css")
    if os.path.exists(css_path):
        with open(css_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        checks = [
            ("Transición main-content", "transition: margin-left" in content),
            ("Tooltips", "sidebar-tooltip" in content),
            ("Media queries", "@media (min-width: 1024px)" in content)
        ]
        
        print("\n📁 responsive.css:")
        for desc, check in checks:
            status = "✅" if check else "❌"
            print(f"  {status} {desc}")
    
    print("\n🎯 SOLUCIÓN IMPLEMENTADA:")
    print("• Layout con margin-left dinámico")
    print("• Sidebar comunica estado de colapso")
    print("• Transiciones suaves de 300ms")
    print("• CSS optimizado para evitar superposición")
    
    print("\n🚀 PARA PROBAR:")
    print("1. cd C:\\Users\\ADMIN\\code\\rh\\frontend")
    print("2. npm start")
    print("3. Hacer clic en ← / → en el header del menú")
    print("4. Verificar que el contenido se desplaza correctamente")

if __name__ == "__main__":
    check_layout_fixes()
