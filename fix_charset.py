#!/usr/bin/env python3
"""
Script para diagnosticar y corregir problemas de codificación UTF-8 en MySQL
"""
from app import create_app
from extensions import db
import sys

def check_mysql_charset():
    """Verificar la configuración de charset de MySQL"""
    print("🔍 Verificando configuración de charset de MySQL...")
    
    try:
        app = create_app()
        with app.app_context():
            # Verificar charset de la base de datos
            result = db.session.execute(db.text("SELECT @@character_set_database, @@collation_database")).fetchone()
            print(f"📊 Base de datos actual:")
            print(f"   Character set: {result[0]}")
            print(f"   Collation: {result[1]}")
            
            # Verificar charset del servidor
            result = db.session.execute(db.text("SELECT @@character_set_server, @@collation_server")).fetchone()
            print(f"🖥️  Servidor MySQL:")
            print(f"   Character set: {result[0]}")
            print(f"   Collation: {result[1]}")
            
            # Verificar charset de la conexión
            result = db.session.execute(db.text("SELECT @@character_set_connection, @@collation_connection")).fetchone()
            print(f"🔗 Conexión actual:")
            print(f"   Character set: {result[0]}")
            print(f"   Collation: {result[1]}")
            
            # Verificar charset de las tablas
            print(f"\n📋 Charset de las tablas:")
            tables_info = db.session.execute(db.text("""
                SELECT TABLE_NAME, TABLE_COLLATION 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_SCHEMA = DATABASE()
            """)).fetchall()
            
            for table_name, table_collation in tables_info:
                print(f"   • {table_name}: {table_collation}")
                
            return True
            
    except Exception as e:
        print(f"❌ Error verificando charset: {str(e)}")
        return False

def check_column_charset():
    """Verificar charset de las columnas específicas"""
    print("\n🔍 Verificando charset de columnas...")
    
    try:
        app = create_app()
        with app.app_context():
            # Verificar columnas de texto en la tabla vacante
            columns_info = db.session.execute(db.text("""
                SELECT COLUMN_NAME, CHARACTER_SET_NAME, COLLATION_NAME, COLUMN_TYPE
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = DATABASE() 
                AND TABLE_NAME = 'vacante'
                AND DATA_TYPE IN ('varchar', 'text', 'longtext', 'mediumtext', 'tinytext')
            """)).fetchall()
            
            print(f"📊 Columnas de texto en tabla 'vacante':")
            for col_name, charset, collation, col_type in columns_info:
                print(f"   • {col_name} ({col_type}): {charset or 'NULL'} / {collation or 'NULL'}")
                
            return True
            
    except Exception as e:
        print(f"❌ Error verificando columnas: {str(e)}")
        return False

def fix_database_charset():
    """Intentar corregir el charset de la base de datos"""
    print("\n🔧 Intentando corregir charset de la base de datos...")
    
    try:
        app = create_app()
        with app.app_context():
            # Obtener nombre de la base de datos
            db_name_result = db.session.execute(db.text("SELECT DATABASE()")).fetchone()
            db_name = db_name_result[0]
            
            print(f"📀 Base de datos: {db_name}")
            
            # Cambiar charset de la base de datos
            db.session.execute(db.text(f"ALTER DATABASE `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
            
            print("✅ Charset de la base de datos actualizado a utf8mb4")
            
            return True
            
    except Exception as e:
        print(f"❌ Error corrigiendo charset de DB: {str(e)}")
        return False

def fix_table_charset():
    """Corregir charset de las tablas"""
    print("\n🔧 Corrigiendo charset de las tablas...")
    
    try:
        app = create_app()
        with app.app_context():
            # Obtener todas las tablas
            tables = db.session.execute(db.text("""
                SELECT TABLE_NAME 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_SCHEMA = DATABASE()
            """)).fetchall()
            
            for (table_name,) in tables:
                try:
                    # Convertir cada tabla a utf8mb4
                    db.session.execute(db.text(f"ALTER TABLE `{table_name}` CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
                    print(f"   ✅ Tabla {table_name} convertida a utf8mb4")
                except Exception as e:
                    print(f"   ⚠️  Error en tabla {table_name}: {str(e)}")
            
            # Commit todos los cambios
            db.session.commit()
            print("✅ Conversión de tablas completada")
            
            return True
            
    except Exception as e:
        print(f"❌ Error corrigiendo tablas: {str(e)}")
        db.session.rollback()
        return False

def test_utf8_insert():
    """Probar inserción de caracteres especiales"""
    print("\n🧪 Probando inserción de caracteres especiales...")
    
    try:
        app = create_app()
        with app.app_context():
            # Crear una vacante de prueba con caracteres especiales
            from models import Vacante, Usuario
            
            # Buscar un usuario para asignar
            user = Usuario.query.first()
            if not user:
                print("❌ No hay usuarios disponibles para la prueba")
                return False
            
            # Texto con caracteres especiales
            test_text = "Prueba áéíóúñü 🚀 Descripción con acentos y emojis"
            
            # Crear vacante de prueba
            test_vacante = Vacante(
                nombre="Prueba UTF-8 áéíóú",
                descripcion=test_text,
                ejecutivo_id=user.id,
                reclutador_id=user.id,
                candidatos_requeridos=3,
                vacantes=1
            )
            
            db.session.add(test_vacante)
            db.session.commit()
            
            # Verificar que se guardó correctamente
            saved_vacante = Vacante.query.filter_by(nombre="Prueba UTF-8 áéíóú").first()
            if saved_vacante and saved_vacante.descripcion == test_text:
                print(f"✅ Inserción exitosa: {saved_vacante.descripcion[:50]}...")
                
                # Limpiar - eliminar la vacante de prueba
                db.session.delete(saved_vacante)
                db.session.commit()
                print("🗑️  Vacante de prueba eliminada")
                
                return True
            else:
                print("❌ Los datos no se guardaron correctamente")
                return False
                
    except Exception as e:
        print(f"❌ Error en prueba UTF-8: {str(e)}")
        db.session.rollback()
        return False

def main():
    print("=" * 70)
    print("🔤 DIAGNÓSTICO Y CORRECCIÓN DE CHARSET UTF-8")
    print("=" * 70)
    
    # Paso 1: Diagnóstico
    if not check_mysql_charset():
        print("❌ No se puede continuar sin conexión a MySQL")
        return
    
    check_column_charset()
    
    # Paso 2: Intentar corrección
    print("\n" + "=" * 50)
    print("🛠️  APLICANDO CORRECCIONES")
    print("=" * 50)
    
    success = True
    
    if not fix_database_charset():
        success = False
    
    if not fix_table_charset():
        success = False
    
    # Paso 3: Verificar corrección
    print("\n" + "=" * 50)
    print("🧪 VERIFICANDO CORRECCIONES")
    print("=" * 50)
    
    print("\n🔍 Configuración después de las correcciones:")
    check_mysql_charset()
    check_column_charset()
    
    # Paso 4: Probar funcionamiento
    if test_utf8_insert():
        print("\n✅ ¡CORRECCIÓN EXITOSA!")
        print("🎉 Los caracteres especiales ahora funcionan correctamente")
    else:
        print("\n⚠️  Aún hay problemas con UTF-8")
        success = False
    
    print("\n" + "=" * 70)
    if success:
        print("✅ PROBLEMA RESUELTO")
        print("\n💡 Recomendaciones adicionales:")
        print("   1. Reinicia tu aplicación Flask")
        print("   2. Prueba crear una vacante con acentos")
        print("   3. Verifica que el frontend también maneje UTF-8")
    else:
        print("❌ CORRECCIÓN PARCIAL O FALLIDA")
        print("\n🔧 Soluciones alternativas:")
        print("   1. Verificar permisos de MySQL")
        print("   2. Consultar al administrador de la base de datos")
        print("   3. Considerar crear una nueva base de datos con UTF-8")
    
    print("=" * 70)

if __name__ == '__main__':
    main()
