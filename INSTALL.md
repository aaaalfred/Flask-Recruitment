# 🚀 Guía de Instalación Rápida - Sistema RH

## Requisitos Previos
- Python 3.8 o superior
- MySQL 5.7 o superior
- Cuenta AWS (opcional, para S3)
- Git

## 🔧 Instalación Local

### 1. Clonar el repositorio
```bash
git clone <tu-repositorio>
cd rh
```

### 2. Crear entorno virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar base de datos MySQL
```sql
CREATE DATABASE recruitment_system;
CREATE USER 'rh_user'@'localhost' IDENTIFIED BY 'rh_password';
GRANT ALL PRIVILEGES ON recruitment_system.* TO 'rh_user'@'localhost';
FLUSH PRIVILEGES;
```

### 5. Configurar variables de entorno
```bash
# Copiar template
copy .env.template .env

# Editar .env con tus credenciales
MYSQL_HOST=localhost
MYSQL_USER=rh_user
MYSQL_PASSWORD=rh_password
MYSQL_DB=recruitment_system

# Opcional: AWS S3
AWS_ACCESS_KEY_ID=tu_access_key
AWS_SECRET_ACCESS_KEY=tu_secret_key
AWS_S3_BUCKET=tu-bucket-name
AWS_S3_REGION=us-east-1

# Claves secretas (generar nuevas para producción)
SECRET_KEY=tu-clave-secreta-aqui
JWT_SECRET_KEY=tu-jwt-secreto-aqui
```

### 6. Crear datos iniciales
```bash
python create_initial_data.py
```

### 7. Ejecutar aplicación
```bash
python app.py
```

La aplicación estará disponible en: http://localhost:5000

## 🐳 Instalación con Docker

### 1. Usando Docker Compose
```bash
# Construir y ejecutar
docker-compose up --build

# En background
docker-compose up -d --build
```

### 2. Crear datos iniciales (Docker)
```bash
docker-compose exec app python create_initial_data.py
```

## 🧪 Probar la instalación

```bash
# Ejecutar tests de API
python test_api.py
```

## 📝 Credenciales por defecto

- **Administrador**: admin@empresa.com / admin123
- **Reclutador**: reclutador@empresa.com / reclutador123  
- **Líder**: lider@empresa.com / lider123

## 🔗 Endpoints principales

- API Base: http://localhost:5000/api
- Login: POST /api/auth/login
- Documentación completa en README.md

## ⚠️ Problemas comunes

### Error de conexión MySQL
- Verificar que MySQL esté ejecutándose
- Comprobar credenciales en .env
- Verificar que la base de datos existe

### Error de importación de módulos
- Asegurar que el entorno virtual está activo
- Reinstalar dependencias: `pip install -r requirements.txt`

### Error de permisos en archivos
- En Linux/Mac: `chmod +x *.py`

## 🛠️ Comandos útiles

```bash
# Activar entorno virtual
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar nueva dependencia
pip install nueva-dependencia
pip freeze > requirements.txt

# Backup de base de datos
mysqldump -u rh_user -p recruitment_system > backup.sql

# Restaurar backup
mysql -u rh_user -p recruitment_system < backup.sql
```

## 📚 Próximos pasos

1. Cambiar credenciales por defecto
2. Configurar AWS S3 para archivos
3. Revisar documentación completa en README.md
4. Personalizar según necesidades de tu organización

## 🆘 Soporte

Si encuentras problemas:
1. Revisar logs de la aplicación
2. Verificar configuración de .env
3. Consultar README.md para documentación completa
