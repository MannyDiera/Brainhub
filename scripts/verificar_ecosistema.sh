#!/bin/bash
# ==============================================
# VERIFICAR DEPENDENCIAS
# ==============================================

echo "🔍 Verificando dependencias..."
echo ""

# Python
if command -v python3 &> /dev/null; then
    echo "✅ Python3: $(python3 --version)"
else
    echo "❌ Python3 no instalado"
fi

# DuckDB
if command -v duckdb &> /dev/null; then
    echo "✅ DuckDB: $(duckdb --version 2>&1 | head -1)"
else
    echo "❌ DuckDB no instalado"
fi

# Streamlit
if python3 -c "import streamlit" 2>/dev/null; then
    echo "✅ Streamlit: $(streamlit --version 2>&1 | head -1)"
else
    echo "❌ Streamlit no instalado"
fi

# NLTK
if python3 -c "import nltk" 2>/dev/null; then
    echo "✅ NLTK instalado"
else
    echo "❌ NLTK no instalado"
fi

# TextBlob
if python3 -c "import textblob" 2>/dev/null; then
    echo "✅ TextBlob instalado"
else
    echo "❌ TextBlob no instalado"
fi

# espeak-ng
if command -v espeak-ng &> /dev/null; then
    echo "✅ espeak-ng: $(espeak-ng --version 2>&1 | head -1)"
else
    echo "❌ espeak-ng no instalado"
fi

# ffmpeg
if command -v ffmpeg &> /dev/null; then
    echo "✅ ffmpeg: $(ffmpeg -version 2>&1 | head -1)"
else
    echo "❌ ffmpeg no instalado"
fi

echo ""
echo "📁 Archivos de configuración:"
ls -lh ~/*.sh ~/*.py 2>/dev/null | head -10
