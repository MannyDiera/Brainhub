#!/bin/bash
# ==============================================
# COMPILAR CON WAKE-LOCK
# Uso: ./compilar.sh "pip install duckdb"
# ==============================================

if [ -z "$1" ]; then
    echo "❌ Uso: ./compilar.sh \"comando_a_ejecutar\""
    exit 1
fi

echo "🔒 Activando wake-lock..."
termux-wake-lock

echo "📦 Ejecutando: $1"
eval "$1"

echo "🔓 Liberando wake-lock..."
termux-wake-unlock

echo "✅ Proceso completado"
