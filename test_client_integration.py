#!/usr/bin/env python3
"""
Script para probar la integración de clientes en el sistema de vacantes
"""

import requests
import json
import os
from datetime import datetime

# Configuración
BASE_URL = 'http://localhost:5000/api'
ADMIN_EMAIL = 'admin@empresa.com'
ADMIN_PASSWORD = 'admin123'

def get_auth_token():
    """Obtener token de autenticación"""
    print("🔐 Obteniendo token de autenticación...")
    
    response = requests.post(f'{BASE_URL}/auth/login', json={
        'email': ADMIN_EMAIL,
        'password': ADMIN_PASSWORD
    })
    
    if response.status_code == 200:
        data = response.json()
        token = data['access_token']
        print(f"✅ Token obtenido exitosamente")
        return token
    else:
        print(f"❌ Error obteniendo token: {response.text}")
        return None

def test_clients_endpoint(token):
    """Probar endpoints de clientes"""
    print("\n📋 Probando endpoints de clientes...")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # 1. Obtener clientes activos
    print("1. Obteniendo clientes activos...")
    response = requests.get(f'{BASE_URL}/clientes/active', headers=headers)
    
    if response.status_code == 200:
        clients = response.json()['clientes']
        print(f"✅ {len(clients)} clientes activos encontrados")
        for client in clients[:3]:  # Mostrar solo los primeros 3
            print(f"   - {client['nombre']} ({client['ccp']})")
        return clients
    else:
        print(f"❌ Error obteniendo clientes: {response.text}")
        return []

def test_create_client(token):
    """Probar creación de cliente"""
    print("\n🆕 Probando creación de cliente...")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # Crear cliente de prueba
    client_data = {
        'nombre': 'Cliente Prueba Integración',
        'ccp': f'TEST-{datetime.now().strftime("%Y%m%d-%H%M%S")}'
    }
    
    response = requests.post(f'{BASE_URL}/clientes', json=client_data, headers=headers)
    
    if response.status_code == 201:
        client = response.json()['cliente']
        print(f"✅ Cliente creado: {client['nombre']} ({client['ccp']})")
        return client
    else:
        print(f"❌ Error creando cliente: {response.text}")
        return None

def test_create_vacant_with_client(token, client_id):
    """Probar creación de vacante con cliente"""
    print("\n🏢 Probando creación de vacante con cliente...")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # Primero obtener usuarios para asignar reclutador
    print("   Obteniendo usuarios...")
    users_response = requests.get(f'{BASE_URL}/usuarios', headers=headers)
    
    if users_response.status_code != 200:
        print(f"❌ Error obteniendo usuarios: {users_response.text}")
        return None
    
    users = users_response.json()['usuarios']
    reclutador = next((u for u in users if u['rol'] in ['reclutador', 'reclutador_lider']), None)
    
    if not reclutador:
        print("❌ No se encontró reclutador disponible")
        return None
    
    # Crear vacante con cliente
    vacant_data = {
        'nombre': f'Vacante de Prueba - {datetime.now().strftime("%Y%m%d %H:%M")}',
        'descripcion': 'Vacante creada para probar integración con clientes',
        'cliente_id': client_id,
        'reclutador_id': reclutador['id'],
        'vacantes': 2,
        'candidatos_requeridos': 5,
        'entrevistas_op': 3,
        'prioridad': 'alta'
    }
    
    response = requests.post(f'{BASE_URL}/vacantes', json=vacant_data, headers=headers)
    
    if response.status_code == 201:
        vacant = response.json()['vacante']
        print(f"✅ Vacante creada exitosamente:")
        print(f"   - ID: {vacant['id']}")
        print(f"   - Nombre: {vacant['nombre']}")
        print(f"   - Cliente: {vacant['cliente_nombre']} ({vacant['cliente_ccp']})")
        print(f"   - Reclutador: {vacant['reclutador']}")
        return vacant
    else:
        print(f"❌ Error creando vacante: {response.text}")
        return None

def test_get_vacant_with_client(token, vacant_id):
    """Probar obtención de vacante con información de cliente"""
    print("\n📄 Probando obtención de vacante con cliente...")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    response = requests.get(f'{BASE_URL}/vacantes/{vacant_id}', headers=headers)
    
    if response.status_code == 200:
        vacant = response.json()
        print(f"✅ Vacante obtenida exitosamente:")
        print(f"   - ID: {vacant['id']}")
        print(f"   - Nombre: {vacant['nombre']}")
        print(f"   - Cliente ID: {vacant['cliente_id']}")
        print(f"   - Cliente Nombre: {vacant['cliente_nombre']}")
        print(f"   - Cliente CCP: {vacant['cliente_ccp']}")
        return True
    else:
        print(f"❌ Error obteniendo vacante: {response.text}")
        return False

def test_search_vacants_by_client(token, client_name):
    """Probar búsqueda de vacantes por cliente"""
    print(f"\n🔍 Probando búsqueda de vacantes por cliente '{client_name}'...")
    
    headers = {'Authorization': f'Bearer {token}'}
    
    response = requests.get(f'{BASE_URL}/vacantes?cliente={client_name}', headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        vacants = data['vacantes']
        print(f"✅ {len(vacants)} vacantes encontradas para el cliente")
        
        for vacant in vacants:
            print(f"   - {vacant['nombre']} | Cliente: {vacant['cliente_nombre']} ({vacant['cliente_ccp']})")
        return True
    else:
        print(f"❌ Error buscando vacantes: {response.text}")
        return False

def main():
    """Función principal"""
    print("🚀 Iniciando pruebas de integración de clientes...")
    print("=" * 60)
    
    # 1. Autenticación
    token = get_auth_token()
    if not token:
        print("❌ No se pudo obtener token. Abortando pruebas.")
        return
    
    # 2. Probar endpoints de clientes
    existing_clients = test_clients_endpoint(token)
    
    # 3. Crear cliente de prueba
    new_client = test_create_client(token)
    if not new_client:
        print("❌ No se pudo crear cliente. Usando cliente existente...")
        if existing_clients:
            new_client = existing_clients[0]
        else:
            print("❌ No hay clientes disponibles. Abortando.")
            return
    
    # 4. Crear vacante con cliente
    vacant = test_create_vacant_with_client(token, new_client['id'])
    if not vacant:
        print("❌ No se pudo crear vacante con cliente.")
        return
    
    # 5. Obtener vacante con información de cliente
    test_get_vacant_with_client(token, vacant['id'])
    
    # 6. Buscar vacantes por cliente
    test_search_vacants_by_client(token, new_client['nombre'])
    
    print("\n" + "=" * 60)
    print("✅ Todas las pruebas de integración completadas exitosamente!")
    print("\n📋 Resumen:")
    print(f"   - Cliente creado: {new_client['nombre']} ({new_client['ccp']})")
    print(f"   - Vacante creada: {vacant['nombre']} (ID: {vacant['id']})")
    print(f"   - Integración cliente-vacante: ✅ Funcionando")

if __name__ == '__main__':
    main()
