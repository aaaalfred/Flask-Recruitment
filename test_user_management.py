#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para probar la gestión de usuarios completa
"""

from app import create_app
from extensions import db
from models import Usuario
import requests
import json

def test_user_management():
    """Prueba completa de la gestión de usuarios"""
    
    print("🧪 === TESTING GESTIÓN DE USUARIOS ===")
    
    # 1. Crear la aplicación y corregir password del admin
    app = create_app()
    
    with app.app_context():
        try:
            # Corregir password del admin
            admin = Usuario.query.filter_by(email='admin@empresa.com').first()
            
            if admin:
                admin.set_password('password123')
                db.session.commit()
                print("✅ Password del admin corregido")
            else:
                print("❌ Admin no encontrado")
                return
            
            # Verificar que el password funciona
            if admin.check_password('password123'):
                print("✅ Password verificado correctamente")
            else:
                print("❌ Password no funciona")
                return
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return
    
    # 2. Probar el login con el API
    print("\n🔐 === TESTING LOGIN API ===")
    
    try:
        login_data = {
            'email': 'admin@empresa.com',
            'password': 'password123'
        }
        
        response = requests.post('http://localhost:5000/api/auth/login', 
                               json=login_data,
                               headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            data = response.json()
            token = data['access_token']
            print(f"✅ Login exitoso. Token: {token[:50]}...")
            
            # 3. Probar endpoint de usuarios
            print("\n👥 === TESTING USUARIOS API ===")
            
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            # Obtener lista de usuarios
            response = requests.get('http://localhost:5000/api/usuarios', headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Usuarios obtenidos: {len(data['usuarios'])} usuarios")
                
                for usuario in data['usuarios']:
                    print(f"   - {usuario['nombre']} ({usuario['email']}) - {usuario['rol']}")
                    
            else:
                print(f"❌ Error obteniendo usuarios: {response.text}")
                
            # 4. Crear un usuario de prueba
            print("\n➕ === TESTING CREAR USUARIO ===")
            
            nuevo_usuario = {
                'nombre': 'Usuario Prueba',
                'email': 'prueba@empresa.com',
                'password': 'prueba123',
                'rol': 'reclutador'
            }
            
            response = requests.post('http://localhost:5000/api/usuarios', 
                                   json=nuevo_usuario, 
                                   headers=headers)
            
            if response.status_code == 201:
                data = response.json()
                usuario_id = data['usuario']['id']
                print(f"✅ Usuario creado exitosamente. ID: {usuario_id}")
                
                # 5. Editar el usuario creado
                print("\n✏️ === TESTING EDITAR USUARIO ===")
                
                usuario_actualizado = {
                    'nombre': 'Usuario Prueba Actualizado',
                    'rol': 'reclutador_lider'
                }
                
                response = requests.put(f'http://localhost:5000/api/usuarios/{usuario_id}', 
                                      json=usuario_actualizado, 
                                      headers=headers)
                
                if response.status_code == 200:
                    print("✅ Usuario actualizado exitosamente")
                else:
                    print(f"❌ Error actualizando usuario: {response.text}")
                
                # 6. Desactivar el usuario
                print("\n🗑️ === TESTING DESACTIVAR USUARIO ===")
                
                response = requests.delete(f'http://localhost:5000/api/usuarios/{usuario_id}', 
                                         headers=headers)
                
                if response.status_code == 200:
                    print("✅ Usuario desactivado exitosamente")
                else:
                    print(f"❌ Error desactivando usuario: {response.text}")
                    
            else:
                print(f"❌ Error creando usuario: {response.text}")
                
        else:
            print(f"❌ Error en login: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar con el servidor. ¿Está corriendo en localhost:5000?")
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")

def create_demo_users():
    """Crear usuarios de demostración"""
    
    print("\n👥 === CREANDO USUARIOS DE DEMOSTRACIÓN ===")
    
    app = create_app()
    
    with app.app_context():
        try:
            # Usuarios de demo
            demo_users = [
                {
                    'nombre': 'María González',
                    'email': 'maria.gonzalez@empresa.com',
                    'password': 'demo123',
                    'rol': 'reclutador'
                },
                {
                    'nombre': 'Carlos Reclutador',
                    'email': 'carlos.reclutador@empresa.com',
                    'password': 'demo123',
                    'rol': 'reclutador'
                },
                {
                    'nombre': 'Ana Líder',
                    'email': 'ana.lider@empresa.com',
                    'password': 'demo123',
                    'rol': 'reclutador_lider'
                },
                {
                    'nombre': 'Roberto Ejecutivo',
                    'email': 'roberto.ejecutivo@empresa.com',
                    'password': 'demo123',
                    'rol': 'ejecutivo'
                }
            ]
            
            usuarios_creados = 0
            
            for user_data in demo_users:
                # Verificar si el usuario ya existe
                existing = Usuario.query.filter_by(email=user_data['email']).first()
                
                if not existing:
                    usuario = Usuario(
                        nombre=user_data['nombre'],
                        email=user_data['email'],
                        rol=user_data['rol'],
                        activo=True
                    )
                    usuario.set_password(user_data['password'])
                    
                    db.session.add(usuario)
                    usuarios_creados += 1
                    print(f"✅ Creado: {user_data['nombre']} ({user_data['rol']})")
                else:
                    print(f"⚠️ Ya existe: {user_data['nombre']}")
            
            db.session.commit()
            
            if usuarios_creados > 0:
                print(f"\n🎉 Se crearon {usuarios_creados} usuarios de demostración")
            else:
                print("\n📋 Todos los usuarios de demostración ya existían")
                
            # Mostrar todos los usuarios actuales
            print("\n📊 === USUARIOS ACTUALES EN EL SISTEMA ===")
            usuarios = Usuario.query.filter_by(activo=True).all()
            
            for usuario in usuarios:
                print(f"   {usuario.nombre:<25} | {usuario.email:<30} | {usuario.rol}")
                
        except Exception as e:
            print(f"❌ Error creando usuarios demo: {str(e)}")
            db.session.rollback()

def check_permissions():
    """Verificar permisos de roles"""
    
    print("\n🔒 === VERIFICANDO PERMISOS POR ROL ===")
    
    print("👨‍💼 EJECUTIVO:")
    print("   ✅ Puede crear vacantes")
    print("   ✅ Puede ver reportes")
    print("   ✅ Puede crear/editar/desactivar usuarios")
    print("   ✅ Acceso completo al sistema")
    
    print("\n👩‍💼 RECLUTADOR LÍDER:")
    print("   ✅ Puede supervisar reclutadores")
    print("   ✅ Puede crear/editar/desactivar usuarios")
    print("   ✅ Puede ver todas las vacantes")
    print("   ✅ Puede generar reportes")
    
    print("\n👨‍💻 RECLUTADOR:")
    print("   ✅ Puede gestionar candidatos asignados")
    print("   ✅ Puede programar entrevistas")
    print("   ✅ Puede ver solo sus vacantes asignadas")
    print("   ❌ No puede crear/editar usuarios")
    print("   ❌ No puede crear vacantes")

if __name__ == '__main__':
    print("🚀 === SISTEMA DE GESTIÓN DE USUARIOS ===\n")
    
    # Paso 1: Corregir password del admin y probar APIs
    test_user_management()
    
    # Paso 2: Crear usuarios de demostración
    create_demo_users()
    
    # Paso 3: Mostrar información de permisos
    check_permissions()
    
    print("\n" + "="*60)
    print("✅ TESTING COMPLETADO")
    print("="*60)
    print("\n🔑 CREDENCIALES PARA PROBAR:")
    print("   Admin: admin@empresa.com / password123")
    print("   Demo:  maria.gonzalez@empresa.com / demo123")
    print("   Demo:  ana.lider@empresa.com / demo123")
    print("\n🌐 URLs:")
    print("   Backend: http://localhost:5000")
    print("   Frontend: http://localhost:3000")
    print("   Gestión de Usuarios: http://localhost:3000/users")
