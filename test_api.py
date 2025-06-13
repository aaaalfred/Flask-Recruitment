"""
Script básico para probar los endpoints principales del sistema
Ejecutar: python test_api.py
"""

import requests
import json

BASE_URL = 'http://localhost:5000/api'
headers = {'Content-Type': 'application/json'}

def test_login():
    """Test login endpoint"""
    print("🔐 Probando login...")
    login_data = {
        'email': 'admin@empresa.com',
        'password': 'admin123'
    }
    
    try:
        response = requests.post(f'{BASE_URL}/auth/login', 
                               json=login_data, 
                               headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            token = data['access_token']
            print(f"✅ Login exitoso. Token: {token[:50]}...")
            return token
        else:
            print(f"❌ Error en login: {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor. ¿Está ejecutándose?")
        return None

def test_create_candidato(token):
    """Test crear candidato"""
    print("👤 Probando crear candidato...")
    auth_headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    
    candidato_data = {
        'nombre': 'Juan Pérez González',
        'email': 'juan.perez@email.com',
        'telefono': '+52 55 1234 5678',
        'experiencia_anos': 5,
        'salario_esperado': 50000.00,
        'ubicacion': 'Ciudad de México',
        'disponibilidad': 'inmediata',
        'nivel_ingles': 'intermedio',
        'linkedin_url': 'https://linkedin.com/in/juan-perez'
    }
    
    try:
        response = requests.post(f'{BASE_URL}/candidatos',
                               json=candidato_data,
                               headers=auth_headers)
        
        if response.status_code == 201:
            candidato = response.json()['candidato']
            print(f"✅ Candidato creado: ID {candidato['id']} - {candidato['nombre']}")
            return candidato['id']
        else:
            print(f"❌ Error creando candidato: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def test_create_vacante(token):
    """Test crear vacante"""
    print("💼 Probando crear vacante...")
    auth_headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    
    vacante_data = {
        'nombre': 'Desarrollador Python Senior',
        'descripcion': 'Buscamos desarrollador Python con experiencia en Flask, Django y bases de datos',
        'reclutador_id': 2,  # ID del reclutador creado en datos iniciales
        'vacantes': 2,
        'prioridad': 'alta',
        'salario_min': 40000.00,
        'salario_max': 80000.00,
        'ubicacion': 'Ciudad de México',
        'modalidad': 'hibrido',
        'comentarios': 'Posición estratégica para el equipo de desarrollo'
    }
    
    try:
        response = requests.post(f'{BASE_URL}/vacantes',
                               json=vacante_data,
                               headers=auth_headers)
        
        if response.status_code == 201:
            vacante = response.json()['vacante']
            print(f"✅ Vacante creada: ID {vacante['id']} - {vacante['nombre']}")
            return vacante['id']
        else:
            print(f"❌ Error creando vacante: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def test_assign_candidato_to_vacante(token, candidato_id, vacante_id):
    """Test asignar candidato a vacante"""
    if not candidato_id or not vacante_id:
        print("⚠️  Saltando asignación - faltan IDs")
        return
        
    print("🔗 Probando asignar candidato a vacante...")
    auth_headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    
    asignacion_data = {
        'candidato_id': candidato_id,
        'vacante_id': vacante_id,
        'status': 'postulado',
        'nota': 'Candidato con buen perfil técnico'
    }
    
    try:
        response = requests.post(f'{BASE_URL}/candidatos-posiciones',
                               json=asignacion_data,
                               headers=auth_headers)
        
        if response.status_code == 201:
            asignacion = response.json()['asignacion']
            print(f"✅ Asignación creada: {asignacion['candidato_nombre']} → {asignacion['vacante_nombre']}")
            return asignacion['id']
        else:
            print(f"❌ Error creando asignación: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def test_create_entrevista(token, candidato_id, vacante_id):
    """Test crear entrevista"""
    if not candidato_id or not vacante_id:
        print("⚠️  Saltando entrevista - faltan IDs")
        return
        
    print("📅 Probando crear entrevista...")
    auth_headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    
    entrevista_data = {
        'fecha': '2024-12-20T10:00:00',
        'tipo': 'video',
        'candidato_id': candidato_id,
        'vacante_id': vacante_id,
        'comentarios': 'Primera entrevista técnica',
        'duracion_minutos': 60,
        'ubicacion': 'https://meet.google.com/abc-defg-hij'
    }
    
    try:
        response = requests.post(f'{BASE_URL}/entrevistas',
                               json=entrevista_data,
                               headers=auth_headers)
        
        if response.status_code == 201:
            entrevista = response.json()['entrevista']
            print(f"✅ Entrevista creada: ID {entrevista['id']} - {entrevista['tipo']}")
            return entrevista['id']
        else:
            print(f"❌ Error creando entrevista: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def test_get_candidatos(token):
    """Test listar candidatos"""
    print("📋 Probando listar candidatos...")
    auth_headers = {
        'Authorization': f'Bearer {token}'
    }
    
    try:
        response = requests.get(f'{BASE_URL}/candidatos',
                              headers=auth_headers)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Candidatos listados: {data['total']} total, {len(data['candidatos'])} en página actual")
            return True
        else:
            print(f"❌ Error listando candidatos: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_get_vacantes(token):
    """Test listar vacantes"""
    print("📋 Probando listar vacantes...")
    auth_headers = {
        'Authorization': f'Bearer {token}'
    }
    
    try:
        response = requests.get(f'{BASE_URL}/vacantes',
                              headers=auth_headers)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Vacantes listadas: {data['total']} total, {len(data['vacantes'])} en página actual")
            return True
        else:
            print(f"❌ Error listando vacantes: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def run_all_tests():
    """Ejecutar todos los tests"""
    print("🚀 Iniciando tests de la API del Sistema de Reclutamiento...")
    print("=" * 60)
    
    # Test login
    token = test_login()
    if not token:
        print("\n❌ Tests fallidos - No se pudo obtener token")
        return
    
    print()
    
    # Test crear candidato
    candidato_id = test_create_candidato(token)
    print()
    
    # Test crear vacante
    vacante_id = test_create_vacante(token)
    print()
    
    # Test asignar candidato a vacante
    asignacion_id = test_assign_candidato_to_vacante(token, candidato_id, vacante_id)
    print()
    
    # Test crear entrevista
    entrevista_id = test_create_entrevista(token, candidato_id, vacante_id)
    print()
    
    # Test listar candidatos
    test_get_candidatos(token)
    print()
    
    # Test listar vacantes
    test_get_vacantes(token)
    
    print("\n" + "=" * 60)
    print("✅ Tests completados exitosamente!")
    print("\n📊 Resumen de IDs creados:")
    if candidato_id:
        print(f"   Candidato ID: {candidato_id}")
    if vacante_id:
        print(f"   Vacante ID: {vacante_id}")
    if asignacion_id:
        print(f"   Asignación ID: {asignacion_id}")
    if entrevista_id:
        print(f"   Entrevista ID: {entrevista_id}")

if __name__ == '__main__':
    run_all_tests()
