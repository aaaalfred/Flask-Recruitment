#!/usr/bin/env python3
"""
Script para crear datos iniciales en el sistema de reclutamiento
"""

from app import create_app, db
from models import Usuario

def create_initial_users():
    """Crear usuarios iniciales para pruebas"""
    
    app = create_app()
    
    with app.app_context():
        # Verificar si ya existen usuarios
        if Usuario.query.first():
            print("Ya existen usuarios en la base de datos")
            return
        
        try:
            # Crear usuario ejecutivo
            ejecutivo = Usuario(
                nombre='Ejecutivo Admin',
                email='ejecutivo@empresa.com',
                rol='ejecutivo',
                activo=True
            )
            ejecutivo.set_password('ejecutivo123')
            
            # Crear reclutador
            reclutador = Usuario(
                nombre='Reclutador Test',
                email='reclutador@empresa.com',
                rol='reclutador',
                activo=True
            )
            reclutador.set_password('reclutador123')
            
            # Crear reclutador líder
            reclutador_lider = Usuario(
                nombre='Lider Reclutamiento',
                email='lider@empresa.com',
                rol='reclutador_lider',
                activo=True
            )
            reclutador_lider.set_password('lider123')
            
            # Guardar en base de datos
            db.session.add(ejecutivo)
            db.session.add(reclutador)
            db.session.add(reclutador_lider)
            db.session.commit()
            
            print("✅ Usuarios iniciales creados exitosamente:")
            print("- Ejecutivo: ejecutivo@empresa.com / ejecutivo123")
            print("- Reclutador: reclutador@empresa.com / reclutador123")
            print("- Líder: lider@empresa.com / lider123")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error creando usuarios: {str(e)}")

def check_database_connection():
    """Verificar conexión a la base de datos"""
    app = create_app()
    
    with app.app_context():
        try:
            # Intentar una consulta simple
            result = db.session.execute(db.text('SELECT 1'))
            print("✅ Conexión a la base de datos exitosa")
            return True
        except Exception as e:
            print(f"❌ Error conectando a la base de datos: {str(e)}")
            return False

def main():
    """Función principal"""
    print("🚀 Inicializando sistema de reclutamiento...")
    print("=" * 50)
    
    # Verificar conexión a BD
    if not check_database_connection():
        print("❌ No se puede conectar a la base de datos. Verifica la configuración en .env")
        return
    
    # Crear usuarios iniciales
    create_initial_users()
    
    print("=" * 50)
    print("✅ Inicialización completada")
    print("\nPuedes ejecutar la aplicación con:")
    print("python app.py")

if __name__ == '__main__':
    main()
