# 👥 GESTIÓN DE USUARIOS - DOCUMENTACIÓN COMPLETA

## 🎯 RESUMEN
Sistema completo de gestión de usuarios implementado en el sistema de reclutamiento. Permite crear, editar, desactivar y gestionar usuarios con diferentes roles y permisos.

---

## 🚀 CONFIGURACIÓN INICIAL

### ✅ Password Corregido
```
Email: admin@empresa.com
Password: password123  ← CORREGIDO
Rol: ejecutivo
```

### 🔧 Scripts de Configuración
- `fix_admin_password.py` - Corrige el password del admin
- `setup_users.py` - Script completo de inicialización
- `test_user_management.py` - Testing completo del sistema

---

## 🏗️ ARQUITECTURA

### 📂 Backend (Flask)
```
routes/usuario_routes.py    - Endpoints de usuarios
models/__init__.py          - Modelo Usuario
services/auth_service.py    - Autenticación y permisos
```

### 🎨 Frontend (React)
```
pages/Users.js             - Componente principal
styles/users.css           - Estilos específicos
App.js                     - Rutas configuradas
```

---

## 🔑 ROLES Y PERMISOS

### 👨‍💼 EJECUTIVO
- ✅ Crear/editar/desactivar usuarios
- ✅ Crear vacantes
- ✅ Ver todos los reportes
- ✅ Acceso completo al sistema

### 👩‍💼 RECLUTADOR LÍDER
- ✅ Crear/editar/desactivar usuarios
- ✅ Supervisar reclutadores
- ✅ Ver todas las vacantes
- ✅ Generar reportes

### 👨‍💻 RECLUTADOR
- ✅ Gestionar candidatos asignados
- ✅ Programar entrevistas
- ✅ Ver solo vacantes asignadas
- ❌ No puede gestionar usuarios
- ❌ No puede crear vacantes

---

## 🛠️ FUNCIONALIDADES IMPLEMENTADAS

### ✅ CRUD Completo
- **Crear usuario**: Formulario con validaciones
- **Listar usuarios**: Paginación y filtros
- **Editar usuario**: Modal con campos pre-poblados
- **Desactivar**: Soft delete (mantiene datos)

### 🔍 Filtros y Búsqueda
- **Búsqueda**: Por nombre o email
- **Filtro por rol**: Todos/Ejecutivo/Reclutador/Líder
- **Estadísticas**: Total y usuarios activos

### 🎨 UI/UX Optimizada
- **Responsive**: Funciona en móvil y desktop
- **Iconos por rol**: Visual diferenciado
- **Estados visuales**: Activo/inactivo
- **Animaciones**: Transiciones suaves
- **Modal elegante**: Para crear/editar

---

## 📡 API ENDPOINTS

### 🔐 Autenticación
```
POST /api/auth/login
{
  "email": "admin@empresa.com",
  "password": "password123"
}
```

### 👥 Gestión de Usuarios
```
GET    /api/usuarios              - Listar usuarios
POST   /api/usuarios              - Crear usuario
GET    /api/usuarios/{id}         - Obtener usuario
PUT    /api/usuarios/{id}         - Actualizar usuario
DELETE /api/usuarios/{id}         - Desactivar usuario
```

### 📋 Ejemplo de Crear Usuario
```json
POST /api/usuarios
{
  "nombre": "María González",
  "email": "maria@empresa.com",
  "password": "demo123",
  "rol": "reclutador"
}
```

---

## 🧪 TESTING

### 🔧 Scripts de Prueba
```bash
# Corregir password del admin
python fix_admin_password.py

# Testing completo
python test_user_management.py

# Configuración completa
python setup_users.py --full
```

### 🧪 Casos de Prueba
- ✅ Login con credenciales correctas
- ✅ Crear usuario con datos válidos
- ✅ Editar usuario existente
- ✅ Desactivar usuario
- ✅ Validación de email único
- ✅ Control de permisos por rol

---

## 🚀 INSTRUCCIONES DE USO

### 1. 🔧 Iniciar Backend
```bash
cd C:\Users\ADMIN\code\rh
python setup_users.py --backend
```

### 2. 🎨 Iniciar Frontend
```bash
cd C:\Users\ADMIN\code\rh
python setup_users.py --frontend
```

### 3. 🌐 Acceder al Sistema
```
URL: http://localhost:3000/login
Email: admin@empresa.com
Password: password123
```

### 4. 👥 Gestión de Usuarios
```
URL: http://localhost:3000/users
- Crear nuevo usuario
- Buscar y filtrar
- Editar usuarios existentes
- Desactivar usuarios
```

---

## 📊 CARACTERÍSTICAS TÉCNICAS

### 🔒 Seguridad
- **JWT Authentication**: Tokens seguros
- **Password Hashing**: bcrypt para passwords
- **Role-based Access**: Control por roles
- **Input Validation**: Validación en frontend y backend

### 🎨 Frontend
- **React 18**: Hooks y componentes funcionales
- **Tailwind CSS**: Diseño responsive
- **HeroIcons**: Iconografía consistente
- **React Hot Toast**: Notificaciones elegantes

### 🔧 Backend
- **Flask**: Framework web Python
- **SQLAlchemy**: ORM para base de datos
- **MySQL**: Base de datos relacional
- **JWT Extended**: Manejo de tokens

---

## 🐛 TROUBLESHOOTING

### ❌ Error: Password incorrecto
```bash
# Ejecutar para corregir
python fix_admin_password.py
```

### ❌ Error: No se puede conectar backend
```bash
# Verificar que esté corriendo
cd C:\Users\ADMIN\code\rh
python app.py
```

### ❌ Error: Frontend no carga
```bash
# Reinstalar dependencias
cd frontend
npm install
npm start
```

### ❌ Error: Base de datos
```bash
# Verificar conexión MySQL
python test_connection.py
```

---

## 📈 PRÓXIMAS MEJORAS

### 🔮 Funcionalidades Futuras
- **Foto de perfil**: Upload de avatares
- **Historial de cambios**: Auditoría de modificaciones
- **Notificaciones**: Alertas por email
- **Roles personalizados**: Permisos granulares
- **Importar usuarios**: Desde CSV/Excel

### 🎨 UI/UX Mejoras
- **Tema oscuro**: Toggle de modo oscuro
- **Bulk actions**: Operaciones masivas
- **Advanced filters**: Filtros más específicos
- **User activity**: Última conexión, estadísticas

---

## 💡 NOTAS IMPORTANTES

### ⚠️ Seguridad
- Cambiar passwords por defecto en producción
- Configurar HTTPS en producción
- Revisar permisos regularmente
- Backup de base de datos

### 🔧 Mantenimiento
- Revisar logs de aplicación
- Monitorear performance de base de datos
- Actualizar dependencias regularmente
- Testing antes de deployments

---

## 📞 SOPORTE

### 🛠️ Para resolver problemas:
1. Ejecutar `python setup_users.py --test`
2. Revisar logs de Flask y React
3. Verificar conexión a MySQL
4. Validar variables de entorno

### 📋 Archivos de configuración:
- `.env` - Variables de entorno
- `config.py` - Configuración de Flask
- `frontend/package.json` - Dependencias React

---

## ✅ CHECKLIST DE VERIFICACIÓN

### 🔍 Antes de usar:
- [ ] MySQL está corriendo
- [ ] Variables de entorno configuradas
- [ ] Password del admin corregido
- [ ] Backend corriendo en localhost:5000
- [ ] Frontend corriendo en localhost:3000
- [ ] Login funciona con admin@empresa.com / password123

### 🎯 Funcionalidades verificadas:
- [ ] Crear usuario nuevo
- [ ] Editar usuario existente
- [ ] Desactivar usuario
- [ ] Filtros y búsqueda
- [ ] Permisos por rol
- [ ] Responsive design

---

**🎉 ¡SISTEMA DE GESTIÓN DE USUARIOS LISTO PARA USAR!**
