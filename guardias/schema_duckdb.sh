#!/bin/bash
# Guardia: verifica esquema de DuckDB

echo "🗄️ Verificando esquema de DuckDB..."

DB="/sdcard/Download/analisis_consolidado.duckdb"

duckdb "$DB" -c "SHOW TABLES;" 2>/dev/null | grep -q "terminos_raw" || {
    echo "❌ Tabla terminos_raw no existe"
    exit 1
}

duckdb "$DB" -c "SHOW TABLES;" 2>/dev/null | grep -q "progreso" || {
    echo "❌ Tabla progreso no existe"
    exit 1
}

echo "✅ Esquema DuckDB OK"
