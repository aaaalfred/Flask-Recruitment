#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corregir el password del usuario admin
"""

from app import create_app
from extensions import db
from models import Usuario

def fix_admin_password():
    """Corrige el password del usuario admin"""
    app = create_app()
    
    with app.app_context():
        try:
            # Buscar al usuario admin
            admin = Usuario.query.filter_by(email='admin@empresa.com').first()
            
            if admin:
                print(f"👤 Usuario encontrado: {admin.nombre} ({admin.email})")
                print(f"🔑 Rol actual: {admin.rol}")
                
                # Establecer el password correcto
                admin.set_password('password123')
                db.session.commit()
                
                print("✅ Password actualizado exitosamente a 'password123'")
                
                # Verificar que funciona
                if admin.check_password('password123'):
                    print("✅ Verificación exitosa: el password funciona correctamente")
                    
                    # Verificar también el password anterior para comparar
                    if admin.check_password('admin123'):
                        print("⚠️ Nota: El password anterior 'admin123' también funciona")
                    else:
                        print("🔒 Password anterior 'admin123' ya no funciona")
                        
                else:
                    print("❌ Error: el password no funciona")
                    
            else:
                print("❌ Usuario admin no encontrado")
                print("📝 Creando usuario admin...")
                
                admin = Usuario(
                    nombre='Administrador Sistema',
                    email='admin@empresa.com',
                    rol='ejecutivo',
                    activo=True
                )
                admin.set_password('password123')
                
                db.session.add(admin)
                db.session.commit()
                
                print("✅ Usuario admin creado exitosamente")
                
            # Mostrar todos los usuarios activos
            print("\n👥 === USUARIOS ACTIVOS EN EL SISTEMA ===\n")
            usuarios = Usuario.query.filter_by(activo=True).all()
            
            for usuario in usuarios:
                print(f"   {usuario.nombre:<25} | {usuario.email:<30} | {usuario.rol}")
                
            print(f"\n📊 Total: {len(usuarios)} usuarios activos")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            db.session.rollback()

if __name__ == '__main__':
    print("🔧 === CORRIGIENDO PASSWORD DEL ADMIN ===")
    fix_admin_password()
    print("\n🎯 ¡Listo! Ahora puedes usar:")
    print("   Email: admin@empresa.com")
    print("   Password: password123")
