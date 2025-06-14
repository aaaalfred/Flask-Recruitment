#!/usr/bin/env python3
"""
Script para inicializar usuarios de prueba
"""
from app import create_app
from extensions import db
from models import Usuario

def create_test_users():
    """Crear usuarios de prueba si no existen"""
    app = create_app()
    
    with app.app_context():
        try:
            # Verificar si ya existen usuarios
            admin_exists = Usuario.query.filter_by(email='admin@empresa.com').first()
            reclutador_exists = Usuario.query.filter_by(email='reclutador@empresa.com').first()
            
            users_created = []
            
            if not admin_exists:
                admin_user = Usuario(
                    nombre='Administrador',
                    email='admin@empresa.com',
                    rol='ejecutivo',
                    activo=True
                )
                admin_user.set_password('admin123')
                db.session.add(admin_user)
                users_created.append('admin@empresa.com')
            
            if not reclutador_exists:
                recruiter_user = Usuario(
                    nombre='Reclutador Test',
                    email='reclutador@empresa.com',
                    rol='reclutador',
                    activo=True
                )
                recruiter_user.set_password('reclutador123')
                db.session.add(recruiter_user)
                users_created.append('reclutador@empresa.com')
            
            # Crear reclutador líder si no existe
            leader_exists = Usuario.query.filter_by(email='lider@empresa.com').first()
            if not leader_exists:
                leader_user = Usuario(
                    nombre='Líder de Reclutamiento',
                    email='lider@empresa.com',
                    rol='reclutador_lider',
                    activo=True
                )
                leader_user.set_password('lider123')
                db.session.add(leader_user)
                users_created.append('lider@empresa.com')
            
            if users_created:
                db.session.commit()
                print("✅ Usuarios de prueba creados:")
                for email in users_created:
                    if 'admin' in email:
                        print(f"   👤 {email} / admin123 (Ejecutivo)")
                    elif 'reclutador' in email:
                        print(f"   👤 {email} / reclutador123 (Reclutador)")
                    elif 'lider' in email:
                        print(f"   👤 {email} / lider123 (Reclutador Líder)")
            else:
                print("ℹ️  Los usuarios de prueba ya existen")
            
            # Mostrar todos los usuarios existentes
            all_users = Usuario.query.filter_by(activo=True).all()
            print(f"\n📋 Total de usuarios activos: {len(all_users)}")
            for user in all_users:
                print(f"   • {user.email} - {user.rol} ({user.nombre})")
                
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error creando usuarios: {str(e)}")
            raise e

if __name__ == '__main__':
    print("🔧 Inicializando usuarios de prueba...")
    create_test_users()
    print("✅ Proceso completado!")
