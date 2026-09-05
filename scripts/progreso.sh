#!/bin/bash
# ==============================================
# PROGRESO - VER ESTADO GENERAL (CORREGIDO)
# ==============================================

DB="/sdcard/Download/analisis_consolidado.duckdb"

echo "📊 PROGRESO DE APRENDIZAJE"
echo "=========================="
echo ""

# Obtener métricas usando -csv para evitar formateo
TOTAL=$(duckdb "$DB" -csv -noheader -c "SELECT COUNT(*) FROM progreso;" 2>/dev/null | head -1 | tr -d '\r')
COMPLETADOS=$(duckdb "$DB" -csv -noheader -c "SELECT COUNT(*) FROM progreso WHERE estado = 'completado';" 2>/dev/null | head -1 | tr -d '\r')

# Si no se obtienen números, mostrar 0
TOTAL=${TOTAL:-0}
COMPLETADOS=${COMPLETADOS:-0}

if [ "$TOTAL" -eq 0 ]; then
    echo "⚠️ No hay contenidos registrados aún."
    exit 0
fi

# Calcular porcentaje
PORCENTAJE=$(echo "scale=1; $COMPLETADOS * 100 / $TOTAL" | bc 2>/dev/null || echo "0")

# Generar barra de progreso
BARRA_LARGO=20
COMPLETADO_BARRA=$(echo "$COMPLETADOS * $BARRA_LARGO / $TOTAL" | bc 2>/dev/null || echo "0")
VACIO_BARRA=$((BARRA_LARGO - COMPLETADO_BARRA))

# Construir barra visual
BARRA=""
for ((i=0; i<COMPLETADO_BARRA; i++)); do
    BARRA="${BARRA}█"
done
for ((i=0; i<VACIO_BARRA; i++)); do
    BARRA="${BARRA}░"
done

echo "📈 Progreso general:"
echo "   $COMPLETADOS de $TOTAL contenidos completados"
echo "   [$BARRA] $PORCENTAJE%"
echo ""

echo "📋 DETALLE POR GRUPO:"
echo ""

# Fundamental
FUND_TOTAL=$(duckdb "$DB" -csv -noheader -c "
SELECT COUNT(*) FROM (
    SELECT t.video FROM terminos_raw t 
    JOIN progreso p ON t.video = p.video 
    GROUP BY t.video 
    HAVING SUM(t.frequency) >= 1000
);" 2>/dev/null | head -1 | tr -d '\r')
FUND_TOTAL=${FUND_TOTAL:-0}

FUND_COMP=$(duckdb "$DB" -csv -noheader -c "
SELECT COUNT(*) FROM (
    SELECT t.video FROM terminos_raw t 
    JOIN progreso p ON t.video = p.video 
    WHERE p.estado = 'completado'
    GROUP BY t.video 
    HAVING SUM(t.frequency) >= 1000
);" 2>/dev/null | head -1 | tr -d '\r')
FUND_COMP=${FUND_COMP:-0}

# Estructurante
ESTR_TOTAL=$(duckdb "$DB" -csv -noheader -c "
SELECT COUNT(*) FROM (
    SELECT t.video FROM terminos_raw t 
    JOIN progreso p ON t.video = p.video 
    GROUP BY t.video 
    HAVING SUM(t.frequency) >= 200 AND SUM(t.frequency) < 1000
);" 2>/dev/null | head -1 | tr -d '\r')
ESTR_TOTAL=${ESTR_TOTAL:-0}

ESTR_COMP=$(duckdb "$DB" -csv -noheader -c "
SELECT COUNT(*) FROM (
    SELECT t.video FROM terminos_raw t 
    JOIN progreso p ON t.video = p.video 
    WHERE p.estado = 'completado'
    GROUP BY t.video 
    HAVING SUM(t.frequency) >= 200 AND SUM(t.frequency) < 1000
);" 2>/dev/null | head -1 | tr -d '\r')
ESTR_COMP=${ESTR_COMP:-0}

# Complementario
COMPL_TOTAL=$(duckdb "$DB" -csv -noheader -c "
SELECT COUNT(*) FROM (
    SELECT t.video FROM terminos_raw t 
    JOIN progreso p ON t.video = p.video 
    GROUP BY t.video 
    HAVING SUM(t.frequency) < 200
);" 2>/dev/null | head -1 | tr -d '\r')
COMPL_TOTAL=${COMPL_TOTAL:-0}

COMPL_COMP=$(duckdb "$DB" -csv -noheader -c "
SELECT COUNT(*) FROM (
    SELECT t.video FROM terminos_raw t 
    JOIN progreso p ON t.video = p.video 
    WHERE p.estado = 'completado'
    GROUP BY t.video 
    HAVING SUM(t.frequency) < 200
);" 2>/dev/null | head -1 | tr -d '\r')
COMPL_COMP=${COMPL_COMP:-0}

# Mostrar grupos con barras
echo "   🔴 Fundamental:  $FUND_COMP/$FUND_TOTAL"
echo "   🟡 Estructurante: $ESTR_COMP/$ESTR_TOTAL"
echo "   🟢 Complementario: $COMPL_COMP/$COMPL_TOTAL"
echo ""

# Lista de pendientes
echo "📌 CONTENIDOS PENDIENTES (próximos 3):"
duckdb "$DB" -c "
SELECT 
    t.video as contenido,
    SUM(t.frequency) as menciones
FROM terminos_raw t
JOIN progreso p ON t.video = p.video
WHERE p.estado = 'pendiente'
GROUP BY t.video
ORDER BY SUM(t.frequency) DESC
LIMIT 3;
" 2>/dev/null

echo ""
