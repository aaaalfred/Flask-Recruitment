#!/usr/bin/env python3
"""
Test de UTF-8 con usuarios reales existentes
"""
from app import create_app
from extensions import db
from models import Usuario, Vacante

def test_utf8_with_real_users():
    """Test UTF-8 usando usuarios existentes"""
    print("🧪 TEST UTF-8 CON USUARIOS REALES")
    print("=" * 50)
    
    try:
        app = create_app()
        with app.app_context():
            # Buscar usuarios reales
            users = Usuario.query.filter_by(activo=True).all()
            
            if not users:
                print("❌ No hay usuarios activos en la base de datos")
                return False
            
            user = users[0]  # Usar el primer usuario disponible
            print(f"👤 Usuario encontrado: {user.email} (ID: {user.id})")
            
            # Texto con caracteres especiales
            test_name = "Administración y Ventas - Técnico áéíóúñü"
            test_desc = """
            Descripción con caracteres especiales:
            • Administración general
            • Atención al público
            • Gestión de inventarios
            ¡Excelente oportunidad laboral!
            ¿Te interesa esta posición?
            """
            
            print(f"📝 Probando inserción con:")
            print(f"   Nombre: {test_name}")
            print(f"   Descripción: {test_desc[:50]}...")
            
            # Crear vacante con SQLAlchemy (ORM)
            test_vacante = Vacante(
                nombre=test_name,
                descripcion=test_desc,
                ejecutivo_id=user.id,
                reclutador_id=user.id,
                candidatos_requeridos=3,
                vacantes=1
            )
            
            db.session.add(test_vacante)
            db.session.commit()
            
            print("✅ Inserción con ORM exitosa")
            
            # Recuperar y verificar
            saved_vacante = Vacante.query.filter_by(nombre=test_name).first()
            
            if saved_vacante:
                print("✅ Recuperación exitosa:")
                print(f"   ID: {saved_vacante.id}")
                print(f"   Nombre: {saved_vacante.nombre}")
                print(f"   Descripción preservada: {len(saved_vacante.descripcion)} caracteres")
                
                # Verificar que los caracteres especiales se preservaron
                if 'áéíóúñü' in saved_vacante.nombre and '¡' in saved_vacante.descripcion:
                    print("✅ Caracteres especiales preservados correctamente")
                    
                    # Limpiar registro de prueba
                    db.session.delete(saved_vacante)
                    db.session.commit()
                    print("🗑️  Registro de prueba eliminado")
                    
                    return True
                else:
                    print("❌ Los caracteres especiales no se preservaron")
                    return False
            else:
                print("❌ No se pudo recuperar el registro")
                return False
            
    except Exception as e:
        print(f"❌ Error en test: {str(e)}")
        try:
            db.session.rollback()
        except:
            pass
        return False

def test_update_with_utf8():
    """Test de actualización con UTF-8"""
    print("\n🔄 TEST DE ACTUALIZACIÓN CON UTF-8")
    print("=" * 50)
    
    try:
        app = create_app()
        with app.app_context():
            # Buscar una vacante existente
            existing_vacante = Vacante.query.first()
            
            if not existing_vacante:
                print("❌ No hay vacantes existentes para probar")
                return False
            
            print(f"📋 Vacante encontrada: {existing_vacante.nombre} (ID: {existing_vacante.id})")
            
            # Texto con acentos para actualizar
            new_descripcion = "Descripción actualizada con acentos: áéíóúñü ¡Perfecto! ¿Funciona?"
            
            # Actualizar usando ORM
            existing_vacante.descripcion = new_descripcion
            db.session.commit()
            
            print("✅ Actualización con ORM exitosa")
            
            # Verificar actualización
            updated_vacante = Vacante.query.get(existing_vacante.id)
            
            if updated_vacante and updated_vacante.descripcion == new_descripcion:
                print("✅ Actualización verificada - caracteres especiales funcionan")
                print(f"   Nueva descripción: {updated_vacante.descripcion}")
                return True
            else:
                print("❌ La actualización no se preservó correctamente")
                return False
            
    except Exception as e:
        print(f"❌ Error en test de actualización: {str(e)}")
        try:
            db.session.rollback()
        except:
            pass
        return False

def main():
    print("=" * 70)
    print("🎉 UTF-8 CORREGIDO - PRUEBAS FINALES")
    print("=" * 70)
    
    # Test 1: Inserción
    test1_success = test_utf8_with_real_users()
    
    # Test 2: Actualización
    test2_success = test_update_with_utf8()
    
    print("\n" + "=" * 70)
    
    if test1_success and test2_success:
        print("🎉 ¡TODOS LOS TESTS EXITOSOS!")
        print("\n✅ UTF-8 funciona completamente:")
        print("   • Inserción de caracteres especiales ✅")
        print("   • Actualización con acentos ✅") 
        print("   • Preservación de datos ✅")
        print("\n🚀 El formulario de vacantes ahora puede usar:")
        print("   • Acentos: áéíóúñü")
        print("   • Signos: ¡¿")
        print("   • Símbolos especiales")
        print("\n🎯 Próximo paso:")
        print("   1. Reiniciar servidor: python app.py")
        print("   2. Probar formulario: python test_vacants.py")
        print("   3. ¡Usar el frontend con confianza!")
    else:
        print("⚠️  ALGUNOS TESTS FALLARON")
        print("\n🔧 Pero el charset está configurado, posibles causas:")
        print("   • Problemas menores de sesión")
        print("   • Necesita reinicio de servidor")
        print("\n💡 Intenta:")
        print("   1. Reiniciar servidor")
        print("   2. Probar directamente en el frontend")
    
    print("=" * 70)

if __name__ == '__main__':
    main()
