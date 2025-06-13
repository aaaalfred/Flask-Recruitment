# 🚀 GUÍA DE INSTALACIÓN Y CONFIGURACIÓN
# Sistema de Gestión de Vacantes y Candidatos

## 📋 Prerrequisitos
1. Python 3.8 o superior
2. MySQL Server ejecutándose
3. Git (opcional)

## 🔧 Pasos de Instalación

### 1. Verificar el entorno virtual
```bash
# Activar entorno virtual (ya debería estar activo)
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Verificar configuración
```bash
python check_config.py
```
Este script verificará:
- Variables de entorno en .env
- Dependencias instaladas
- Conexión a la base de datos

### 4. Inicializar migraciones de base de datos
```bash
flask db init
```

### 5. Crear migración inicial
```bash
flask db migrate -m "Initial migration"
```

### 6. Aplicar migraciones
```bash
flask db upgrade
```

### 7. Crear datos iniciales
```bash
python init_data.py
```
Esto creará usuarios de prueba:
- ejecutivo@empresa.com / ejecutivo123
- reclutador@empresa.com / reclutador123  
- lider@empresa.com / lider123

### 8. Ejecutar la aplicación
```bash
python app.py
```
La aplicación estará disponible en: http://localhost:5000

### 9. Probar la API
```bash
python test_api.py
```

## 🌐 Endpoints Principales

### Autenticación
- POST /api/auth/login - Iniciar sesión
- POST /api/auth/register - Registrar usuario

### Usuarios
- GET /api/usuarios - Listar usuarios
- POST /api/usuarios - Crear usuario
- GET /api/usuarios/{id} - Obtener usuario
- PUT /api/usuarios/{id} - Actualizar usuario
- DELETE /api/usuarios/{id} - Eliminar usuario

### Vacantes
- GET /api/vacantes - Listar vacantes
- POST /api/vacantes - Crear vacante
- GET /api/vacantes/{id} - Obtener vacante
- PUT /api/vacantes/{id} - Actualizar vacante
- DELETE /api/vacantes/{id} - Eliminar vacante

### Candidatos
- GET /api/candidatos - Listar candidatos
- POST /api/candidatos - Crear candidato
- GET /api/candidatos/{id} - Obtener candidato
- PUT /api/candidatos/{id} - Actualizar candidato
- DELETE /api/candidatos/{id} - Eliminar candidato

### Documentos
- POST /api/documentos/upload - Subir archivo
- GET /api/documentos/{id} - Obtener documento
- DELETE /api/documentos/{id} - Eliminar documento

### Entrevistas
- GET /api/entrevistas - Listar entrevistas
- POST /api/entrevistas - Crear entrevista
- GET /api/entrevistas/{id} - Obtener entrevista
- PUT /api/entrevistas/{id} - Actualizar entrevista
- DELETE /api/entrevistas/{id} - Eliminar entrevista

### Candidatos-Posiciones
- GET /api/candidatos-posiciones - Listar asignaciones
- POST /api/candidatos-posiciones - Asignar candidato a vacante
- PUT /api/candidatos-posiciones/{id} - Actualizar estado
- DELETE /api/candidatos-posiciones/{id} - Eliminar asignación

## 🔐 Autenticación
Todos los endpoints (excepto login/register) requieren:
```
Authorization: Bearer {token}
```

## 📝 Ejemplo de uso con curl

### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "ejecutivo@empresa.com", "password": "ejecutivo123"}'
```

### Crear candidato
```bash
curl -X POST http://localhost:5000/api/candidatos \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "nombre": "Juan Pérez",
    "email": "juan@email.com",
    "telefono": "+52 55 1234 5678",
    "experiencia_anos": 5,
    "salario_esperado": 50000.00,
    "ubicacion": "Ciudad de México",
    "disponibilidad": "inmediata",
    "nivel_ingles": "intermedio"
  }'
```

## 🗂️ Estructura del Proyecto
```
rh/
├── app.py                    # Aplicación principal
├── config.py                 # Configuración
├── requirements.txt          # Dependencias
├── .env                      # Variables de entorno
├── models/
│   └── __init__.py          # Modelos SQLAlchemy
├── routes/                   # Endpoints de la API
├── services/                 # Servicios (Auth, S3)
├── utils/                    # Utilidades
├── migrations/               # Migraciones de BD (generado)
├── check_config.py          # Verificación de configuración
├── init_data.py             # Datos iniciales
└── test_api.py              # Pruebas de API
```

## 🔧 Solución de Problemas

### Error de conexión a MySQL
1. Verificar que MySQL esté ejecutándose
2. Verificar credenciales en .env
3. Verificar que la base de datos exista
4. Probar conexión manual

### Error "AttributeError: Decimal"
- Ya corregido en el código (usar db.Numeric en lugar de db.Decimal)

### Error de importación de módulos
- Verificar que todos los archivos __init__.py existan
- Verificar la estructura de carpetas

### Error de Flask-Migrate
```bash
# Si hay problemas con migraciones, resetear:
rm -rf migrations/
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## 📊 Base de Datos
El sistema crea automáticamente las siguientes tablas:
- usuario
- vacante  
- candidato
- documento
- entrevista
- candidatos_posiciones

## 🔄 Comandos Útiles

### Crear nueva migración
```bash
flask db migrate -m "Descripción del cambio"
```

### Aplicar migraciones
```bash
flask db upgrade
```

### Retroceder migración
```bash
flask db downgrade
```

### Ver estado de migraciones
```bash
flask db show
```

## 🎯 Próximos Pasos
1. Configurar AWS S3 para subida de archivos
2. Agregar más validaciones
3. Implementar reportes
4. Agregar frontend
5. Configurar deployment en producción
