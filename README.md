# Sistema de Gestión de Vacantes y Candidatos

## Descripción
Sistema completo para la gestión de procesos de reclutamiento, desarrollado con Flask, SQLAlchemy, MySQL y AWS S3.

## Características principales
- CRUD completo para todas las entidades
- Gestión de roles y permisos
- Subida de archivos a AWS S3
- Relaciones muchos-a-muchos entre candidatos y vacantes
- API RESTful documentada
- Autenticación JWT

## Tecnologías utilizadas
- **Backend**: Flask (Python)
- **Base de datos**: MySQL
- **ORM**: SQLAlchemy
- **Almacenamiento**: AWS S3
- **Autenticación**: JWT + Flask-Login
- **Migraciones**: Flask-Migrate

## Instalación

1. Clonar el repositorio
2. Crear entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configurar variables de entorno:
   - Copiar `.env.template` a `.env`
   - Completar con tus credenciales

5. Inicializar base de datos:
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. Ejecutar aplicación:
   ```bash
   python app.py
   ```

## Estructura del proyecto
```
/rh
  /models/          # Modelos de SQLAlchemy
  /routes/          # Blueprints con endpoints
  /services/        # Servicios (S3, Auth)
  /utils/           # Utilidades
  config.py         # Configuración
  app.py           # Aplicación principal
requirements.txt
README.md
.env.template
```

## Endpoints principales

### Autenticación
- `POST /api/auth/login` - Iniciar sesión
- `POST /api/auth/register` - Registrar usuario

### Usuarios
- `GET /api/usuarios` - Listar usuarios
- `POST /api/usuarios` - Crear usuario
- `GET /api/usuarios/<id>` - Obtener usuario
- `PUT /api/usuarios/<id>` - Actualizar usuario
- `DELETE /api/usuarios/<id>` - Eliminar usuario

### Vacantes
- `GET /api/vacantes` - Listar vacantes
- `POST /api/vacantes` - Crear vacante
- `GET /api/vacantes/<id>` - Obtener vacante
- `PUT /api/vacantes/<id>` - Actualizar vacante
- `DELETE /api/vacantes/<id>` - Eliminar vacante

### Candidatos
- `GET /api/candidatos` - Listar candidatos
- `POST /api/candidatos` - Crear candidato
- `GET /api/candidatos/<id>` - Obtener candidato
- `PUT /api/candidatos/<id>` - Actualizar candidato
- `DELETE /api/candidatos/<id>` - Eliminar candidato

### Documentos
- `POST /api/documentos/upload` - Subir archivo
- `GET /api/documentos/<id>` - Obtener documento
- `DELETE /api/documentos/<id>` - Eliminar documento

### Entrevistas
- `GET /api/entrevistas` - Listar entrevistas
- `POST /api/entrevistas` - Crear entrevista
- `GET /api/entrevistas/<id>` - Obtener entrevista
- `PUT /api/entrevistas/<id>` - Actualizar entrevista
- `DELETE /api/entrevistas/<id>` - Eliminar entrevista

### Candidatos-Posiciones
- `GET /api/candidatos-posiciones` - Listar asignaciones
- `POST /api/candidatos-posiciones` - Asignar candidato a vacante
- `PUT /api/candidatos-posiciones/<id>` - Actualizar estado
- `DELETE /api/candidatos-posiciones/<id>` - Eliminar asignación

## Roles de usuario
- **Ejecutivo**: Puede crear vacantes y ver reportes
- **Reclutador**: Gestiona candidatos y entrevistas
- **Reclutador Líder**: Supervisión general

## Base de datos
El sistema utiliza las siguientes tablas:
- usuarios
- vacantes
- candidatos
- documentos
- entrevistas
- candidatos_posiciones (tabla intermedia)

## Configuración de desarrollo

### Base de datos local
1. Instalar MySQL
2. Crear base de datos: `CREATE DATABASE recruitment_system;`
3. Configurar credenciales en `.env`

### AWS S3
1. Crear bucket en AWS S3
2. Configurar IAM con permisos S3
3. Agregar credenciales AWS en `.env`

## Comandos útiles

```bash
# Crear migración
flask db migrate -m "Descripción del cambio"

# Aplicar migraciones
flask db upgrade

# Ejecutar en modo desarrollo
python app.py

# Instalar dependencias
pip install -r requirements.txt
```

## Estructura de archivos

```
rh/
├── app.py                              # Aplicación principal
├── config.py                           # Configuración
├── requirements.txt                    # Dependencias
├── .env.template                       # Template variables entorno
├── README.md                          # Documentación
├── models/
│   └── __init__.py                    # Modelos SQLAlchemy
├── routes/
│   ├── auth_routes.py                 # Autenticación
│   ├── usuario_routes.py              # CRUD usuarios
│   ├── vacante_routes.py              # CRUD vacantes
│   ├── candidato_routes.py            # CRUD candidatos
│   ├── documento_routes.py            # Gestión archivos
│   ├── entrevista_routes.py           # CRUD entrevistas
│   └── candidatos_posiciones_routes.py # Relaciones N:M
├── services/
│   ├── s3_service.py                  # Servicio AWS S3
│   └── auth_service.py                # Autenticación JWT
└── utils/
    └── file_utils.py                  # Utilidades archivos
```
