#!/bin/bash
# ==============================================
# MAPA DE APRENDIZAJE - ECOSISTEMA DE CONTENIDOS
# ==============================================

echo "🗺️ MAPA DE APRENDIZAJE"
echo "======================"
echo ""

duckdb /sdcard/Download/analisis_consolidado.duckdb -c "
SELECT 
    CASE 
        WHEN SUM(frequency) >= 1000 THEN '🔴 Fundamental'
        WHEN SUM(frequency) >= 200 AND SUM(frequency) < 1000 THEN '🟡 Estructurante'
        ELSE '🟢 Complementario'
    END as grupo,
    video,
    SUM(frequency) as menciones
FROM terminos_raw
GROUP BY video
ORDER BY SUM(frequency) DESC;
"
