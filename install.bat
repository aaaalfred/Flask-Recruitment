@echo off
echo 🔧 INSTALANDO DEPENDENCIAS DEL SISTEMA RH
echo =======================================

echo.
echo 📦 Instalando dependencias de Python...
pip install -r requirements.txt

echo.
echo 📦 Instalando dependencias del Frontend...
cd frontend
npm install
cd ..

echo.
echo ✅ Instalacion completa!
echo 🚀 Ejecuta start.bat para iniciar el sistema

pause
