@echo off
echo 🚀 Instalando Sistema de Gestión de RH - Frontend y Backend
echo ===========================================================

REM Verificar que estamos en el directorio correcto
if not exist "app.py" (
    echo ❌ Error: Ejecuta este script desde la carpeta raíz del proyecto (donde está app.py^)
    pause
    exit /b 1
)

echo 📦 Instalando dependencias del backend...
REM Activar entorno virtual si existe
if exist "venv" (
    echo 🔄 Activando entorno virtual...
    call venv\Scripts\activate
) else (
    echo ⚠️  No se encontró entorno virtual. Creando uno nuevo...
    python -m venv venv
    call venv\Scripts\activate
)

REM Instalar dependencias de Python
pip install -r requirements.txt

echo 📦 Instalando dependencias del frontend...
cd frontend

REM Verificar que Node.js esté instalado
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Node.js no está instalado.
    echo 👉 Por favor instala Node.js desde https://nodejs.org/
    echo 👉 Luego ejecuta: cd frontend ^&^& npm install ^&^& npm start
    pause
    exit /b 1
)

REM Instalar dependencias de Node.js
npm install

echo ✅ ¡Instalación completada!
echo.
echo 🚀 Para iniciar el sistema:
echo 1. Backend (desde la carpeta raíz^):
echo    python app.py
echo.
echo 2. Frontend (desde la carpeta frontend^):
echo    cd frontend
echo    npm start
echo.
echo 🌐 URLs:
echo - Frontend: http://localhost:3000
echo - Backend API: http://localhost:5000/api
echo.
echo 🔐 Credenciales de prueba:
echo - Ejecutivo: admin@empresa.com / admin123
echo - Reclutador: reclutador@empresa.com / reclutador123
echo.
echo 📚 Para más información:
echo - Backend: README.md
echo - Frontend: frontend/README.md
pause
