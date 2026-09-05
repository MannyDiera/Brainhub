#!/bin/bash
# ==============================================
# GENERAR AUDIO DESDE JSON (OPCIONAL)
# Uso: ./audio_desde_json.sh archivo_analisis_completo.json
# ==============================================

JSON="$1"

if [ ! -f "$JSON" ]; then
    echo "❌ Uso: ./audio_desde_json.sh archivo_analisis_completo.json"
    exit 1
fi

python3 -c "
import sys
sys.path.insert(0, '/data/data/com.termux/files/home/proyectos/nlp')
from modulos.generar_audio import generar_audio_si_aplica

generar_audio_si_aplica('$JSON')
"
