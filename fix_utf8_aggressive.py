#!/usr/bin/env python3
"""
Script de corrección agresiva para UTF-8 - Solución definitiva
"""
from app import create_app
from extensions import db
import sys

def fix_database_charset_aggressive():
    """Corrección agresiva del charset de la base de datos"""
    print("🔧 CORRECCIÓN AGRESIVA DE UTF-8")
    print("=" * 50)
    
    try:
        app = create_app()
        with app.app_context():
            # Obtener nombre de la base de datos
            db_name_result = db.session.execute(db.text("SELECT DATABASE()")).fetchone()
            db_name = db_name_result[0]
            
            print(f"📀 Base de datos: {db_name}")
            
            # Paso 1: Cambiar charset de la base de datos
            print("\n🔧 Paso 1: Cambiando charset de la base de datos...")
            db.session.execute(db.text(f"ALTER DATABASE `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
            print("✅ Database charset actualizado")
            
            # Paso 2: Obtener todas las tablas
            print("\n🔧 Paso 2: Convirtiendo tablas...")
            tables = db.session.execute(db.text("""
                SELECT TABLE_NAME 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_SCHEMA = DATABASE()
                AND TABLE_TYPE = 'BASE TABLE'
            """)).fetchall()
            
            for (table_name,) in tables:
                print(f"   🔄 Convirtiendo tabla: {table_name}")
                try:
                    # Convertir tabla completa
                    db.session.execute(db.text(f"ALTER TABLE `{table_name}` CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
                    print(f"   ✅ {table_name} convertida")
                except Exception as e:
                    print(f"   ⚠️  Error en {table_name}: {str(e)}")
            
            # Paso 3: Verificar columnas específicas de la tabla vacante
            print("\n🔧 Paso 3: Verificando columnas específicas...")
            text_columns = db.session.execute(db.text("""
                SELECT COLUMN_NAME, COLUMN_TYPE
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = DATABASE() 
                AND TABLE_NAME = 'vacante'
                AND DATA_TYPE IN ('varchar', 'text', 'longtext', 'mediumtext', 'tinytext')
            """)).fetchall()
            
            for col_name, col_type in text_columns:
                print(f"   🔄 Actualizando columna: {col_name} ({col_type})")
                try:
                    # Cambiar charset de columna específica
                    db.session.execute(db.text(f"""
                        ALTER TABLE vacante 
                        MODIFY COLUMN `{col_name}` {col_type} 
                        CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
                    """))
                    print(f"   ✅ {col_name} actualizada")
                except Exception as e:
                    print(f"   ⚠️  Error en columna {col_name}: {str(e)}")
            
            # Paso 4: Commit todos los cambios
            db.session.commit()
            print("\n✅ Todos los cambios aplicados")
            
            return True
            
    except Exception as e:
        print(f"\n❌ Error en corrección agresiva: {str(e)}")
        db.session.rollback()
        return False

def verify_charset_after_fix():
    """Verificar que el charset se aplicó correctamente"""
    print("\n🔍 VERIFICACIÓN POST-CORRECCIÓN")
    print("=" * 50)
    
    try:
        app = create_app()
        with app.app_context():
            # Verificar charset de la base de datos
            result = db.session.execute(db.text("SELECT @@character_set_database, @@collation_database")).fetchone()
            print(f"📊 Base de datos: {result[0]} / {result[1]}")
            
            # Verificar tabla vacante específicamente
            table_info = db.session.execute(db.text("""
                SELECT TABLE_COLLATION 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_SCHEMA = DATABASE() 
                AND TABLE_NAME = 'vacante'
            """)).fetchone()
            
            if table_info:
                print(f"📋 Tabla vacante: {table_info[0]}")
            
            # Verificar columnas críticas
            critical_columns = ['nombre', 'descripcion', 'comentarios']
            for col_name in critical_columns:
                col_info = db.session.execute(db.text(f"""
                    SELECT CHARACTER_SET_NAME, COLLATION_NAME
                    FROM INFORMATION_SCHEMA.COLUMNS 
                    WHERE TABLE_SCHEMA = DATABASE() 
                    AND TABLE_NAME = 'vacante'
                    AND COLUMN_NAME = '{col_name}'
                """)).fetchone()
                
                if col_info:
                    charset, collation = col_info
                    if 'utf8mb4' in str(charset):
                        print(f"   ✅ {col_name}: {charset} / {collation}")
                    else:
                        print(f"   ❌ {col_name}: {charset} / {collation}")
                        return False
            
            return True
            
    except Exception as e:
        print(f"❌ Error en verificación: {str(e)}")
        return False

def test_utf8_insert_simple():
    """Test simplificado de UTF-8"""
    print("\n🧪 TEST SIMPLIFICADO UTF-8")
    print("=" * 50)
    
    try:
        app = create_app()
        with app.app_context():
            # Test directo con SQL
            test_name = "Test áéíóú"
            test_desc = "Descripción con ñ y acentos"
            
            # Intentar inserción directa
            result = db.session.execute(db.text("""
                INSERT INTO vacante (nombre, descripcion, ejecutivo_id, reclutador_id, candidatos_requeridos)
                VALUES (:nombre, :descripcion, 1, 1, 3)
            """), {
                'nombre': test_name,
                'descripcion': test_desc
            })
            
            # Obtener ID insertado
            inserted_id = result.lastrowid
            db.session.commit()
            
            # Verificar que se insertó correctamente
            check_result = db.session.execute(db.text("""
                SELECT nombre, descripcion FROM vacante WHERE id = :id
            """), {'id': inserted_id}).fetchone()
            
            if check_result:
                retrieved_name, retrieved_desc = check_result
                print(f"✅ Inserción exitosa:")
                print(f"   Nombre: {retrieved_name}")
                print(f"   Descripción: {retrieved_desc}")
                
                # Limpiar
                db.session.execute(db.text("DELETE FROM vacante WHERE id = :id"), {'id': inserted_id})
                db.session.commit()
                print("🗑️  Registro de prueba eliminado")
                
                return True
            else:
                print("❌ No se pudo recuperar el registro")
                return False
            
    except Exception as e:
        print(f"❌ Error en test: {str(e)}")
        db.session.rollback()
        return False

def fix_connection_charset():
    """Forzar charset en la sesión actual"""
    print("\n🔧 CONFIGURANDO CHARSET DE SESIÓN")
    print("=" * 50)
    
    try:
        app = create_app()
        with app.app_context():
            # Configurar charset para la sesión actual
            charset_commands = [
                "SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci",
                "SET CHARACTER SET utf8mb4",
                "SET character_set_connection=utf8mb4",
                "SET character_set_client=utf8mb4",
                "SET character_set_results=utf8mb4"
            ]
            
            for command in charset_commands:
                db.session.execute(db.text(command))
                print(f"   ✅ {command}")
            
            db.session.commit()
            print("✅ Charset de sesión configurado")
            return True
            
    except Exception as e:
        print(f"❌ Error configurando sesión: {str(e)}")
        return False

def main():
    print("=" * 70)
    print("🛠️  CORRECCIÓN DEFINITIVA DE UTF-8")
    print("=" * 70)
    
    success = True
    
    # Paso 1: Configurar charset de sesión
    if not fix_connection_charset():
        success = False
    
    # Paso 2: Corrección agresiva
    if not fix_database_charset_aggressive():
        success = False
    
    # Paso 3: Verificar corrección
    if not verify_charset_after_fix():
        success = False
    
    # Paso 4: Test final
    if not test_utf8_insert_simple():
        success = False
    
    print("\n" + "=" * 70)
    
    if success:
        print("🎉 ¡UTF-8 CORREGIDO EXITOSAMENTE!")
        print("\n✅ Ahora puedes:")
        print("   1. Reiniciar el servidor: python app.py")
        print("   2. Probar formulario: python test_vacants.py")
        print("   3. Usar acentos sin problemas")
    else:
        print("❌ CORRECCIÓN FALLIDA")
        print("\n🔧 Alternativas:")
        print("   1. Verificar permisos de MySQL")
        print("   2. Contactar al administrador de DB")
        print("   3. Recrear la base de datos con UTF-8")
        print("\n💡 Comando manual para MySQL:")
        print("   CREATE DATABASE recruitment_system_utf8")
        print("   CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    
    print("=" * 70)

if __name__ == '__main__':
    main()
