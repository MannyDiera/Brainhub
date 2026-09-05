#!/bin/bash
# ==============================================
# COMPLETAR - MARCAR CONTENIDO COMO VISTO
# ==============================================

DB="/sdcard/Download/analisis_consolidado.duckdb"
BUSQUEDA="$1"

if [ -z "$BUSQUEDA" ]; then
    echo "❌ Error: Tenés que escribir algo para buscar."
    echo "📋 Uso: listo \"nombre_parcial\""
    echo "📋 Ejemplo: listo Git"
    exit 0
fi

# Buscar el video usando formato CSV para evitar caracteres de tabla
VIDEO=$(duckdb "$DB" -csv -noheader -c "
SELECT video FROM terminos_raw 
WHERE video LIKE '%$BUSQUEDA%' 
LIMIT 1;
" 2>/dev/null | head -1 | tr -d '\r')

if [ -z "$VIDEO" ]; then
    echo "❌ No se encontró ningún contenido con: '$BUSQUEDA'"
    echo "📋 Contenidos disponibles (primeros 10):"
    duckdb "$DB" -csv -noheader -c "SELECT DISTINCT video FROM terminos_raw LIMIT 10;"
    exit 0
fi

echo "✅ Video encontrado: $VIDEO"

# Verificar si ya está completado
ESTADO=$(duckdb "$DB" -csv -noheader -c "SELECT estado FROM progreso WHERE video = '$VIDEO';" 2>/dev/null | head -1 | tr -d '\r')

if [ "$ESTADO" = "completado" ]; then
    echo "✅ '$VIDEO' ya estaba marcado como completado."
    echo ""
    echo "🎯 Siguiente contenido:"
    ~/que_sigue.sh
    exit 0
fi

# Obtener tipo del contenido
TIPO=$(duckdb "$DB" -csv -noheader -c "
SELECT CASE 
    WHEN SUM(frequency) >= 1000 THEN 'Fundamental'
    WHEN SUM(frequency) >= 200 AND SUM(frequency) < 1000 THEN 'Estructurante'
    ELSE 'Complementario'
END as tipo
FROM terminos_raw
WHERE video = '$VIDEO'
GROUP BY video;
" 2>/dev/null | head -1 | tr -d '\r')

# Fecha actual
FECHA=$(date +%Y-%m-%d)

# Marcar como completado
duckdb "$DB" -c "
UPDATE progreso 
SET estado = 'completado', 
    fecha_completado = '$FECHA'
WHERE video = '$VIDEO';
"

echo "✅ '$VIDEO' marcado como completado."
echo "📊 Tipo: $TIPO"
echo ""
echo "🎯 Siguiente contenido:"
~/que_sigue.sh
