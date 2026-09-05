#!/bin/bash
# ==============================================
# ANÁLISIS COMPLETO - VERSIÓN UNIFICADA
# Uso: ./analisis_completo.sh archivo_transcripcion.txt
# ==============================================

ARCHIVO="$1"

if [ ! -f "$ARCHIVO" ]; then
    echo "❌ Uso: ./analisis_completo.sh archivo_transcripcion.txt"
    exit 1
fi

echo "🧠 ANÁLISIS COMPLETO DEL DOCUMENTO"
echo "=================================="
echo ""

# 1. Análisis básico con NLP
echo "📊 ANÁLISIS NLP BÁSICO"
~/analizar.sh "$ARCHIVO"

# 2. Segmentación avanzada de hablantes
echo ""
echo "💬 SEGMENTACIÓN DE HABLANTES (V2)"
python3 ~/segmentar_hablantes_v2.py "$ARCHIVO"

# 3. Sentimiento por segmento
echo ""
echo "😊 SENTIMIENTO POR SEGMENTO (V2)"
python3 ~/sentimiento_segmentos_v2.py "$ARCHIVO"

# 4. Resumen ejecutivo
echo ""
echo "📋 RESUMEN EJECUTIVO"
echo "===================="
ANALISIS_TXT="${ARCHIVO%.txt}_analisis.txt"
if [ -f "$ANALISIS_TXT" ]; then
    echo "📌 Términos clave (top 5):"
    grep -A 5 "📌 Términos clave" "$ANALISIS_TXT" | grep -E "^  [a-z]" | head -5
    
    echo ""
    echo "😊 Sentimiento general:"
    grep -A 3 "😊 ANÁLISIS DE SENTIMIENTO" "$ANALISIS_TXT" | head -4
fi

echo ""
echo "✅ Análisis completo finalizado"
