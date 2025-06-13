@echo off
echo 🧹 Limpiando repositorio Git...
echo ================================

REM Hacer unstage de todos los archivos nuevos
echo 📂 Removiendo archivos del staging area...
git reset

REM Mostrar estado actual (solo las primeras 20 líneas)
echo 📊 Estado actual del repositorio:
git status --porcelain | findstr /V "node_modules" | findstr /V "__pycache__" | findstr /V ".log"

echo.
echo ✅ Limpieza completada!
echo.
echo 📋 Para añadir solo los archivos importantes:
echo git add .
echo git commit -m "Add frontend and complete RH system"
echo.
echo 🔍 Archivos que serán ignorados:
echo - frontend/node_modules/ (dependencias Node.js)
echo - venv/ (entorno virtual Python)
echo - .env (variables de entorno)
echo - __pycache__/ (archivos Python compilados)
echo - *.log (archivos de log)
echo.
pause
