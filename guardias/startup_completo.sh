#!/bin/bash
# Startup completo de BrainHub - cadena de guardias

set -e

echo "🚀 BrainHub - Verificación de startup"
echo "===================================="

./guardias/identidad.sh
./guardias/schema_duckdb.sh
./guardias/stopwords.sh
./guardias/diccionarios.sh

echo ""
echo "✅ Todas las guardias pasaron"
echo "🧠 BrainHub operativo"
