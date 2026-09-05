#!/bin/bash
# ==============================================
# VER CONTENIDO CON ALIAS
# Uso: ./ver_contenido.sh ID_del_video
# ==============================================

VIDEO="$1"
ALIAS_FILE="/data/data/com.termux/files/home/proyectos/nlp/alias_contenidos.csv"

if [ -z "$VIDEO" ]; then
    echo "❌ Uso: ./ver_contenido.sh ID_del_video"
    echo ""
    echo "📋 Contenidos disponibles:"
    cat "$ALIAS_FILE" | column -t -s ','
    exit 1
fi

# Buscar el video en el archivo de alias
INFO=$(grep "^$VIDEO," "$ALIAS_FILE" 2>/dev/null)

if [ -z "$INFO" ]; then
    echo "❌ No se encontró alias para: $VIDEO"
    echo ""
    echo "📋 Contenidos disponibles:"
    cat "$ALIAS_FILE" | column -t -s ',' | head -10
    exit 1
fi

# Extraer campos
NOMBRE=$(echo "$INFO" | cut -d',' -f2)
LINK=$(echo "$INFO" | cut -d',' -f3)
NICHO=$(echo "$INFO" | cut -d',' -f4)
DESCRIPCION=$(echo "$INFO" | cut -d',' -f5)

echo "📹 CONTENIDO"
echo "========================================="
echo "🔍 ID: $VIDEO"
echo "📌 Nombre: $NOMBRE"
echo "🔗 Link: $LINK"
echo "📂 Nicho: $NICHO"
echo "📝 Descripción: $DESCRIPCION"
echo ""
echo "📁 Archivos asociados:"
ls -lh /sdcard/Download/Transcript_${VIDEO}*.* 2>/dev/null | head -5

echo ""
echo "📊 Análisis:"
if [ -f "/sdcard/Download/Transcript_${VIDEO}_resumen.txt" ]; then
    echo "  ✅ Resumen disponible"
    grep -A 3 "📌 Términos clave" "/sdcard/Download/Transcript_${VIDEO}_resumen.txt" | head -5
else
    echo "  ⚠️ Resumen no encontrado"
fi
