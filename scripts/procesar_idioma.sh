#!/bin/bash
# ==============================================
# PROCESAR VIDEO EN CUALQUIER IDIOMA
# IDIOMA → INGLÉS → ESPAÑOL
# ==============================================

VIDEO_URL="$1"
SUB_LANG="$2"

if [ -z "$VIDEO_URL" ] || [ -z "$SUB_LANG" ]; then
    echo "❌ Uso: ./procesar_idioma.sh https://youtu.be/VIDEO_ID cs"
    echo "📋 Ejemplos: cs (checo), hi (hindi), th (tailandés)"
    exit 1
fi

VIDEO_ID=$(echo "$VIDEO_URL" | grep -oE '([a-zA-Z0-9_-]{11})' | head -1)

if [ -z "$VIDEO_ID" ]; then
    echo "❌ No se pudo extraer el ID de: $VIDEO_URL"
    exit 1
fi

echo "🔄 PROCESANDO VIDEO EN IDIOMA: $SUB_LANG"
echo "============================="
echo "🎯 ID: $VIDEO_ID"

# 1. Descargar subtítulos
echo ""
echo "📥 Descargando subtítulos en $SUB_LANG..."
yt-dlp \
    --write-auto-subs \
    --sub-langs "$SUB_LANG" \
    --skip-download \
    --output "/sdcard/Download/$VIDEO_ID.%(ext)s" \
    "$VIDEO_URL" 2>&1 | grep -v "WARNING"

# 2. Limpiar VTT
vtt_file=$(find /sdcard/Download -maxdepth 1 -name "*$VIDEO_ID*.vtt" -type f | head -1)

if [ ! -f "$vtt_file" ]; then
    echo "❌ No se encontró el archivo VTT"
    exit 1
fi

echo ""
echo "🧹 Limpiando VTT..."
TXT_ORIGINAL="/sdcard/Download/Transcript_${VIDEO_ID}_${SUB_LANG}_original.txt"

awk '
    /^[0-9][0-9]:[0-9][0-9]:/ { next }
    /^WEBVTT/ { next }
    /^Kind:/ { next }
    /^Language:/ { next }
    /^[[:space:]]*$/ { next }
    {
        gsub(/<[^>]*>/, "")
        gsub(/^.*position:0%/, "")
        gsub(/^[[:space:]]+/, "")
        if (length > 0) print
    }
' "$vtt_file" | awk '!seen[$0]++' > "$TXT_ORIGINAL"

echo "✅ Original guardado: $TXT_ORIGINAL"
echo "📊 Líneas: $(wc -l < "$TXT_ORIGINAL")"

# 3. Traducir: Idioma origen → Inglés → Español
echo ""
echo "🌐 Traduciendo $SUB_LANG → EN → ES..."
python3 ~/traducir_universal.py "$TXT_ORIGINAL" "$SUB_LANG"

# 4. Analizar la versión en español
ARCHIVO_ES="${TXT_ORIGINAL%.txt}_es.txt"
if [ -f "$ARCHIVO_ES" ]; then
    echo ""
    echo "🔍 Analizando versión en español..."
    ~/analizar.sh "$ARCHIVO_ES"
    
    echo ""
    echo "📋 Resumen 80/20:"
    ~/resumen_rapido.sh "${ARCHIVO_ES%.txt}_analisis.txt" "$VIDEO_URL"
else
    echo "❌ No se encontró la traducción al español"
fi

echo ""
echo "✅ Proceso completado"
echo "📁 Archivos generados:"
ls -lh /sdcard/Download/Transcript_${VIDEO_ID}_${SUB_LANG}*.* 2>/dev/null
