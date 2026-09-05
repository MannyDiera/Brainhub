#!/bin/bash
# ==============================================
# COMPARADOR DE CONTENIDO v4 (FORMATO LIMPIO)
# Uso: ./comparar_contenido.sh archivo1_analisis.txt archivo2_analisis.txt
# ==============================================

ARCHIVO1="$1"
ARCHIVO2="$2"

if [ ! -f "$ARCHIVO1" ] || [ ! -f "$ARCHIVO2" ]; then
    echo "❌ Uso: ./comparar_contenido.sh archivo1_analisis.txt archivo2_analisis.txt"
    exit 1
fi

echo "📊 COMPARATIVA DE CONTENIDO"
echo "==========================="
echo ""

# Directorio temporal en HOME (con permisos)
TEMP_DIR="$HOME/temp_comparar"
mkdir -p "$TEMP_DIR"

# Extraer métricas de archivo1
NOMBRE1=$(basename "$ARCHIVO1" .txt | sed 's/_analisis//')
TERMINOS1=$(grep -A 15 "📌 Términos clave" "$ARCHIVO1" | grep -E "^  [a-z]" | head -3 | awk '{print $1}' | tr '\n' ', ' | sed 's/, $//' | sed 's/,$//' | sed 's/://g')
SENTIMIENTO1=$(grep -A 5 "😊 ANÁLISIS DE SENTIMIENTO" "$ARCHIVO1" | grep "Polaridad:" | awk '{print $2}')

# Extraer métricas de archivo2
NOMBRE2=$(basename "$ARCHIVO2" .txt | sed 's/_analisis//')
TERMINOS2=$(grep -A 15 "📌 Términos clave" "$ARCHIVO2" | grep -E "^  [a-z]" | head -3 | awk '{print $1}' | tr '\n' ', ' | sed 's/, $//' | sed 's/,$//' | sed 's/://g')
SENTIMIENTO2=$(grep -A 5 "😊 ANÁLISIS DE SENTIMIENTO" "$ARCHIVO2" | grep "Polaridad:" | awk '{print $2}')

# Ejecutar clasificador para obtener métricas completas
echo "📊 Generando métricas para $NOMBRE1..."
~/clasificador_contenido.sh "$ARCHIVO1" > "$TEMP_DIR/m1.txt"
COMPLEJIDAD1=$(grep "Complejidad:" "$TEMP_DIR/m1.txt" | cut -d':' -f2- | sed 's/^ //')
DENSIDAD1=$(grep "Densidad técnica:" "$TEMP_DIR/m1.txt" | grep -o "[0-9.]*" | head -1)
PALABRAS1=$(grep "Palabras totales:" "$TEMP_DIR/m1.txt" | grep -o "[0-9]*" | head -1)
ESTILO1=$(grep "Estilo:" "$TEMP_DIR/m1.txt" | cut -d':' -f2- | sed 's/^ //')

echo "📊 Generando métricas para $NOMBRE2..."
~/clasificador_contenido.sh "$ARCHIVO2" > "$TEMP_DIR/m2.txt"
COMPLEJIDAD2=$(grep "Complejidad:" "$TEMP_DIR/m2.txt" | cut -d':' -f2- | sed 's/^ //')
DENSIDAD2=$(grep "Densidad técnica:" "$TEMP_DIR/m2.txt" | grep -o "[0-9.]*" | head -1)
PALABRAS2=$(grep "Palabras totales:" "$TEMP_DIR/m2.txt" | grep -o "[0-9]*" | head -1)
ESTILO2=$(grep "Estilo:" "$TEMP_DIR/m2.txt" | cut -d':' -f2- | sed 's/^ //')

# Limpiar temporales
rm -rf "$TEMP_DIR"

# Si no hay densidad, poner 0
DENSIDAD1=${DENSIDAD1:-0}
DENSIDAD2=${DENSIDAD2:-0}

# Mostrar tabla
printf "%-25s | %-30s | %-30s\n" "Métrica" "${NOMBRE1:0:30}" "${NOMBRE2:0:30}"
echo "--------------------------+----------------------------+----------------------------"
printf "%-25s | %-30s | %-30s\n" "Términos clave" "${TERMINOS1:0:30}" "${TERMINOS2:0:30}"
printf "%-25s | %-30s | %-30s\n" "Sentimiento" "${SENTIMIENTO1:-No disponible}" "${SENTIMIENTO2:-No disponible}"
printf "%-25s | %-30s | %-30s\n" "Complejidad" "${COMPLEJIDAD1:-No disponible}" "${COMPLEJIDAD2:-No disponible}"
printf "%-25s | %-30s | %-30s\n" "Densidad técnica" "${DENSIDAD1}%" "${DENSIDAD2}%"
printf "%-25s | %-30s | %-30s\n" "Palabras totales" "${PALABRAS1:-0}" "${PALABRAS2:-0}"
printf "%-25s | %-30s | %-30s\n" "Estilo" "${ESTILO1:-No disponible}" "${ESTILO2:-No disponible}"

echo ""
echo "💡 RECOMENDACIÓN FINAL"
echo "---------------------"

# Determinar cuál es más simple
if [[ "$COMPLEJIDAD1" == *"Bajo"* ]] || [[ "$COMPLEJIDAD1" == *"Simple"* ]]; then
    echo "1️⃣ Empieza con: $NOMBRE1 (más simple, densidad ${DENSIDAD1}%)"
    echo "2️⃣ Luego profundiza con: $NOMBRE2 (más técnico, densidad ${DENSIDAD2}%)"
elif [[ "$COMPLEJIDAD2" == *"Bajo"* ]] || [[ "$COMPLEJIDAD2" == *"Simple"* ]]; then
    echo "1️⃣ Empieza con: $NOMBRE2 (más simple, densidad ${DENSIDAD2}%)"
    echo "2️⃣ Luego profundiza con: $NOMBRE1 (más técnico, densidad ${DENSIDAD1}%)"
else
    echo "📌 Ambos son complejos. Recomendación por densidad técnica:"
    if (( $(echo "$DENSIDAD1 < $DENSIDAD2" | bc -l 2>/dev/null || echo "0") )); then
        echo "1️⃣ Empieza con: $NOMBRE1 (densidad ${DENSIDAD1}%)"
        echo "2️⃣ Luego: $NOMBRE2 (densidad ${DENSIDAD2}%)"
    else
        echo "1️⃣ Empieza con: $NOMBRE2 (densidad ${DENSIDAD2}%)"
        echo "2️⃣ Luego: $NOMBRE1 (densidad ${DENSIDAD1}%)"
    fi
fi
