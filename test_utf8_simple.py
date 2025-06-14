#!/usr/bin/env python3
"""
Test simple para verificar UTF-8
"""
from app import create_app
from extensions import db
from models import Vacante, Usuario

def test_utf8_simple():
    """Prueba simple de caracteres especiales"""
    app = create_app()
    
    with app.app_context():
        # Buscar un usuario
        user = Usuario.query.first()
        if not user:
            print("❌ No hay usuarios disponibles")
            return False
        
        # Texto con acentos
        test_descripcion = "Descripción con acentos: áéíóúñü ¡Hola! ¿Cómo estás?"
        
        try:
            # Crear vacante de prueba
            test_vacante = Vacante(
                nombre="Test UTF-8 áéíóú",
                descripcion=test_descripcion,
                ejecutivo_id=user.id,
                reclutador_id=user.id,
                candidatos_requeridos=3
            )
            
            db.session.add(test_vacante)
            db.session.commit()
            
            # Recuperar y verificar
            saved = Vacante.query.filter_by(nombre="Test UTF-8 áéíóú").first()
            if saved and saved.descripcion == test_descripcion:
                print("✅ UTF-8 funciona correctamente")
                print(f"   Guardado: {saved.descripcion}")
                
                # Limpiar
                db.session.delete(saved)
                db.session.commit()
                return True
            else:
                print("❌ Los caracteres no se guardaron correctamente")
                return False
                
        except Exception as e:
            print(f"❌ Error en test UTF-8: {str(e)}")
            db.session.rollback()
            return False

if __name__ == '__main__':
    test_utf8_simple()
