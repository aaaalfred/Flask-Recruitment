@echo off
echo ========================================
echo 🔧 CONFIGURACION COMPLETA DEL ENTORNO
echo ========================================
echo.

cd /d C:\Users\ADMIN\code\rh
echo 📁 Directorio actual: %CD%
echo.

echo 🔍 Verificando entorno virtual...
if exist "venv\Scripts\activate.bat" (
    echo ✅ Entorno virtual encontrado
    echo 🚀 Activando entorno virtual...
    call venv\Scripts\activate.bat
    echo ✅ Entorno virtual activado
) else (
    echo ⚠️  Entorno virtual no encontrado, creando uno nuevo...
    python -m venv venv
    echo ✅ Entorno virtual creado
    echo 🚀 Activando entorno virtual...
    call venv\Scripts\activate.bat
    echo ✅ Entorno virtual activado
)

echo.
echo 📦 Instalando dependencias...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo 🧪 Verificando instalación...
python -c "import flask; print('✅ Flask instalado:', flask.__version__)"
python -c "import flask_sqlalchemy; print('✅ Flask-SQLAlchemy instalado')"
python -c "import pymysql; print('✅ PyMySQL instalado')"

echo.
echo ========================================
echo ✅ ENTORNO CONFIGURADO CORRECTAMENTE
echo ========================================
echo.
echo 🎯 Ahora puedes ejecutar:
echo    python app.py
echo    python test_utf8_simple.py
echo    python test_vacants.py
echo.
pause
