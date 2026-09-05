#!/bin/bash
# ==============================================
# ANÁLISIS AVANZADO - POST PROCESAMIENTO
# Uso: ./analizar_avanzado.sh archivo_analisis.txt
# ==============================================

ARCHIVO="$1"

if [ ! -f "$ARCHIVO" ]; then
    echo "❌ Uso: ./analizar_avanzado.sh archivo_analisis.txt"
    exit 1
fi

echo "🧠 ANÁLISIS AVANZADO"
echo "===================="
echo ""

# 1. Extracción de secciones
echo "📋 EXTRACCIÓN DE SECCIONES:"
grep -A 10 "❓ Preguntas clave" "$ARCHIVO" | head -5
echo ""

# 2. Segmentación por hablante (si hay diálogos)
echo "💬 SEGMENTACIÓN POR HABLANTE:"
python3 ~/segmentar_hablantes.py "$ARCHIVO" 2>/dev/null || echo "  (No se detectaron diálogos)"
echo ""

# 3. Sentimiento por segmento
echo "😊 SENTIMIENTO POR SEGMENTO:"
python3 ~/sentimiento_segmentos.py "$ARCHIVO" 2>/dev/null | head -10
echo ""

# 4. Términos clave (sin stopwords)
echo "📌 TÉRMINOS CLAVE (sin stopwords):"
grep -A 15 "📌 Términos clave" "$ARCHIVO" | grep -E "^  [a-z]" | head -10

echo ""
echo "✅ Análisis avanzado completado"
