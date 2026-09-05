#!/bin/bash
# Mostrar estado general del progreso

DB="/sdcard/Download/analisis_consolidado.duckdb"
ALIAS_FILE="/data/data/com.termux/files/home/proyectos/nlp/alias_contenidos.csv"

echo "📊 ESTADO GENERAL"
echo "================"

# Estadísticas
total=$(duckdb "$DB" -csv -noheader -c "SELECT COUNT(*) FROM progreso;" 2>/dev/null)
completados=$(duckdb "$DB" -csv -noheader -c "SELECT COUNT(*) FROM progreso WHERE estado='completado';" 2>/dev/null)
pendientes=$(duckdb "$DB" -csv -noheader -c "SELECT COUNT(*) FROM progreso WHERE estado='pendiente';" 2>/dev/null)

echo "📹 Total: $total"
echo "✅ Completados: $completados"
echo "📋 Pendientes: $pendientes"

# Porcentaje
if [ "$total" -gt 0 ]; then
    porcentaje=$(( (completados * 100) / total ))
    echo "📈 Progreso: $porcentaje%"
fi

echo ""
echo "📋 PENDIENTES:"
duckdb "$DB" -csv -noheader -c "
SELECT video FROM progreso WHERE estado='pendiente' ORDER BY video;" | while read video; do
    alias=$(grep "^$video," "$ALIAS_FILE" | cut -d',' -f2)
    echo "  📹 $( [ ! -z "$alias" ] && echo "$alias" || echo "$video" )"
done

echo ""
echo "✅ COMPLETADOS:"
duckdb "$DB" -csv -noheader -c "
SELECT video, fecha_completado FROM progreso WHERE estado='completado';" | while IFS=',' read video fecha; do
    alias=$(grep "^$video," "$ALIAS_FILE" | cut -d',' -f2)
    echo "  ✅ $( [ ! -z "$alias" ] && echo "$alias" || echo "$video" ) ($fecha)"
done
