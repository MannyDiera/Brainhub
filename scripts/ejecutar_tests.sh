#!/bin/bash
# ==============================================
# EJECUTAR TESTS CRÍTICOS
# ==============================================

echo "🧪 EJECUTANDO TESTS CRÍTICOS"
echo "============================"
echo ""

cd ~/proyectos/nlp

# Verificar que pytest está instalado
if ! python3 -c "import pytest" 2>/dev/null; then
    echo "📦 Instalando pytest..."
    pip install pytest pytest-cov
fi

# Ejecutar tests críticos
pytest tests/test_criticos.py -v --tb=short

echo ""
echo "✅ Tests completados"
