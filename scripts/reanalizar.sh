#!/bin/bash
# ==============================================
# REANALIZAR - FORZAR ANÁLISIS
# ==============================================

ARCHIVO="$1"

if [ -z "$ARCHIVO" ] || [ ! -f "$ARCHIVO" ]; then
    echo "❌ Uso: ./reanalizar.sh archivo.txt"
    exit 1
fi

# Borrar análisis existente
ANALISIS="${ARCHIVO%.txt}_analisis.txt"
if [ -f "$ANALISIS" ]; then
    rm -f "$ANALISIS"
    echo "🗑️  Análisis eliminado: $(basename "$ANALISIS")"
fi

# Ejecutar análisis
~/analizar.sh "$ARCHIVO"
