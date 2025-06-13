#!/bin/bash

echo "🧹 Limpiando repositorio Git..."
echo "================================"

# Ir al directorio raíz del proyecto
cd "$(dirname "$0")"

# Hacer unstage de todos los archivos nuevos
echo "📂 Removiendo archivos del staging area..."
git reset

# Limpiar archivos no trackeados (pero mantener directorios importantes)
echo "🗑️ Limpiando archivos temporales..."
git clean -fd --exclude=frontend/node_modules --exclude=venv --exclude=.env

# Mostrar estado actual
echo "📊 Estado actual del repositorio:"
git status --porcelain | head -20

echo ""
echo "✅ Limpieza completada!"
echo ""
echo "📋 Para añadir solo los archivos importantes:"
echo "git add ."
echo "git commit -m 'Add frontend and complete RH system'"
echo ""
echo "🔍 Archivos que serán ignorados:"
echo "- frontend/node_modules/ (dependencias Node.js)"
echo "- venv/ (entorno virtual Python)"
echo "- .env (variables de entorno)"
echo "- __pycache__/ (archivos Python compilados)"
echo "- *.log (archivos de log)"
