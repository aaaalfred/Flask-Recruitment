def test_create_vacante_as_ejecutivo():
    """Probar creación de vacante como ejecutivo"""
    print("💼 Probando creación de vacante como ejecutivo...")
    
    # Login como ejecutivo
    login_data = {
        'email': 'ejecutivo@empresa.com',
        'password': 'ejecutivo123'
    }
    
    try:
        response = requests.post(
            f'{BASE_URL}/auth/login',
            json=login_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code != 200:
            print("❌ Error en login de ejecutivo")
            return None
        
        token = response.json().get('access_token')
        
        # Obtener ID de un reclutador
        reclutador_id = get_reclutador_id(token)
        if not reclutador_id:
            print("❌ No se encontró ningún reclutador")
            return None
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        
        vacante_data = {
            'nombre': 'Desarrollador Python Senior - Test',
            'descripcion': 'Posicion de prueba para desarrollador Python con Flask',
            'reclutador_id': reclutador_id,
            'vacantes': 1,
            'prioridad': 'media',
            'salario_min': 40000.00,
            'salario_max': 70000.00,
            'ubicacion': 'Ciudad de Mexico',
            'modalidad': 'hibrido'
        }
        
        response = requests.post(
            f'{BASE_URL}/vacantes',
            json=vacante_data,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 201:
            data = response.json()
            vacante_id = data.get('vacante', {}).get('id')
            print(f"✅ Vacante creada exitosamente - ID: {vacante_id}")
            return vacante_id
        else:
            print(f"❌ Error creando vacante: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"❌ Error en creación de vacante: {str(e)}")
        return None

def get_reclutador_id(token):
    """Obtener ID de un reclutador"""
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    
    try:
        response = requests.get(
            f'{BASE_URL}/usuarios',
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            usuarios = data.get('usuarios', [])
            
            # Buscar un reclutador
            for usuario in usuarios:
                if usuario.get('rol') in ['reclutador', 'reclutador_lider']:
                    return usuario.get('id')
            
            return None
        else:
            return None
            
    except Exception as e:
        print(f"❌ Error obteniendo reclutadores: {str(e)}")
        return None#!/usr/bin/env python3
"""
Script de prueba básica de la API del sistema de reclutamiento
"""

import requests
import json
import sys

BASE_URL = 'http://localhost:5000/api'

def test_server_running():
    """Verificar que el servidor esté ejecutándose"""
    try:
        response = requests.get(f'{BASE_URL}/auth/login', timeout=5)
        return True
    except requests.exceptions.ConnectionError:
        print("❌ El servidor no está ejecutándose")
        print("Ejecuta: python app.py")
        return False
    except Exception as e:
        print(f"❌ Error conectando al servidor: {str(e)}")
        return False

def test_login():
    """Probar endpoint de login"""
    print("🔐 Probando login...")
    
    login_data = {
        'email': 'reclutador@empresa.com',  # Cambiar a reclutador
        'password': 'reclutador123'
    }
    
    try:
        response = requests.post(
            f'{BASE_URL}/auth/login',
            json=login_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            if token:
                print("✅ Login exitoso")
                return token
            else:
                print("❌ No se recibió token")
                return None
        else:
            print(f"❌ Login falló: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"❌ Error en login: {str(e)}")
        return None

def test_protected_endpoint(token):
    """Probar endpoint protegido"""
    print("🔒 Probando endpoint protegido...")
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    
    try:
        response = requests.get(
            f'{BASE_URL}/usuarios',
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Endpoint protegido funciona - {len(data.get('usuarios', []))} usuarios encontrados")
            return True
        else:
            print(f"❌ Endpoint protegido falló: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ Error en endpoint protegido: {str(e)}")
        return False

def test_create_candidato(token):
    """Probar creación de candidato"""
    print("👤 Probando creación de candidato...")
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    
    candidato_data = {
        'nombre': 'Juan Perez Test',  # Sin acentos
        'email': 'juan.test@email.com',
        'telefono': '+52 55 1234 5678',
        'experiencia_anos': 3,
        'salario_esperado': 45000.00,
        'ubicacion': 'Ciudad de Mexico',  # Sin acentos
        'disponibilidad': 'inmediata',
        'nivel_ingles': 'intermedio'
    }
    
    try:
        response = requests.post(
            f'{BASE_URL}/candidatos',
            json=candidato_data,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 201:
            data = response.json()
            candidato_id = data.get('candidato', {}).get('id')
            print(f"✅ Candidato creado exitosamente - ID: {candidato_id}")
            return candidato_id
        else:
            print(f"❌ Error creando candidato: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"❌ Error en creación de candidato: {str(e)}")
        return None

def test_create_vacante(token):
    """Probar creación de vacante"""
    print("💼 Probando creación de vacante...")
    
    # Primero obtener ID de un reclutador
    reclutador_id = get_reclutador_id(token)
    if not reclutador_id:
        print("❌ No se encontró ningún reclutador")
        return None
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    
    vacante_data = {
        'nombre': 'Desarrollador Python Senior - Test',
        'descripcion': 'Posición de prueba para desarrollador Python con Flask',
        'reclutador_id': reclutador_id,  # Usar ID dinámico
        'vacantes': 1,
        'prioridad': 'media',
        'salario_min': 40000.00,
        'salario_max': 70000.00,
        'ubicacion': 'Ciudad de México',
        'modalidad': 'hibrido'
    }
    
    try:
        response = requests.post(
            f'{BASE_URL}/vacantes',
            json=vacante_data,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 201:
            data = response.json()
            vacante_id = data.get('vacante', {}).get('id')
            print(f"✅ Vacante creada exitosamente - ID: {vacante_id}")
            return vacante_id
        else:
            print(f"❌ Error creando vacante: {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"❌ Error en creación de vacante: {str(e)}")
        return None

def main():
    """Función principal de pruebas"""
    print("🧪 PRUEBAS DE LA API")
    print("=" * 50)
    
    # Verificar servidor
    if not test_server_running():
        sys.exit(1)
    
    print("✅ Servidor ejecutándose")
    print("-" * 30)
    
    # Probar login
    token = test_login()
    if not token:
        print("❌ No se puede continuar sin token")
        sys.exit(1)
    
    print("-" * 30)
    
    # Probar endpoint protegido
    if not test_protected_endpoint(token):
        print("❌ Endpoints protegidos no funcionan")
        sys.exit(1)
    
    print("-" * 30)
    
    # Probar CRUD
    candidato_id = test_create_candidato(token)
    vacante_id = test_create_vacante_as_ejecutivo()  # Nueva función
    
    print("-" * 30)
    print("=" * 50)
    
    if candidato_id and vacante_id:
        print("✅ TODAS LAS PRUEBAS BÁSICAS PASARON")
        print(f"   - Candidato creado: ID {candidato_id}")
        print(f"   - Vacante creada: ID {vacante_id}")
    else:
        print("⚠️  ALGUNAS PRUEBAS FALLARON")
        print("   - Verifica los logs del servidor")

if __name__ == '__main__':
    main()
