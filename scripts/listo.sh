#!/bin/bash
# Marcar contenido como completado

DB="/sdcard/Download/analisis_consolidado.duckdb"
ALIAS_FILE="/data/data/com.termux/files/home/proyectos/nlp/alias_contenidos.csv"

if [ -z "$1" ]; then
    echo "Uso: listo <video_id>"
    echo ""
    echo "Contenidos pendientes:"
    duckdb "$DB" -csv -noheader -c "
    SELECT video FROM progreso WHERE estado = 'pendiente';" | while read video; do
        alias=$(grep "^$video," "$ALIAS_FILE" | cut -d',' -f2)
        echo "  📹 $alias ($video)"
    done
    exit 1
fi

VIDEO="$1"

# Verificar que existe
existe=$(duckdb "$DB" -csv -noheader -c "
SELECT COUNT(*) FROM progreso WHERE video = '$VIDEO';" 2>/dev/null)

if [ "$existe" = "0" ]; then
    echo "❌ Video no encontrado: $VIDEO"
    exit 1
fi

# Marcar como completado
duckdb "$DB" -c "
UPDATE progreso 
SET estado = 'completado', 
    fecha_completado = CURRENT_DATE 
WHERE video = '$VIDEO';"

alias=$(grep "^$VIDEO," "$ALIAS_FILE" | cut -d',' -f2)
echo "✅ $( [ ! -z "$alias" ] && echo "$alias" || echo "$VIDEO" ) marcado como completado"
