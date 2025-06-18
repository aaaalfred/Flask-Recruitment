@echo off
echo.
echo ================================================
echo 🚀 INICIANDO SISTEMA DE RECLUTAMIENTO
echo ================================================
echo.
echo 📋 Modal de Candidatos Mejorado - Pruebas
echo.

REM Verificar que estamos en el directorio correcto
if not exist "app.py" (
    echo ❌ Error: No se encuentra app.py
    echo    Asegurate de ejecutar este script desde C:\Users\ADMIN\code\rh
    pause
    exit /b 1
)

echo ✅ Directorio correcto encontrado
echo.

REM Activar entorno virtual si existe
if exist "venv\Scripts\activate.bat" (
    echo 🔧 Activando entorno virtual...
    call venv\Scripts\activate.bat
    echo ✅ Entorno virtual activado
) else (
    echo ⚠️  No se encontró entorno virtual, usando Python global
)

echo.
echo 🔍 Verificando dependencias...
python -c "import flask, sqlalchemy, werkzeug" 2>nul
if errorlevel 1 (
    echo ❌ Faltan dependencias. Instalando...
    pip install -r requirements.txt
) else (
    echo ✅ Dependencias verificadas
)

echo.
echo 🧪 Ejecutando pruebas del modal de candidatos...
echo.
python test_candidate_modal.py

echo.
echo ================================================
echo 🎯 INSTRUCCIONES PARA PROBAR EL MODAL
echo ================================================
echo.
echo 1. Abre otra terminal y ejecuta el frontend:
echo    cd frontend
echo    npm start
echo.
echo 2. Ve a: http://localhost:3000/candidates
echo.
echo 3. Haz clic en "Nuevo Candidato" para probar el modal
echo.
echo 4. Campos requeridos:
echo    - Nombre Completo ✅
echo    - Teléfono ✅
echo.
echo 5. Campos opcionales:
echo    - Ubicación
echo    - LinkedIn Profile
echo    - Comentarios
echo.
echo 6. Prueba también editar candidatos existentes
echo.
echo ================================================
echo 📝 CAMBIOS IMPLEMENTADOS
echo ================================================
echo.
echo ✅ Modal responsive para candidatos
echo ✅ Solo campos esenciales (nombre + teléfono)
echo ✅ Email eliminado (no es requerido)
echo ✅ Validaciones mejoradas
echo ✅ Estados de carga claros
echo ✅ Integración con la lista existente
echo.
pause
