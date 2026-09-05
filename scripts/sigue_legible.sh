#!/bin/bash
# ==============================================
# QUE SIGUE - CON ALIAS LEGIBLES
# ==============================================

DB="/sdcard/Download/analisis_consolidado.duckdb"
ALIAS_FILE="/data/data/com.termux/files/home/proyectos/nlp/alias_contenidos.csv"

echo "🎯 QUE SIGUE EN TU COLA DE APRENDIZAJE"
echo "======================================"
echo ""

# Obtener el siguiente contenido pendiente
VIDEO=$(duckdb "$DB" -csv -noheader -c "
SELECT t.video FROM terminos_raw t
JOIN progreso p ON t.video = p.video
WHERE p.estado = 'pendiente'
GROUP BY t.video
ORDER BY SUM(t.frequency) DESC
LIMIT 1;
" 2>/dev/null | head -1 | tr -d '\r')

if [ -z "$VIDEO" ]; then
    echo "🎉 ¡FELICITACIONES! No tenés contenidos pendientes."
    exit 0
fi

# Buscar alias
INFO=$(grep "^$VIDEO," "$ALIAS_FILE" 2>/dev/null)

if [ -n "$INFO" ]; then
    NOMBRE=$(echo "$INFO" | cut -d',' -f2)
    NICHO=$(echo "$INFO" | cut -d',' -f4)
    DESCRIPCION=$(echo "$INFO" | cut -d',' -f5)
    echo "📌 $NOMBRE"
    echo "   📂 Nicho: $NICHO"
    echo "   📝 $DESCRIPCION"
    echo "   🆔 ID: $VIDEO"
else
    echo "📌 $VIDEO (sin alias)"
fi

echo ""
echo "📋 ¿Cómo marcar como completado?"
echo "   listo \"$VIDEO\""
