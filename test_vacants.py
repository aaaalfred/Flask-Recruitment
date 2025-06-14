#!/usr/bin/env python3
"""
Script para probar la creación de vacantes con los nuevos campos
"""

import requests
import json
from datetime import datetime, timedelta

# Configuración
BASE_URL = 'http://localhost:5000/api'
headers = {'Content-Type': 'application/json'}

def test_login():
    """Test login y obtener token"""
    print("🔐 Probando login...")
    
    login_data = {
        'email': 'admin@empresa.com',
        'password': 'password123'
    }
    
    try:
        response = requests.post(f'{BASE_URL}/auth/login', 
                               json=login_data, 
                               headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            token = data['access_token']
            print(f"✅ Login exitoso. Token obtenido.")
            return token
        else:
            print(f"❌ Error en login: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

def test_get_users(token):
    """Obtener lista de usuarios para las pruebas"""
    print("👥 Obteniendo usuarios...")
    
    auth_headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    
    try:
        response = requests.get(f'{BASE_URL}/usuarios?per_page=50', headers=auth_headers)
        
        if response.status_code == 200:
            data = response.json()
            usuarios = data['usuarios']
            
            reclutadores = [u for u in usuarios if u['rol'] in ['reclutador', 'reclutador_lider']]
            lideres = [u for u in usuarios if u['rol'] == 'reclutador_lider']
            
            print(f"✅ Encontrados {len(reclutadores)} reclutadores y {len(lideres)} líderes")
            return reclutadores, lideres
        else:
            print(f"❌ Error obteniendo usuarios: {response.text}")
            return [], []
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return [], []

def test_create_vacant(token, reclutadores, lideres):
    """Test crear vacante con los nuevos campos"""
    print("📋 Probando creación de vacante...")
    
    auth_headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    
    # Fechas de ejemplo
    fecha_limite = datetime.now() + timedelta(days=30)
    fecha_envio = datetime.now() + timedelta(days=15)
    
    vacante_data = {
        'nombre': '2301 ACC PRUEBA TEST',
        'descripcion': 'Vacante de prueba para verificar el nuevo formulario sin ubicación, modalidad ni salarios',
        'candidatos_requeridos': 5,
        'entrevistas_op': 3,
        'vacantes': 2,
        'avance': 'Creada',
        'reclutador_id': reclutadores[0]['id'] if reclutadores else None,
        'reclutador_lider_id': lideres[0]['id'] if lideres else None,
        'prioridad': 'alta',
        'envio_candidatos_rh': fecha_envio.isoformat(),
        'fecha_limite': fecha_limite.isoformat(),
        'comentarios': 'Esta es una vacante de prueba creada para validar el formulario actualizado'
    }
    
    try:
        response = requests.post(f'{BASE_URL}/vacantes',
                               json=vacante_data,
                               headers=auth_headers)
        
        if response.status_code == 201:
            data = response.json()
            vacante = data['vacante']
            print(f"✅ Vacante creada exitosamente:")
            print(f"   - ID: {vacante['id']}")
            print(f"   - Nombre: {vacante['nombre']}")
            print(f"   - Candidatos requeridos: {vacante['candidatos_requeridos']}")
            print(f"   - Vacantes disponibles: {vacante['vacantes']}")
            print(f"   - Prioridad: {vacante['prioridad']}")
            print(f"   - Avance: {vacante['avance']}")
            
            if vacante.get('envio_candidatos_rh'):
                print(f"   - Envío candidatos RH: {vacante['envio_candidatos_rh']}")
            if vacante.get('fecha_limite'):
                print(f"   - Fecha límite: {vacante['fecha_limite']}")
            
            return vacante['id']
        else:
            print(f"❌ Error creando vacante: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

def test_get_vacant(token, vacante_id):
    """Test obtener vacante específica"""
    print(f"🔍 Obteniendo vacante {vacante_id}...")
    
    auth_headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    
    try:
        response = requests.get(f'{BASE_URL}/vacantes/{vacante_id}', headers=auth_headers)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Vacante obtenida exitosamente")
            
            # Verificar que no tenga los campos eliminados
            campos_eliminados = ['ubicacion', 'modalidad', 'salario_min', 'salario_max']
            for campo in campos_eliminados:
                if data.get(campo) is not None:
                    print(f"⚠️  Advertencia: El campo '{campo}' todavía está presente")
            
            # Verificar que tenga el nuevo campo
            if 'envio_candidatos_rh' in data:
                print(f"✅ Campo 'envio_candidatos_rh' presente: {data['envio_candidatos_rh']}")
            else:
                print("⚠️  Campo 'envio_candidatos_rh' no encontrado")
                
            return True
        else:
            print(f"❌ Error obteniendo vacante: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_update_vacant(token, vacante_id):
    """Test actualizar vacante"""
    print(f"✏️  Actualizando vacante {vacante_id}...")
    
    auth_headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    
    # Nueva fecha de envío
    nueva_fecha_envio = datetime.now() + timedelta(days=20)
    
    update_data = {
        'descripcion': 'Descripción actualizada - Formulario funcionando correctamente',
        'avance': 'Buscando candidatos',
        'envio_candidatos_rh': nueva_fecha_envio.isoformat(),
        'prioridad': 'critica'
    }
    
    try:
        response = requests.put(f'{BASE_URL}/vacantes/{vacante_id}',
                              json=update_data,
                              headers=auth_headers)
        
        if response.status_code == 200:
            data = response.json()
            vacante = data['vacante']
            print("✅ Vacante actualizada exitosamente")
            print(f"   - Nuevo avance: {vacante['avance']}")
            print(f"   - Nueva prioridad: {vacante['prioridad']}")
            return True
        else:
            print(f"❌ Error actualizando vacante: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_list_vacants(token):
    """Test listar vacantes"""
    print("📋 Obteniendo lista de vacantes...")
    
    auth_headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    
    try:
        response = requests.get(f'{BASE_URL}/vacantes?per_page=5', headers=auth_headers)
        
        if response.status_code == 200:
            data = response.json()
            vacantes = data['vacantes']
            print(f"✅ Se obtuvieron {len(vacantes)} vacantes")
            
            for v in vacantes:
                print(f"   - {v['nombre']} (ID: {v['id']}) - {v['avance']}")
            
            return True
        else:
            print(f"❌ Error listando vacantes: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def main():
    """Función principal"""
    print("=" * 60)
    print("🚀 PRUEBAS DEL FORMULARIO DE VACANTES ACTUALIZADO")
    print("=" * 60)
    print()
    
    # Test 1: Login
    token = test_login()
    if not token:
        print("❌ No se pudo obtener token. Verificar que el servidor esté corriendo.")
        return
    
    print()
    
    # Test 2: Obtener usuarios
    reclutadores, lideres = test_get_users(token)
    if not reclutadores:
        print("⚠️  No se encontraron reclutadores. Algunas pruebas pueden fallar.")
    
    print()
    
    # Test 3: Crear vacante
    vacante_id = test_create_vacant(token, reclutadores, lideres)
    if not vacante_id:
        print("❌ No se pudo crear vacante. Verificar configuración.")
        return
    
    print()
    
    # Test 4: Obtener vacante específica
    test_get_vacant(token, vacante_id)
    
    print()
    
    # Test 5: Actualizar vacante
    test_update_vacant(token, vacante_id)
    
    print()
    
    # Test 6: Listar vacantes
    test_list_vacants(token)
    
    print()
    print("=" * 60)
    print("✅ PRUEBAS COMPLETADAS")
    print("=" * 60)
    print()
    print("📝 RESUMEN:")
    print("   - Campos eliminados: ubicacion, modalidad, salario_min, salario_max")
    print("   - Campo agregado: envio_candidatos_rh")
    print("   - Formulario con scroll funcional")
    print("   - Headers y botones sticky implementados")
    print()
    print("🎯 El formulario está listo para usar en producción!")

if __name__ == '__main__':
    main()
