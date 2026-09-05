#!/bin/bash
# ==============================================
# CLASIFICADOR DE CONTENIDO v2
# Uso: ./clasificador_contenido.sh Transcript_analisis.txt
# ==============================================

ARCHIVO="$1"

if [ ! -f "$ARCHIVO" ]; then
    echo "❌ Uso: ./clasificador_contenido.sh Transcript_analisis.txt"
    exit 1
fi

echo "🔍 ANALIZANDO CONTENIDO"
echo "======================="
echo ""

# ==============================================
# 1. EXTRAER MÉTRICAS DEL ANÁLISIS
# ==============================================

# Extraer sentimiento
SENTIMIENTO=$(grep -A 5 "😊 ANÁLISIS DE SENTIMIENTO" "$ARCHIVO" | grep "Polaridad:" | awk '{print $2}' | tr -d ',')
INTERPRETACION=$(grep -A 5 "😊 ANÁLISIS DE SENTIMIENTO" "$ARCHIVO" | grep "Interpretación:" | cut -d':' -f2- | sed 's/^ //' | tr -d ',')

# Extraer términos clave (top 5, sin comas)
TERMINOS=$(grep -A 20 "📌 Términos clave" "$ARCHIVO" | grep -E "^  [a-z]" | head -5 | awk '{print $1}' | tr '\n' ', ' | sed 's/, $//' | sed 's/,$//')

# Extraer preguntas clave
PREGUNTAS=$(grep -A 10 "❓ Preguntas clave" "$ARCHIVO" | grep -E "^  " | head -2 | sed 's/^  //')

# Extraer oportunidades
OPORTUNIDADES=$(grep -A 10 "🎯 Oportunidades detectadas" "$ARCHIVO" | grep -E "^  " | head -2 | sed 's/^  //')

# Detectar estilo (basado en palabras clave)
if grep -qi "tutorial\|paso a paso\|cómo hacer\|vamos a\|ejemplo" "$ARCHIVO"; then
    ESTILO="Práctico/Tutorial"
elif grep -qi "teórico\|concepto\|framework\|metodología\|principio" "$ARCHIVO"; then
    ESTILO="Técnico/Formal"
else
    ESTILO="Mixto"
fi

# ==============================================
# 2. CALCULAR COMPLEJIDAD
# ==============================================

# Contar términos técnicos (actualizado para ambos videos)
TERMINOS_TECNICOS=$(grep -oE '\b(framework|agente|modelo|memoria|cadena|herramienta|api|llm|prompt|token|embeddings|vector|inteligencia|datos|fase|análisis|procesamiento|infraestructura|opsec|ciclo|pivotaje|hash|atribución|chain|langchain|osint|inteligencia|fuentes|abiertas|recolección|procesado|estructura|limpia|enriquecimiento|pivotar|matriz|preservación|confianza|certeza)\b' "$ARCHIVO" | wc -l)

# Palabras totales
PALABRAS=$(wc -w < "$ARCHIVO")

# Calcular densidad técnica (usando bc o fallback)
if command -v bc &> /dev/null; then
    DENSIDAD_TECNICA=$(echo "scale=2; $TERMINOS_TECNICOS * 100 / $PALABRAS" | bc 2>/dev/null || echo "0")
else
    DENSIDAD_TECNICA="0"
fi

# Determinar complejidad con fallback numérico
if [ -n "$DENSIDAD_TECNICA" ] && [ "$DENSIDAD_TECNICA" != "0" ]; then
    if (( $(echo "$DENSIDAD_TECNICA > 5" | bc -l 2>/dev/null || echo "0") )); then
        COMPLEJIDAD="Complejo"
        NIVEL="🔴 Alto"
    elif (( $(echo "$DENSIDAD_TECNICA > 2" | bc -l 2>/dev/null || echo "0") )); then
        COMPLEJIDAD="Intermedio"
        NIVEL="🟡 Medio"
    else
        COMPLEJIDAD="Simple"
        NIVEL="🟢 Bajo"
    fi
else
    # Fallback basado en palabras totales
    if [ "$PALABRAS" -gt 10000 ]; then
        COMPLEJIDAD="Complejo"
        NIVEL="🔴 Alto"
    elif [ "$PALABRAS" -gt 5000 ]; then
        COMPLEJIDAD="Intermedio"
        NIVEL="🟡 Medio"
    else
        COMPLEJIDAD="Simple"
        NIVEL="🟢 Bajo"
    fi
fi

# ==============================================
# 3. CALCULAR RECOMENDACIÓN
# ==============================================

# Basado en sentimiento
if [ -n "$SENTIMIENTO" ]; then
    if (( $(echo "$SENTIMIENTO > 0.2" | bc -l 2>/dev/null || echo "0") )); then
        RECOMENDACION_SENTIMIENTO="✅ Contenido positivo"
    elif (( $(echo "$SENTIMIENTO > -0.2" | bc -l 2>/dev/null || echo "0") )); then
        RECOMENDACION_SENTIMIENTO="⚪ Contenido neutral/objetivo"
    else
        RECOMENDACION_SENTIMIENTO="⚠️  Contenido crítico"
    fi
else
    RECOMENDACION_SENTIMIENTO="❓ Sin datos de sentimiento"
fi

# Basado en estilo
if [ "$ESTILO" = "Práctico/Tutorial" ]; then
    RECOMENDACION_ESTILO="✅ Ideal para aprendizaje práctico"
elif [ "$ESTILO" = "Técnico/Formal" ]; then
    RECOMENDACION_ESTILO="📚 Ideal para profundizar conceptos"
else
    RECOMENDACION_ESTILO="📖 Contenido general"
fi

# Recomendación general
if [ "$COMPLEJIDAD" = "Simple" ] && [ "$ESTILO" = "Práctico/Tutorial" ]; then
    RECOMENDACION_FINAL="🌟 ALTAMENTE RECOMENDADO para principiantes"
elif [ "$COMPLEJIDAD" = "Intermedio" ] && [ "$ESTILO" = "Técnico/Formal" ]; then
    RECOMENDACION_FINAL="📈 RECOMENDADO para estudiantes intermedios"
elif [ "$COMPLEJIDAD" = "Complejo" ]; then
    RECOMENDACION_FINAL="🎓 RECOMENDADO para expertos o con preparación previa"
else
    RECOMENDACION_FINAL="📖 Útil como referencia"
fi

# ==============================================
# 4. MOSTRAR RESULTADOS
# ==============================================

echo "📊 MÉTRICAS DE CONTENIDO"
echo "-----------------------"
echo ""
echo "📌 Términos clave: $TERMINOS"
echo "📖 Estilo: $ESTILO"
echo "😊 Sentimiento: $SENTIMIENTO ($INTERPRETACION)"
echo "📊 Complejidad: $NIVEL ($COMPLEJIDAD)"
echo "   - Palabras totales: $PALABRAS"
echo "   - Términos técnicos: $TERMINOS_TECNICOS"
echo "   - Densidad técnica: ${DENSIDAD_TECNICA}%"
echo ""

echo "❓ Preguntas clave:"
echo "$PREGUNTAS" | sed 's/^/   /'
echo ""

echo "🎯 Oportunidades:"
echo "$OPORTUNIDADES" | sed 's/^/   /'
echo ""

echo "💡 RECOMENDACIONES"
echo "-----------------"
echo "   $RECOMENDACION_SENTIMIENTO"
echo "   $RECOMENDACION_ESTILO"
echo "   $RECOMENDACION_FINAL"
echo ""

echo "✅ Clasificación completada"
