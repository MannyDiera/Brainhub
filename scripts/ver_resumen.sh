#!/bin/bash
# ==============================================
# VER RESUMEN DE UN CONTENIDO CON SU URL
# Uso: ./ver_resumen.sh Transcript_ID_analisis.txt [URL]
# ==============================================

ARCHIVO="$1"
URL="$2"

if [ ! -f "$ARCHIVO" ]; then
    echo "❌ Archivo no encontrado: $ARCHIVO"
    echo "📋 Uso: ./ver_resumen.sh Transcript_ID_analisis.txt [URL]"
    exit 1
fi

~/resumen_rapido.sh "$ARCHIVO" "$URL"
