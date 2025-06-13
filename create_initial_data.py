"""
Script para crear datos iniciales del sistema de reclutamiento
Ejecutar: python create_initial_data.py
"""

from app import create_app, db
from models import Usuario

def create_initial_data():
    """Crear datos iniciales para testing"""
    app = create_app()
    
    with app.app_context():
        try:
            # Crear tablas si no existen
            db.create_all()
            
            # Verificar si ya existen usuarios
            if Usuario.query.count() > 0:
                print("Ya existen usuarios en la base de datos")
                return
            
            # Crear usuario administrador inicial
            admin_user = Usuario(
                nombre='Administrador Sistema',
                email='admin@empresa.com',
                rol='ejecutivo',
                activo=True
            )
            admin_user.set_password('admin123')
            
            # Crear reclutador de prueba
            recruiter_user = Usuario(
                nombre='Reclutador Principal',
                email='reclutador@empresa.com',
                rol='reclutador',
                activo=True
            )
            recruiter_user.set_password('reclutador123')
            
            # Crear reclutador líder
            leader_user = Usuario(
                nombre='Líder de Reclutamiento',
                email='lider@empresa.com',
                rol='reclutador_lider',
                activo=True
            )
            leader_user.set_password('lider123')
            
            db.session.add(admin_user)
            db.session.add(recruiter_user)
            db.session.add(leader_user)
            db.session.commit()
            
            print("✅ Usuarios iniciales creados exitosamente")
            print("\n🔑 Credenciales de acceso:")
            print("Administrador: admin@empresa.com / admin123")
            print("Reclutador: reclutador@empresa.com / reclutador123")
            print("Líder: lider@empresa.com / lider123")
            print("\n🚀 Ejecuta 'python app.py' para iniciar el servidor")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error creando datos iniciales: {str(e)}")

if __name__ == '__main__':
    create_initial_data()
