# 🚀 Instrucciones de Instalación del Frontend

## Paso 1: Instalar Node.js

Si no tienes Node.js instalado:

1. Ve a https://nodejs.org/
2. Descarga la versión LTS (recomendada)
3. Instala siguiendo las instrucciones
4. Verifica la instalación:
   ```bash
   node --version
   npm --version
   ```

## Paso 2: Instalar Dependencias

Desde la carpeta `frontend`:

```bash
cd frontend
npm install
```

Este comando instalará todas las dependencias necesarias:
- React y React DOM
- React Router para navegación
- Tailwind CSS para estilos
- Axios para comunicación con el backend
- Y muchas más...

## Paso 3: Configurar Variables de Entorno

El archivo `.env` ya está configurado para desarrollo local. Si necesitas cambiar la URL del backend, edita:

```env
REACT_APP_API_URL=http://localhost:5000/api
```

## Paso 4: Iniciar el Frontend

```bash
npm start
```

Esto iniciará el servidor de desarrollo de React en `http://localhost:3000`

## Paso 5: Verificar Conexión con Backend

1. Asegúrate de que el backend Flask esté corriendo en `http://localhost:5000`
2. Ve a `http://localhost:3000`
3. Deberías ver la página de login
4. Usa las credenciales de prueba:
   - **Ejecutivo**: admin@empresa.com / admin123
   - **Reclutador**: reclutador@empresa.com / reclutador123

## 🎯 ¡Listo!

Tu frontend ya está funcionando y conectado al backend. Puedes:

- ✅ Hacer login con las credenciales de prueba
- ✅ Ver el dashboard con métricas
- ✅ Navegar por las diferentes secciones
- ✅ Ver la lista de vacantes y candidatos
- ✅ Usar todos los filtros y búsquedas

## 🔧 Comandos Útiles

```bash
# Instalar dependencias
npm install

# Iniciar desarrollo
npm start

# Construir para producción
npm run build

# Ejecutar tests
npm test
```

## 🐛 Solución de Problemas

### Si npm install falla:
```bash
# Limpiar cache de npm
npm cache clean --force

# Borrar node_modules y reinstalar
rm -rf node_modules package-lock.json
npm install
```

### Si el frontend no se conecta al backend:
1. Verifica que Flask esté corriendo en puerto 5000
2. Revisa que no haya errores de CORS
3. Comprueba la URL en el archivo `.env`

### Si Tailwind CSS no funciona:
```bash
# Reinstalar dependencias de Tailwind
npm install tailwindcss autoprefixer postcss
```

¡Disfruta usando tu nuevo sistema de RH! 🎉
