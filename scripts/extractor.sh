#!/bin/bash
# ==============================================
# EXTRACTOR DE SECCIONES DE ANÁLISIS
# Uso: ./extractor.sh archivo_analisis.txt
# ==============================================

ARCHIVO="$1"

if [ ! -f "$ARCHIVO" ]; then
    echo "❌ Uso: ./extractor.sh archivo_analisis.txt"
    exit 1
fi

echo "📋 EXTRACCIÓN DE SECCIONES"
echo "=========================="
echo ""

# 1. Preguntas clave
echo "❓ PREGUNTAS CLAVE:"
grep -A 10 "❓ Preguntas clave" "$ARCHIVO" | grep -v "❓ Preguntas clave" | head -10
echo ""

# 2. Oportunidades
echo "🎯 OPORTUNIDADES:"
grep -A 10 "🎯 Oportunidades" "$ARCHIVO" | grep -v "🎯 Oportunidades" | head -10
echo ""

# 3. Definiciones
echo "📖 DEFINICIONES:"
grep -A 10 "📖 Definiciones" "$ARCHIVO" | grep -v "📖 Definiciones" | head -10
echo ""

# 4. Términos clave (top 5)
echo "📌 TÉRMINOS CLAVE (top 5):"
grep -A 10 "📌 Términos clave" "$ARCHIVO" | grep -E "^  [a-z]" | head -5
echo ""

# 5. Sentimiento (si existe)
echo "😊 SENTIMIENTO:"
grep -A 5 "😊 ANÁLISIS DE SENTIMIENTO" "$ARCHIVO" | grep -v "😊 ANÁLISIS DE SENTIMIENTO" | head -5
