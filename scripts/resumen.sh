#!/bin/bash
# ==============================================
# RESUMEN EXPRESS - SOLO LO ESENCIAL
# ==============================================

ARCHIVO="$1"

if [ ! -f "$ARCHIVO" ]; then
    echo "❌ Uso: ./resumen.sh Transcript.txt"
    exit 1
fi

echo "📚 RESUMEN EXPRESS"
echo "=================="
echo ""
echo "📌 TÉRMINOS CLAVE:"
grep -A 10 "📌 Términos clave" "$ARCHIVO" | head -10
echo ""
echo "❓ PREGUNTAS CLAVE:"
grep -A 5 "❓ Preguntas clave" "$ARCHIVO"
echo ""
echo "🎯 OPORTUNIDADES:"
grep -A 5 "🎯 Oportunidades detectadas" "$ARCHIVO"
echo ""
echo "📖 DEFINICIONES:"
grep -A 5 "📖 Definiciones" "$ARCHIVO"
