#!/bin/bash
# ==============================================
# RESUMEN RÁPIDO 80/20 (MODULAR)
# Uso: ./resumen_rapido.sh archivo_analisis.json [URL_del_video]
# ==============================================

ARCHIVO="$1"
URL="$2"

if [ ! -f "$ARCHIVO" ]; then
    echo "❌ Uso: ./resumen_rapido.sh archivo_analisis.json [URL_del_video]"
    exit 1
fi

# Usar el módulo Python
python3 -c "
import sys
sys.path.insert(0, '/data/data/com.termux/files/home/proyectos/nlp')
from modulos.resumen import extraer_resumen_completo, resumen_a_texto

resumen = extraer_resumen_completo('$ARCHIVO')
print(resumen_a_texto(resumen, '$URL'))
"
