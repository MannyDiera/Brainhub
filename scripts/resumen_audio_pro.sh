#!/bin/bash
# ==============================================
# RESUMEN CON AUDIO - DEFINITIVO (NOMBRE CORREGIDO)
# Uso: ./resumen_audio_pro.sh Transcript.txt
# ==============================================

ARCHIVO="$1"

if [ ! -f "$ARCHIVO" ]; then
    echo "❌ Uso: ./resumen_audio_pro.sh Transcript.txt"
    exit 1
fi

AUDIO_DIR="/sdcard/Download"

# Verificar dependencias
if ! command -v espeak-ng &> /dev/null; then
    echo "📦 Instalando espeak-ng..."
    pkg install espeak-ng -y
fi

if ! command -v ffmpeg &> /dev/null; then
    echo "📦 Instalando ffmpeg..."
    pkg install ffmpeg -y
fi

echo "📝 Generando resumen..."
RESUMEN_TXT="$AUDIO_DIR/resumen_temp.txt"
AUDIO_WAV="$AUDIO_DIR/resumen_temp.wav"
# CORREGIDO: eliminar .txt del nombre
BASE_NAME=$(basename "$ARCHIVO" .txt)
AUDIO_MP3="$AUDIO_DIR/${BASE_NAME}_resumen_pro.mp3"

# Generar el resumen usando resumen.sh
~/resumen.sh "$ARCHIVO" > "$RESUMEN_TXT"

echo "🎙️ Generando audio (esto puede tomar unos segundos)..."

# Generar WAV con espeak-ng
espeak-ng -v es \
    -f "$RESUMEN_TXT" \
    -w "$AUDIO_WAV" \
    -s 135 2>/dev/null

# Verificar que se creó el WAV
if [ ! -f "$AUDIO_WAV" ] || [ ! -s "$AUDIO_WAV" ]; then
    echo "❌ Error: No se pudo generar el archivo WAV"
    exit 1
fi

echo "🔊 Convirtiendo a MP3..."
ffmpeg -i "$AUDIO_WAV" \
    -af "loudnorm=I=-16:LRA=11:TP=-0.8" \
    -ar 44100 \
    -b:a 192k \
    -y "$AUDIO_MP3" 2>/dev/null

# Limpiar temporales
rm -f "$AUDIO_WAV" "$RESUMEN_TXT"

if [ ! -f "$AUDIO_MP3" ]; then
    echo "❌ Error: No se pudo crear el MP3"
    exit 1
fi

# Obtener duración
DURACION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$AUDIO_MP3" 2>/dev/null | cut -d. -f1)
TAMANIO=$(du -h "$AUDIO_MP3" 2>/dev/null | cut -f1)

echo ""
echo "✅ AUDIO GENERADO:"
echo "   📁 Archivo: $AUDIO_MP3"
if [ -n "$DURACION" ] && [ "$DURACION" != "0" ]; then
    echo "   ⏱️  Duración: ${DURACION}s (~$((DURACION / 60))m $((DURACION % 60))s)"
fi
echo "   📊 Tamaño: $TAMANIO"
echo "   🔧 Velocidad: 0.9x (135 ppm)"
echo "   🔊 Volumen: Normalizado (-0.8 dB TP)"
echo ""
echo "✅ ¡Archivo creado!"
