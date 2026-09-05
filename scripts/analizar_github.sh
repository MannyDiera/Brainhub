#!/bin/bash
# ==============================================
# ANALIZAR REPOSITORIO DE GITHUB (CORREGIDO)
# Uso: ./analizar_github.sh usuario/repo [rama]
# Ejemplo: ./analizar_github.sh msamiullah-ai/ML-Math-Bridge main
# ==============================================

REPO="$1"
BRANCH="${2:-main}"
OUTPUT_DIR="/sdcard/Download/github_analisis"

if [ -z "$REPO" ]; then
    echo "❌ Uso: ./analizar_github.sh usuario/repo [rama]"
    echo "📋 Ejemplo: ./analizar_github.sh msamiullah-ai/ML-Math-Bridge main"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

echo "🚀 ANALIZANDO REPOSITORIO: $REPO"
echo "================================="
echo "📂 Rama: $BRANCH"
echo ""

# 1. Descargar el repositorio como ZIP
echo "📥 Descargando repositorio..."
ZIP_URL="https://github.com/$REPO/archive/refs/heads/$BRANCH.zip"
ZIP_FILE="$OUTPUT_DIR/${REPO//\//_}_$BRANCH.zip"

if [ -f "$ZIP_FILE" ]; then
    echo "✅ ZIP ya existe: $(basename "$ZIP_FILE")"
else
    curl -L -o "$ZIP_FILE" "$ZIP_URL" 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "❌ Error al descargar: $ZIP_URL"
        exit 1
    fi
    echo "✅ ZIP descargado: $(basename "$ZIP_FILE")"
fi

# 2. Extraer archivos
echo "📦 Extrayendo archivos..."

# Detectar el nombre de la carpeta extraída (el nombre del repositorio sin el usuario)
REPO_NAME=$(basename "$REPO")
EXTRACT_DIR="$OUTPUT_DIR/${REPO_NAME}-$BRANCH"

if [ -d "$EXTRACT_DIR" ]; then
    echo "✅ Ya extraído: $(basename "$EXTRACT_DIR")"
else
    # Probar a extraer
    unzip -q "$ZIP_FILE" -d "$OUTPUT_DIR" 2>/dev/null
    
    # Buscar la carpeta extraída (puede tener un nombre ligeramente diferente)
    EXTRACT_DIR=$(find "$OUTPUT_DIR" -maxdepth 1 -type d -name "*-$BRANCH" | head -1)
    
    if [ -z "$EXTRACT_DIR" ]; then
        # Buscar cualquier carpeta que contenga el nombre del repo
        EXTRACT_DIR=$(find "$OUTPUT_DIR" -maxdepth 1 -type d -name "*${REPO_NAME}*" | head -1)
    fi
    
    if [ -n "$EXTRACT_DIR" ]; then
        echo "✅ Extraído en: $(basename "$EXTRACT_DIR")"
    else
        echo "❌ No se pudo encontrar la carpeta extraída"
        exit 1
    fi
fi

# 3. Buscar archivos de texto relevantes
echo "🔍 Buscando archivos relevantes..."
TEMP_FILE="$OUTPUT_DIR/texto_combinado.txt"
> "$TEMP_FILE"

# Contar archivos encontrados
FILE_COUNT=0

# Archivos a incluir
find "$EXTRACT_DIR" -type f \( \
    -name "*.md" -o \
    -name "*.txt" -o \
    -name "*.rst" -o \
    -name "*.py" -o \
    -name "*.js" -o \
    -name "*.java" -o \
    -name "*.c" -o \
    -name "*.cpp" -o \
    -name "*.h" -o \
    -name "*.go" -o \
    -name "*.rs" -o \
    -name "*.sh" -o \
    -name "*.yml" -o \
    -name "*.yaml" -o \
    -name "*.json" -o \
    -name "*.toml" -o \
    -name "*.xml" -o \
    -name "*.html" -o \
    -name "*.css" \
\) -not -path "*/.*" -not -path "*/node_modules/*" -not -path "*/__pycache__/*" 2>/dev/null | while read -r file; do
    echo "--- Archivo: $(basename "$file") ---" >> "$TEMP_FILE"
    cat "$file" 2>/dev/null >> "$TEMP_FILE"
    echo "" >> "$TEMP_FILE"
    FILE_COUNT=$((FILE_COUNT + 1))
done

echo "✅ Archivos procesados: $FILE_COUNT"
echo "✅ Texto combinado guardado: $(basename "$TEMP_FILE")"
echo "📊 Líneas: $(wc -l < "$TEMP_FILE" 2>/dev/null || echo "0")"

# 4. Analizar el texto combinado
echo ""
echo "🔍 ANALIZANDO CONTENIDO..."

if [ -f "$TEMP_FILE" ] && [ $(wc -l < "$TEMP_FILE" 2>/dev/null || echo "0") -gt 10 ]; then
    # Usar el alias 'analizar' si existe, o el script completo
    if command -v analizar &> /dev/null; then
        analizar "$TEMP_FILE"
    else
        python3 ~/proyectos/nlp/analisis_completo_v6.4.py "$TEMP_FILE"
    fi
else
    echo "❌ El archivo combinado está vacío o no tiene contenido suficiente."
    echo "💡 El repositorio puede no tener archivos de texto relevantes."
fi

echo ""
echo "✅ Análisis completado"
echo "📁 Archivos generados:"
ls -lh "$OUTPUT_DIR"/*_analisis* 2>/dev/null || echo "  (ninguno)"
