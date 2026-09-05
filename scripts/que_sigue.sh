#!/bin/bash
# ==============================================
# QUE SIGUE - GESTOR DE COLA DE APRENDIZAJE
# ==============================================

DB="/sdcard/Download/analisis_consolidado.duckdb"

echo "🎯 QUE SIGUE EN TU COLA DE APRENDIZAJE"
echo "======================================"
echo ""

# Contar pendientes - con manejo de errores
PENDIENTES=$(duckdb "$DB" -c "
SELECT COUNT(*) FROM progreso WHERE estado = 'pendiente';
" 2>/dev/null | grep -E '^[0-9]+$' | head -1)

# Si no se pudo obtener el número, asumir 0
if [ -z "$PENDIENTES" ]; then
    PENDIENTES=0
fi

if [ "$PENDIENTES" -eq 0 ]; then
    echo "🎉 ¡FELICITACIONES! No tenés contenidos pendientes."
    echo "📋 Todos los contenidos están completados."
    echo ""
    ~/progreso.sh
    exit 0
fi

# Obtener el siguiente contenido - con formato limpio
duckdb "$DB" -c "
SELECT 
    CASE 
        WHEN SUM(frequency) >= 1000 THEN '🔴 Fundamental'
        WHEN SUM(frequency) >= 200 AND SUM(frequency) < 1000 THEN '🟡 Estructurante'
        ELSE '🟢 Complementario'
    END as grupo,
    t.video as contenido,
    SUM(frequency) as menciones
FROM terminos_raw t
JOIN progreso p ON t.video = p.video
WHERE p.estado = 'pendiente'
GROUP BY t.video
ORDER BY 
    CASE 
        WHEN SUM(frequency) >= 1000 THEN 1
        WHEN SUM(frequency) >= 200 AND SUM(frequency) < 1000 THEN 2
        ELSE 3
    END,
    SUM(frequency) DESC
LIMIT 1;
"

echo ""
echo "📊 Pendientes: $PENDIENTES"
echo ""
echo "📋 ¿Cómo marcar como completado?"
echo "   listo \"nombre_parcial\""
echo "   Ejemplo: listo Git"
echo "   Ejemplo: listo Transcript_VgzHT9quo5c"
