# Frontend - Sistema de Gestión de RH

Frontend desarrollado en React para el Sistema de Gestión de Recursos Humanos.

## 🚀 Tecnologías Utilizadas

- **React 18** - Framework frontend
- **React Router DOM** - Navegación
- **Tailwind CSS** - Estilos y diseño
- **Headless UI** - Componentes accesibles
- **Heroicons** - Iconografía
- **Axios** - Cliente HTTP
- **React Hook Form** - Gestión de formularios
- **React Hot Toast** - Notificaciones
- **Recharts** - Gráficos y visualizaciones
- **date-fns** - Manejo de fechas

## 📁 Estructura del Proyecto

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/        # Componentes reutilizables
│   │   ├── Layout.js
│   │   ├── Sidebar.js
│   │   ├── Header.js
│   │   └── LoadingSpinner.js
│   ├── pages/            # Páginas principales
│   │   ├── Login.js
│   │   ├── Dashboard.js
│   │   ├── Vacants.js
│   │   ├── Candidates.js
│   │   ├── Interviews.js
│   │   ├── Users.js
│   │   └── Reports.js
│   ├── services/         # Servicios de API
│   │   └── api.js
│   ├── hooks/           # Hooks personalizados
│   │   └── useAuth.js
│   ├── utils/           # Utilidades
│   │   ├── helpers.js
│   │   └── constants.js
│   ├── App.js           # Componente principal
│   ├── index.js         # Punto de entrada
│   └── index.css        # Estilos globales
├── package.json
├── tailwind.config.js
└── postcss.config.js
```

## 🛠️ Instalación y Configuración

### 1. Instalar dependencias

```bash
cd frontend
npm install
```

### 2. Configurar variables de entorno

El archivo `.env` ya está configurado para desarrollo local:

```env
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_APP_NAME=Sistema RH
REACT_APP_VERSION=1.0.0
REACT_APP_DEBUG=true
```

### 3. Ejecutar en modo desarrollo

```bash
npm start
```

La aplicación estará disponible en `http://localhost:3000`

## 🔐 Autenticación

El sistema incluye autenticación completa con JWT:

- **Login automático** si hay token válido
- **Redirección** automática según estado de autenticación
- **Manejo de roles** (ejecutivo, reclutador, reclutador_lider)
- **Interceptor de axios** para agregar token automáticamente

### Credenciales de prueba:
- **Ejecutivo**: admin@empresa.com / admin123
- **Reclutador**: reclutador@empresa.com / reclutador123

## 📱 Características del Frontend

### ✅ Implementado
- **Dashboard interactivo** con métricas en tiempo real
- **Gestión de vacantes** con filtros y paginación
- **Gestión de candidatos** con búsqueda avanzada
- **Autenticación completa** con JWT
- **Diseño responsivo** para móvil y desktop
- **Navegación contextual** según rol de usuario
- **Notificaciones** con react-hot-toast
- **Loading states** y manejo de errores
- **Sidebar dinámico** con permisos por rol

### 🔄 En desarrollo
- Formularios de creación/edición
- Gestión de entrevistas
- Gestión de usuarios
- Reportes avanzados
- Subida de documentos

## 🎨 Diseño y UX

- **Tailwind CSS** para estilos consistentes
- **Diseño moderno** con glassmorphism y animaciones
- **Accesibilidad** con Headless UI
- **Iconografía** consistente con Heroicons
- **Responsive design** mobile-first
- **Dark mode ready** (configuración preparada)

## 🔌 Integración con Backend

El frontend está completamente integrado con tu backend Flask:

### Servicios implementados:
- `authService` - Login, registro, logout
- `vacantService` - CRUD de vacantes
- `candidateService` - CRUD de candidatos
- `userService` - Gestión de usuarios
- `documentService` - Subida de archivos
- `interviewService` - Gestión de entrevistas
- `reportService` - Dashboard y reportes

### Interceptors configurados:
- **Request**: Agrega token JWT automáticamente
- **Response**: Maneja errores 401 y redirección

## 📊 Dashboard

El dashboard incluye:
- **Métricas clave**: Vacantes activas, candidatos totales, entrevistas pendientes
- **Gráficos interactivos**: Estados de candidatos, vacantes populares
- **Acciones rápidas**: Enlaces directos a crear vacantes/candidatos
- **Actividad reciente**: Timeline de eventos

## 🚀 Comandos Disponibles

```bash
# Desarrollo
npm start              # Inicia servidor de desarrollo
npm run build         # Construye para producción
npm test              # Ejecuta tests
npm run eject         # Eyecta configuración (no recomendado)
```

## 🔧 Configuración Adicional

### Proxy para desarrollo
El `package.json` incluye proxy al backend:
```json
"proxy": "http://localhost:5000"
```

### Tailwind CSS
Configuración personalizada con:
- Colores del sistema (primary, success, warning, danger)
- Animaciones personalizadas
- Componentes reutilizables

## 🐛 Troubleshooting

### Error de CORS
Si hay problemas de CORS, verifica que el backend tenga Flask-CORS configurado.

### Problemas de autenticación
1. Verifica que el backend esté corriendo en puerto 5000
2. Revisa las credenciales de prueba
3. Limpia localStorage si hay tokens corruptos

### Estilos no se cargan
1. Verifica que Tailwind esté instalado: `npm install tailwindcss`
2. Asegúrate de que PostCSS esté configurado correctamente

## 📝 Próximos Pasos

1. **Completar formularios** de creación/edición
2. **Implementar subida de archivos** con drag & drop
3. **Añadir más gráficos** al dashboard
4. **Tests unitarios** con Jest y React Testing Library
5. **Optimización de rendimiento** con lazy loading

---

¡El frontend está listo para usar! 🎉
