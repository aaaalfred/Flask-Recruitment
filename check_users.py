#!/usr/bin/env python3
"""
Script para verificar los usuarios existentes en la base de datos
"""

from app import create_app
from extensions import db
from models import Usuario

def list_users():
    """Listar todos los usuarios"""
    app = create_app()
    
    with app.app_context():
        usuarios = Usuario.query.all()
        
        print("📋 USUARIOS EN LA BASE DE DATOS:")
        print("=" * 50)
        
        for usuario in usuarios:
            print(f"ID: {usuario.id}")
            print(f"Nombre: {usuario.nombre}")
            print(f"Email: {usuario.email}")
            print(f"Rol: {usuario.rol}")
            print(f"Activo: {usuario.activo}")
            print("-" * 30)
        
        print(f"\nTotal de usuarios: {len(usuarios)}")

if __name__ == '__main__':
    list_users()
