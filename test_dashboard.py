#!/usr/bin/env python3
"""
Script para probar el nuevo endpoint de dashboard con estadísticas mejoradas
"""

import requests
import json

# Configuración
BASE_URL = 'http://localhost:5000/api'
LOGIN_EMAIL = 'admin@empresa.com'
LOGIN_PASSWORD = 'password123'

def login_and_get_token():
    """Hacer login y obtener token JWT"""
    login_data = {
        'email': LOGIN_EMAIL,
        'password': LOGIN_PASSWORD
    }
    
    try:
        response = requests.post(f'{BASE_URL}/auth/login', json=login_data)
        if response.status_code == 200:
            data = response.json()
            token = data['access_token']
            user = data['user']
            print(f"✅ Login exitoso: {user['nombre']} ({user['rol']})")
            return token
        else:
            print(f"❌ Error en login: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error de conexión: {str(e)}")
        return None

def test_dashboard_stats(token):
    """Probar el endpoint de estadísticas del dashboard"""
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    print("\n🔍 Probando endpoint de estadísticas del dashboard...")
    
    try:
        response = requests.get(f'{BASE_URL}/reports/dashboard', headers=headers)
        
        if response.status_code == 200:
            stats = response.json()
            print("✅ Estadísticas obtenidas exitosamente!")
            
            print(f"\n📊 MÉTRICAS PRINCIPALES:")
            print(f"   • Total vacantes: {stats.get('total_vacantes', 0)}")
            print(f"   • Vacantes abiertas: {stats.get('vacantes_abiertas', 0)}")
            print(f"   • Vacantes cerradas: {stats.get('vacantes_cerradas', 0)}")
            print(f"   • Total candidatos: {stats.get('total_candidatos', 0)}")
            print(f"   • Candidatos activos: {stats.get('candidatos_activos', 0)}")
            print(f"   • Total entrevistas: {stats.get('total_entrevistas', 0)}")
            print(f"   • Entrevistas pendientes: {stats.get('entrevistas_pendientes', 0)}")
            
            print(f"\n🏢 ESTADÍSTICAS DE VACANTES:")
            por_prioridad = stats.get('vacantes_por_prioridad', {})
            for prioridad, count in por_prioridad.items():
                print(f"   • {prioridad or 'Sin prioridad'}: {count}")
            
            por_modalidad = stats.get('vacantes_por_modalidad', {})
            if por_modalidad:
                print(f"\n   Por modalidad:")
                for modalidad, count in por_modalidad.items():
                    print(f"   • {modalidad or 'Sin modalidad'}: {count}")
            
            print(f"\n👥 ESTADÍSTICAS DE CANDIDATOS:")
            por_estado = stats.get('candidatos_por_estado', {})
            for estado, count in por_estado.items():
                print(f"   • {estado or 'Sin estado'}: {count}")
            
            print(f"\n📅 ESTADÍSTICAS DE ENTREVISTAS:")
            por_tipo = stats.get('entrevistas_por_tipo', {})
            for tipo, count in por_tipo.items():
                print(f"   • {tipo or 'Sin tipo'}: {count}")
            
            # Estadísticas de usuarios (solo para ejecutivos y líderes)
            usuarios_stats = stats.get('usuarios', {})
            if usuarios_stats:
                print(f"\n👤 ESTADÍSTICAS DE USUARIOS:")
                print(f"   • Total usuarios: {usuarios_stats.get('total_usuarios', 0)}")
                por_rol = usuarios_stats.get('por_rol', {})
                for rol, count in por_rol.items():
                    print(f"   • {rol}: {count}")
            
            # Rendimiento por reclutador
            rendimiento = stats.get('rendimiento_reclutadores', [])
            if rendimiento:
                print(f"\n🏆 RENDIMIENTO POR RECLUTADOR:")
                for r in rendimiento[:5]:  # Solo top 5
                    print(f"   • {r['nombre']}: {r['candidatos']} candidatos, {r['efectividad']}% efectividad")
            
            # Vacantes que requieren atención
            vacantes_antiguas = stats.get('vacantes_antiguas', [])
            if vacantes_antiguas:
                print(f"\n⚠️ VACANTES QUE REQUIEREN ATENCIÓN:")
                for v in vacantes_antiguas[:3]:  # Solo top 3
                    print(f"   • {v['nombre']}: {v['dias_transcurridos']} días ({v['candidatos']} candidatos)")
            
            # Actividad reciente
            print(f"\n📈 ACTIVIDAD RECIENTE (últimos 7 días):")
            print(f"   • Candidatos nuevos: {stats.get('candidatos_recientes', 0)}")
            print(f"   • Entrevistas realizadas: {stats.get('entrevistas_recientes', 0)}")
            
            # Metadatos
            print(f"\n🔍 METADATOS:")
            print(f"   • Tipo de usuario: {stats.get('tipo_usuario', 'N/A')}")
            print(f"   • Última actualización: {stats.get('fecha_actualizacion', 'N/A')}")
            
            return True
        else:
            print(f"❌ Error obteniendo estadísticas: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error de conexión: {str(e)}")
        return False

def test_user_stats(token):
    """Probar el endpoint de estadísticas de usuarios"""
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    print("\n🔍 Probando endpoint de estadísticas de usuarios...")
    
    try:
        response = requests.get(f'{BASE_URL}/reports/usuarios/estadisticas', headers=headers)
        
        if response.status_code == 200:
            stats = response.json()
            print("✅ Estadísticas de usuarios obtenidas exitosamente!")
            
            print(f"\n👥 ESTADÍSTICAS DETALLADAS DE USUARIOS:")
            print(f"   • Total usuarios activos: {stats.get('total_usuarios', 0)}")
            print(f"   • Usuarios inactivos: {stats.get('usuarios_inactivos', 0)}")
            print(f"   • Usuarios nuevos (30 días): {stats.get('usuarios_recientes', 0)}")
            
            por_rol = stats.get('usuarios_por_rol', {})
            print(f"\n   Por rol:")
            for rol, count in por_rol.items():
                print(f"   • {rol}: {count}")
            
            actividad = stats.get('actividad_reclutadores', [])
            if actividad:
                print(f"\n🚀 ACTIVIDAD DE RECLUTADORES (últimos 30 días):")
                for r in actividad[:5]:  # Solo top 5
                    print(f"   • {r['nombre']}: {r['candidatos_mes']} candidatos, {r['entrevistas_mes']} entrevistas")
            
            return True
        else:
            print(f"❌ Error obteniendo estadísticas de usuarios: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error de conexión: {str(e)}")
        return False

if __name__ == '__main__':
    print("🧪 PROBANDO ESTADÍSTICAS MEJORADAS DEL DASHBOARD")
    print("=" * 60)
    
    # Login
    token = login_and_get_token()
    if not token:
        print("❌ No se pudo obtener token. Verificar credenciales y servidor.")
        exit(1)
    
    # Probar dashboard general
    success1 = test_dashboard_stats(token)
    
    # Probar estadísticas de usuarios
    success2 = test_user_stats(token)
    
    print("\n" + "=" * 60)
    if success1 and success2:
        print("🎉 TODAS LAS PRUEBAS EXITOSAS - Dashboard mejorado funcionando!")
    else:
        print("⚠️ Algunas pruebas fallaron. Revisar logs arriba.")
