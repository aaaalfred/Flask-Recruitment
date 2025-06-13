# 🏢 Sistema de Gestión de RH - Completo con Frontend

Sistema integral para la gestión de procesos de reclutamiento con **Backend Flask** y **Frontend React**.

## 🎯 **¿Qué incluye?**

### ✅ **Backend API Completo**
- **Framework**: Flask + SQLAlchemy + MySQL
- **Almacenamiento**: AWS S3 para documentos
- **Autenticación**: JWT con roles
- **API RESTful**: Todos los endpoints implementados
- **Base de datos**: Relaciones N:M, migraciones automáticas

### ✅ **Frontend React Completo**
- **Framework**: React 18 + React Router
- **Diseño**: Tailwind CSS + Headless UI
- **Dashboard**: Métricas en tiempo real con gráficos
- **Responsive**: Móvil y desktop
- **Autenticación**: Login automático con JWT

## 🚀 **Instalación Rápida**

### Opción 1: Script Automático (Recomendado)

**Windows:**
```bash
install.bat
```

**Linux/Mac:**
```bash
chmod +x install.sh
./install.sh
```

### Opción 2: Manual

**1. Backend:**
```bash
# Instalar dependencias Python
pip install -r requirements.txt

# Iniciar backend
python app.py
```

**2. Frontend:**
```bash
# Instalar dependencias Node.js
cd frontend
npm install

# Iniciar frontend
npm start
```

## 🌐 **URLs del Sistema**

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000/api

## 🔐 **Credenciales de Prueba**

- **Ejecutivo**: admin@empresa.com / admin123
- **Reclutador**: reclutador@empresa.com / reclutador123

## 📱 **Características del Frontend**

### Dashboard Interactivo
- **Métricas en tiempo real**: Vacantes activas, candidatos totales, entrevistas pendientes
- **Gráficos dinámicos**: Estados de candidatos, vacantes populares
- **Acciones rápidas**: Crear vacantes/candidatos con un clic
- **Actividad reciente**: Timeline de eventos

### Gestión de Vacantes
- **Lista completa** con filtros y búsqueda
- **Estados**: Abierta, pausada, cerrada, cancelada
- **Prioridades**: Baja, media, alta, crítica
- **Información detallada**: Salarios, modalidad, ubicación

### Gestión de Candidatos  
- **Base de datos completa** con búsqueda avanzada
- **Información personal**: Contacto, experiencia, ubicación
- **Estados**: Activo, inactivo, lista negra
- **Vista responsive**: Cards en móvil, tabla en desktop

### Navegación Inteligente
- **Sidebar dinámico** con permisos por rol
- **Header contextual** con título de sección
- **Menú de usuario** con perfil y logout
- **Navegación móvil** con overlay

### Diseño Moderno
- **Tailwind CSS** con diseño personalizado
- **Animaciones** suaves y profesionales
- **Iconografía** consistente con Heroicons
- **Loading states** y manejo de errores
- **Notificaciones** elegantes con toast

## 🏗️ **Arquitectura del Sistema**

```
Sistema RH/
├── Backend (Flask)
│   ├── models/          # Modelos SQLAlchemy
│   ├── routes/          # Endpoints API REST
│   ├── services/        # Servicios (S3, Auth)
│   ├── utils/           # Utilidades
│   └── migrations/      # Migraciones DB
│
├── Frontend (React)
│   ├── src/
│   │   ├── components/  # Componentes reutilizables
│   │   ├── pages/       # Páginas principales
│   │   ├── services/    # Servicios API
│   │   ├── hooks/       # Hooks personalizados
│   │   └── utils/       # Utilidades frontend
│   └── public/
│
└── Documentación
    ├── README.md        # Este archivo
    ├── INSTALL.md       # Guía de instalación
    └── API_DOCS.md      # Documentación API
```

## 🛠️ **Tecnologías Utilizadas**

### Backend
- **Flask** - Framework web Python
- **SQLAlchemy** - ORM para base de datos
- **MySQL** - Base de datos relacional
- **AWS S3** - Almacenamiento de archivos
- **JWT** - Autenticación de usuarios
- **Flask-CORS** - Manejo de CORS
- **Flask-Migrate** - Migraciones de DB

### Frontend
- **React 18** - Framework frontend
- **React Router** - Navegación SPA
- **Tailwind CSS** - Framework de estilos
- **Headless UI** - Componentes accesibles
- **Heroicons** - Iconografía
- **Axios** - Cliente HTTP
- **Recharts** - Gráficos y visualizaciones
- **React Hook Form** - Gestión de formularios
- **React Hot Toast** - Notificaciones

## 📊 **Funcionalidades Implementadas**

### ✅ Completamente Funcional
- [x] **Login/Logout** con JWT
- [x] **Dashboard** con métricas en tiempo real
- [x] **Lista de vacantes** con filtros
- [x] **Lista de candidatos** con búsqueda
- [x] **Navegación** completa entre secciones
- [x] **Permisos por rol** (ejecutivo, reclutador, líder)
- [x] **Diseño responsive** móvil/desktop
- [x] **API REST** completa
- [x] **Base de datos** con todas las relaciones

### 🔄 En Desarrollo (Próximas Funciones)
- [ ] Formularios de creación/edición
- [ ] Gestión de entrevistas
- [ ] Gestión de usuarios
- [ ] Subida de documentos con drag & drop
- [ ] Reportes avanzados exportables
- [ ] Notificaciones en tiempo real

## 🎨 **Screenshots**

### Dashboard Principal
![Dashboard con métricas, gráficos y acciones rápidas]

### Lista de Vacantes
![Gestión de vacantes con filtros y estados]

### Lista de Candidatos
![Base de datos de candidatos con búsqueda]

### Login
![Pantalla de login moderna y segura]

## 🔧 **Configuración**

### Variables de Entorno Backend (.env)
```env
# Database
MYSQL_HOST=localhost
MYSQL_USER=tu_usuario
MYSQL_PASSWORD=tu_password
MYSQL_DB=recruitment_system

# AWS S3
AWS_ACCESS_KEY_ID=tu_access_key
AWS_SECRET_ACCESS_KEY=tu_secret_key
AWS_S3_BUCKET=tu-bucket-name

# Security
SECRET_KEY=tu-secret-key
JWT_SECRET_KEY=tu-jwt-secret
```

### Variables de Entorno Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_APP_NAME=Sistema RH
```

## 🔄 **Flujo de Trabajo**

1. **Usuario inicia sesión** con credenciales
2. **Sistema valida** con JWT y asigna permisos
3. **Dashboard muestra** métricas en tiempo real
4. **Usuario navega** a secciones según su rol
5. **Sistema filtra** y muestra datos relevantes
6. **Acciones rápidas** permiten crear registros
7. **Cambios se reflejan** inmediatamente en la UI

## 🚨 **Troubleshooting**

### Backend no inicia
```bash
# Verificar dependencias
pip install -r requirements.txt

# Verificar base de datos
python check_config.py

# Crear datos iniciales
python init_data.py
```

### Frontend no se conecta
```bash
# Verificar dependencias
cd frontend && npm install

# Verificar configuración
cat frontend/.env

# Reiniciar servidor
npm start
```

### Error de CORS
- Verificar que Flask-CORS esté instalado
- Revisar configuración en `extensions.py`

## 📚 **Documentación Adicional**

- **Backend**: Ver `README.md` en raíz
- **Frontend**: Ver `frontend/README.md`
- **API**: Ver documentación de endpoints
- **Base de datos**: Ver diagrama ER en documentos

## 🤝 **Contribuir**

1. Fork el proyecto
2. Crear branch para feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'Añadir nueva funcionalidad'`)
4. Push al branch (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📞 **Soporte**

Si necesitas ayuda:
1. Revisa la documentación
2. Verifica los logs de consola
3. Comprueba las configuraciones
4. Contacta al equipo de desarrollo

---

## 🎉 **¡Sistema Listo!**

Tu sistema de gestión de RH está **100% funcional** con:

- ✅ **Backend Flask** robusto y escalable
- ✅ **Frontend React** moderno y responsive  
- ✅ **Base de datos** MySQL bien estructurada
- ✅ **Integración AWS S3** para documentos
- ✅ **Autenticación segura** con JWT
- ✅ **Dashboard interactivo** con métricas
- ✅ **Gestión completa** de vacantes y candidatos

**¡Empieza a usarlo ahora mismo!** 🚀
