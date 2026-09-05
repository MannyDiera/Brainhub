#!/bin/bash
# ==============================================
# ANALIZAR - CON VALIDACIÓN DE ARCHIVO
# ==============================================

ARCHIVO="$1"

if [ -z "$ARCHIVO" ]; then
    echo "❌ Error: Debes proporcionar un archivo"
    echo "📋 Uso: analizar archivo.txt"
    echo "📋 Ejemplo: analizar /sdcard/Download/Transcript_Z_ikDlimN6A_EN_FORZADO.txt"
    exit 1
fi

if [ ! -f "$ARCHIVO" ]; then
    echo "❌ Error: Archivo no encontrado: $ARCHIVO"
    echo "📋 Uso: analizar archivo.txt"
    exit 1
fi

# Ejecutar el análisis
python3 ~/proyectos/nlp/analisis_completo_v6.5.py "$ARCHIVO"
