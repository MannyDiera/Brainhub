#!/bin/bash
# Shadow test: compara versiones antes de hacer push

if [ -z "$1" ]; then
    echo "❌ Uso: shadow_test.sh archivo_entrada.txt"
    echo "📋 Compara v6.5 (actual) vs v6.4 (anterior)"
    exit 1
fi

echo "🧪 Ejecutando shadow test..."
python3 ~/proyectos/nlp/modulos/shadow_testing.py "$1" analisis_completo_v6.4.py
