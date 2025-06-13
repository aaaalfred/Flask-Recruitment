#!/bin/bash

echo "🚀 Instalando Sistema de Gestión de RH - Frontend y Backend"
echo "==========================================================="

# Verificar que estamos en el directorio correcto
if [ ! -f "app.py" ]; then
    echo "❌ Error: Ejecuta este script desde la carpeta raíz del proyecto (donde está app.py)"
    exit 1
fi

echo "📦 Instalando dependencias del backend..."
# Activar entorno virtual si existe
if [ -d "venv" ]; then
    echo "🔄 Activando entorno virtual..."
    source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null
else
    echo "⚠️  No se encontró entorno virtual. Creando uno nuevo..."
    python -m venv venv
    source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null
fi

# Instalar dependencias de Python
pip install -r requirements.txt

echo "📦 Instalando dependencias del frontend..."
cd frontend

# Verificar que Node.js esté instalado
if ! command -v node &> /dev/null; then
    echo "❌ Node.js no está instalado."
    echo "👉 Por favor instala Node.js desde https://nodejs.org/"
    echo "👉 Luego ejecuta: cd frontend && npm install && npm start"
    exit 1
fi

# Instalar dependencias de Node.js
npm install

echo "✅ ¡Instalación completada!"
echo ""
echo "🚀 Para iniciar el sistema:"
echo "1. Backend (desde la carpeta raíz):"
echo "   python app.py"
echo ""
echo "2. Frontend (desde la carpeta frontend):"
echo "   cd frontend"
echo "   npm start"
echo ""
echo "🌐 URLs:"
echo "- Frontend: http://localhost:3000"
echo "- Backend API: http://localhost:5000/api"
echo ""
echo "🔐 Credenciales de prueba:"
echo "- Ejecutivo: admin@empresa.com / admin123"
echo "- Reclutador: reclutador@empresa.com / reclutador123"
echo ""
echo "📚 Para más información:"
echo "- Backend: README.md"
echo "- Frontend: frontend/README.md"
