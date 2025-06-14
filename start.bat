@echo off
echo 🚀 SISTEMA DE GESTION RH - VERIFICACION RAPIDA
echo =============================================

echo.
echo 📋 Ejecutando verificacion...
python quick_check.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo 🌐 ¿Quieres iniciar el frontend? ^(s/n^)
    set /p respuesta="> "
    if /i "%respuesta%"=="s" (
        echo.
        echo 🚀 Iniciando frontend...
        cd frontend
        start cmd /k "npm start"
        cd ..
        echo ✅ Frontend iniciandose en nueva ventana...
    )
) else (
    echo.
    echo ❌ Hay problemas que resolver antes de continuar
)

echo.
pause
