#!/bin/bash

echo ""
echo "================================================"
echo "🚀 INICIANDO SISTEMA DE RECLUTAMIENTO"
echo "================================================"
echo ""
echo "📋 Modal de Candidatos Mejorado - Pruebas"
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "app.py" ]; then
    echo "❌ Error: No se encuentra app.py"
    echo "   Asegúrate de ejecutar este script desde /rh"
    exit 1
fi

echo "✅ Directorio correcto encontrado"
echo ""

# Activar entorno virtual si existe
if [ -f "venv/bin/activate" ]; then
    echo "🔧 Activando entorno virtual..."
    source venv/bin/activate
    echo "✅ Entorno virtual activado"
else
    echo "⚠️  No se encontró entorno virtual, usando Python global"
fi

echo ""
echo "🔍 Verificando dependencias..."
python3 -c "import flask, sqlalchemy, werkzeug" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Faltan dependencias. Instalando..."
    pip install -r requirements.txt
else
    echo "✅ Dependencias verificadas"
fi

echo ""
echo "🧪 Ejecutando pruebas del modal de candidatos..."
echo ""
python3 test_candidate_modal.py

echo ""
echo "================================================"
echo "🎯 INSTRUCCIONES PARA PROBAR EL MODAL"
echo "================================================"
echo ""
echo "1. Abre otra terminal y ejecuta el frontend:"
echo "   cd frontend"
echo "   npm start"
echo ""
echo "2. Ve a: http://localhost:3000/candidates"
echo ""
echo "3. Haz clic en \"Nuevo Candidato\" para probar el modal"
echo ""
echo "4. Campos requeridos:"
echo "   - Nombre Completo ✅"
echo "   - Teléfono ✅"
echo ""
echo "5. Campos opcionales:"
echo "   - Ubicación"
echo "   - LinkedIn Profile"
echo "   - Comentarios"
echo ""
echo "6. Prueba también editar candidatos existentes"
echo ""
echo "================================================"
echo "📝 CAMBIOS IMPLEMENTADOS"
echo "================================================"
echo ""
echo "✅ Modal responsive para candidatos"
echo "✅ Solo campos esenciales (nombre + teléfono)"
echo "✅ Email eliminado (no es requerido)"
echo "✅ Validaciones mejoradas"
echo "✅ Estados de carga claros"
echo "✅ Integración con la lista existente"
echo ""
read -p "Presiona Enter para continuar..."
