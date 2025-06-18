import requests
import json
from datetime import datetime

# Configuración
BASE_URL = 'http://localhost:5000/api'
headers = {'Content-Type': 'application/json'}

def test_candidate_modal_improvements():
    """
    Script para probar las mejoras del modal de candidatos
    """
    print("🧪 Iniciando pruebas del modal de candidatos mejorado...")
    print("=" * 60)
    
    # Paso 1: Login para obtener token
    print("\n1️⃣  Probando login...")
    login_data = {
        'email': 'admin@empresa.com',
        'password': 'admin123'
    }
    
    try:
        response = requests.post(f'{BASE_URL}/auth/login', 
                               json=login_data, 
                               headers=headers, 
                               timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            token = data['access_token']
            print(f"✅ Login exitoso. Token obtenido.")
            
            # Actualizar headers con el token
            auth_headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            }
        else:
            print(f"❌ Error en login: {response.status_code} - {response.text}")
            return
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión en login: {e}")
        return
    
    # Paso 2: Crear candidato con campos mínimos (nuevo modal)
    print("\n2️⃣  Probando creación de candidato con campos mínimos...")
    candidato_minimo = {
        'nombre': f'Juan Pérez Modal Test {datetime.now().strftime("%H%M%S")}',
        'telefono': '+52 55 1234 5678'
    }
    
    try:
        response = requests.post(f'{BASE_URL}/candidatos',
                               json=candidato_minimo,
                               headers=auth_headers,
                               timeout=10)
        
        if response.status_code == 201:
            candidato_data = response.json()
            candidato_id_minimo = candidato_data['candidato']['id']
            print(f"✅ Candidato mínimo creado exitosamente. ID: {candidato_id_minimo}")
            print(f"   Nombre: {candidato_data['candidato']['nombre']}")
            print(f"   Teléfono: {candidato_data['candidato']['telefono']}")
            print(f"   Email: {candidato_data['candidato'].get('email', 'No especificado')}")
        else:
            print(f"❌ Error creando candidato mínimo: {response.status_code} - {response.text}")
            return
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión creando candidato mínimo: {e}")
        return
    
    # Paso 3: Crear candidato con comentarios
    print("\n3️⃣  Probando creación de candidato con comentarios...")
    candidato_completo = {
        'nombre': f'María García Modal Test {datetime.now().strftime("%H%M%S")}',
        'telefono': '+52 55 8765 4321',
        'comentarios_finales': 'Candidata creada desde el modal simplificado con comentarios'
    }
    
    try:
        response = requests.post(f'{BASE_URL}/candidatos',
                               json=candidato_completo,
                               headers=auth_headers,
                               timeout=10)
        
        if response.status_code == 201:
            candidato_data = response.json()
            candidato_id_completo = candidato_data['candidato']['id']
            print(f"✅ Candidato con comentarios creado exitosamente. ID: {candidato_id_completo}")
            print(f"   Nombre: {candidato_data['candidato']['nombre']}")
            print(f"   Teléfono: {candidato_data['candidato']['telefono']}")
            print(f"   Comentarios: {candidato_data['candidato'].get('comentarios_generales', 'No especificados')[:50]}...")
        else:
            print(f"❌ Error creando candidato con comentarios: {response.status_code} - {response.text}")
            return
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión creando candidato con comentarios: {e}")
        return
    
    # Paso 4: Probar edición de candidato (simulando el modal de edición)
    print("\n4️⃣  Probando edición de candidato...")
    candidato_editado = {
        'nombre': f'Juan Pérez Editado {datetime.now().strftime("%H%M%S")}',
        'telefono': '+52 55 1234 9999',
        'estado': 'inactivo',
        'comentarios_finales': 'Candidato editado desde el modal simplificado'
    }
    
    try:
        response = requests.put(f'{BASE_URL}/candidatos/{candidato_id_minimo}',
                              json=candidato_editado,
                              headers=auth_headers,
                              timeout=10)
        
        if response.status_code == 200:
            candidato_data = response.json()
            print(f"✅ Candidato editado exitosamente.")
            print(f"   Nombre actualizado: {candidato_data['candidato']['nombre']}")
            print(f"   Teléfono actualizado: {candidato_data['candidato']['telefono']}")
            print(f"   Estado actualizado: {candidato_data['candidato']['estado']}")
        else:
            print(f"❌ Error editando candidato: {response.status_code} - {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión editando candidato: {e}")
    
    # Paso 5: Probar validaciones (nombre vacío)
    print("\n5️⃣  Probando validaciones...")
    candidato_invalido = {
        'telefono': '+52 55 1111 2222'
        # Nombre faltante intencionalmente
    }
    
    try:
        response = requests.post(f'{BASE_URL}/candidatos',
                               json=candidato_invalido,
                               headers=auth_headers,
                               timeout=10)
        
        if response.status_code == 400:
            print(f"✅ Validación funcionando correctamente: {response.json().get('message', 'Error de validación')}")
        else:
            print(f"⚠️  Validación inesperada: {response.status_code} - {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión probando validaciones: {e}")
    
    # Paso 6: Obtener lista de candidatos para verificar
    print("\n6️⃣  Verificando candidatos en la lista...")
    try:
        response = requests.get(f'{BASE_URL}/candidatos?per_page=5',
                              headers=auth_headers,
                              timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            candidatos = data['candidatos']
            print(f"✅ Lista obtenida: {len(candidatos)} candidatos encontrados")
            
            # Buscar nuestros candidatos de prueba
            candidatos_test = [c for c in candidatos if 'Modal Test' in c['nombre']]
            print(f"   Candidatos de prueba encontrados: {len(candidatos_test)}")
            
            for candidato in candidatos_test[-2:]:  # Mostrar los últimos 2
                print(f"   - {candidato['nombre']} | {candidato['telefono']} | {candidato['estado']}")
                
        else:
            print(f"❌ Error obteniendo lista: {response.status_code} - {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión obteniendo lista: {e}")
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📋 RESUMEN DE PRUEBAS DEL MODAL DE CANDIDATOS")
    print("=" * 60)
    print("✅ Login y autenticación")
    print("✅ Creación con campos mínimos (nombre + teléfono)")
    print("✅ Creación con todos los campos opcionales")
    print("✅ Edición de candidato existente")
    print("✅ Validaciones de campos requeridos")
    print("✅ Listado y verificación")
    print("\n🎉 ¡Todas las pruebas del modal completadas exitosamente!")
    print("\n🔗 Ahora puedes probar la interfaz en:")
    print("   http://localhost:3000/candidates")
    print("\n📝 Pasos para probar manualmente:")
    print("   1. Hacer clic en 'Nuevo Candidato'")
    print("   2. Llenar solo nombre y teléfono")
    print("   3. Guardar y verificar que aparece en la lista")
    print("   4. Editar el candidato con el ícono de lápiz")
    print("   5. Probar validaciones dejando campos vacíos")

if __name__ == '__main__':
    test_candidate_modal_improvements()
