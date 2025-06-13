#!/usr/bin/env python3
"""
Script para crear usuarios de prueba específicos
"""

from app import create_app
from extensions import db
from models import Usuario

def create_test_users():
    """Crear usuarios de prueba con credenciales específicas"""
    
    app = create_app()
    
    with app.app_context():
        try:
            # Verificar si ya existe el usuario admin
            admin_user = Usuario.query.filter_by(email='admin@empresa.com').first()
            if not admin_user:
                # Crear usuario admin (ejecutivo)
                admin_user = Usuario(
                    nombre='Administrador Sistema',
                    email='admin@empresa.com',
                    rol='ejecutivo',
                    activo=True
                )
                admin_user.set_password('admin123')
                db.session.add(admin_user)
                print("✅ Usuario admin creado: admin@empresa.com / admin123")
            else:
                print("ℹ️ Usuario admin ya existe")
            
            # Verificar si ya existe el usuario reclutador
            recruiter_user = Usuario.query.filter_by(email='reclutador@empresa.com').first()
            if not recruiter_user:
                # Crear usuario reclutador
                recruiter_user = Usuario(
                    nombre='Reclutador Principal',
                    email='reclutador@empresa.com',
                    rol='reclutador',
                    activo=True
                )
                recruiter_user.set_password('reclutador123')
                db.session.add(recruiter_user)
                print("✅ Usuario reclutador creado: reclutador@empresa.com / reclutador123")
            else:
                print("ℹ️ Usuario reclutador ya existe")
            
            # Guardar cambios
            db.session.commit()
            
            print("\n🎉 Usuarios de prueba listos:")
            print("👤 Ejecutivo: admin@empresa.com / admin123")
            print("👤 Reclutador: reclutador@empresa.com / reclutador123")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error creando usuarios: {str(e)}")

def test_login():
    """Probar login con las credenciales"""
    
    app = create_app()
    
    with app.app_context():
        # Probar admin
        admin = Usuario.query.filter_by(email='admin@empresa.com').first()
        if admin and admin.check_password('admin123'):
            print("✅ Login admin funcionando correctamente")
        else:
            print("❌ Error en login admin")
        
        # Probar reclutador
        reclutador = Usuario.query.filter_by(email='reclutador@empresa.com').first()
        if reclutador and reclutador.check_password('reclutador123'):
            print("✅ Login reclutador funcionando correctamente")
        else:
            print("❌ Error en login reclutador")

if __name__ == '__main__':
    print("🔧 Creando usuarios de prueba...")
    print("=" * 40)
    
    create_test_users()
    
    print("\n🧪 Probando autenticación...")
    print("=" * 40)
    
    test_login()
    
    print("\n✅ Proceso completado!")
