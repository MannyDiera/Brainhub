#!/bin/bash
# ==============================================
# SCRIPT MAESTRO DE APRENDIZAJE V2
# Con soporte para archivos de análisis faltantes y alias legibles
# ==============================================

DB="/sdcard/Download/analisis_consolidado.duckdb"
CONTENIDO=""
BASE="/sdcard/Download"
ALIAS_FILE="/data/data/com.termux/files/home/proyectos/nlp/alias_contenidos.csv"
SCRIPT_ANALISIS="/data/data/com.termux/files/home/proyectos/nlp/analisis_completo_v6.4.py"

# Colores
ROJO='\033[0;31m'
VERDE='\033[0;32m'
AMARILLO='\033[1;33m'
AZUL='\033[0;34m'
NC='\033[0m'

# ==============================================
# FUNCIONES
# ==============================================

mostrar_progreso() {
    echo -e "\n${AZUL}📊 PROGRESO ACTUAL${NC}"
    echo "=========================="
    ~/progreso.sh
}

get_nombre_legible() {
    local video="$1"
    if [ -f "$ALIAS_FILE" ]; then
        grep "^$video," "$ALIAS_FILE" | cut -d',' -f2 | head -1
    fi
}

get_link() {
    local video="$1"
    if [ -f "$ALIAS_FILE" ]; then
        grep "^$video," "$ALIAS_FILE" | cut -d',' -f3 | head -1
    fi
}

validar_archivos() {
    local video="$1"
    local nombre_base="$video"
    
    # Lista de posibles nombres de archivo
    posibles_txt=(
        "$BASE/${video}.txt"
        "$BASE/Transcript_${video}.txt"
        "$BASE/${video}.EN_FORZADO.txt"
        "$BASE/${video}_analisis.txt"
    )
    
    posibles_analisis=(
        "$BASE/${video}_analisis.txt"
        "$BASE/Transcript_${video}_analisis.txt"
        "$BASE/${video}_analisis_completo.txt"
        "$BASE/${video}_analisis_completo.json"
    )
    
    posibles_audio=(
        "$BASE/${video}_analisis_resumen_pro.mp3"
        "$BASE/Transcript_${video}_analisis_resumen_pro.mp3"
    )
    
    # Buscar archivos
    TXT=""
    ANALISIS=""
    AUDIO=""
    
    for f in "${posibles_txt[@]}"; do
        if [ -f "$f" ]; then
            TXT="$f"
            break
        fi
    done
    
    for f in "${posibles_analisis[@]}"; do
        if [ -f "$f" ]; then
            ANALISIS="$f"
            break
        fi
    done
    
    for f in "${posibles_audio[@]}"; do
        if [ -f "$f" ]; then
            AUDIO="$f"
            break
        fi
    done
    
    # Si no se encuentra el análisis, ofrecer generarlo
    if [ -z "$ANALISIS" ] && [ -f "$TXT" ]; then
        ANALISIS_FALTANTE="✅ (se puede generar)"
    else
        ANALISIS_FALTANTE=""
    fi
    
    # Mostrar disponibilidad
    echo -e "\n${AZUL}📁 ARCHIVOS DISPONIBLES${NC}"
    echo "=========================="
    
    if [ -n "$TXT" ]; then
        echo "  📄 Transcripción: ✅ $(basename "$TXT")"
        RUTA_TXT="$TXT"
    else
        echo "  📄 Transcripción: ❌"
        RUTA_TXT=""
    fi
    
    if [ -n "$ANALISIS" ]; then
        echo "  📊 Análisis: ✅ $(basename "$ANALISIS")"
        RUTA_ANALISIS="$ANALISIS"
    elif [ -n "$ANALISIS_FALTANTE" ]; then
        echo "  📊 Análisis: ⚠️  $ANALISIS_FALTANTE"
        RUTA_ANALISIS=""
    else
        echo "  📊 Análisis: ❌"
        RUTA_ANALISIS=""
    fi
    
    if [ -n "$AUDIO" ]; then
        echo "  🎧 Audio: ✅ $(basename "$AUDIO")"
        RUTA_AUDIO="$AUDIO"
    else
        echo "  🎧 Audio: ❌"
        RUTA_AUDIO=""
    fi
    
    echo ""
    
    if [ -n "$TXT" ]; then
        return 0
    else
        return 1
    fi
}

seleccionar_contenido() {
    echo -e "\n${AZUL}🎯 SELECCIONAR CONTENIDO${NC}"
    echo "=========================="
    
    PRIMERO=$(duckdb "$DB" -csv -noheader -c "
    SELECT t.video FROM terminos_raw t
    JOIN progreso p ON t.video = p.video
    WHERE p.estado = 'pendiente'
    GROUP BY t.video
    ORDER BY SUM(t.frequency) DESC
    LIMIT 1;
    " 2>/dev/null | head -1 | tr -d '\r')
    
    if [ -z "$PRIMERO" ]; then
        echo "🎉 ¡FELICITACIONES! No tenés contenidos pendientes."
        exit 0
    fi
    
    NOMBRE_LEGIBLE=$(get_nombre_legible "$PRIMERO")
    if [ -n "$NOMBRE_LEGIBLE" ]; then
        echo "📌 Contenido sugerido: $NOMBRE_LEGIBLE"
        echo "   🆔 ID: $PRIMERO"
    else
        echo "📌 Contenido sugerido: $PRIMERO"
    fi
    
    validar_archivos "$PRIMERO"
    
    echo ""
    echo "Opciones:"
    echo "  1. Usar el contenido sugerido"
    echo "  2. Elegir otro contenido"
    echo "  3. Volver al menú principal"
    echo ""
    read -p "Elegí una opción (1-3): " OPCION
    
    case $OPCION in
        1)
            CONTENIDO="$PRIMERO"
            ;;
        2)
            echo -e "\n${AZUL}📋 CONTENIDOS PENDIENTES${NC}"
            echo "=========================="
            
            duckdb "$DB" -c "
            SELECT 
                COALESCE(a.nombre_amigable, t.video) as nombre,
                t.video as id,
                SUM(t.frequency) as menciones
            FROM terminos_raw t
            JOIN progreso p ON t.video = p.video
            LEFT JOIN alias a ON t.video = a.video
            WHERE p.estado = 'pendiente'
            GROUP BY t.video, a.nombre_amigable
            ORDER BY SUM(t.frequency) DESC
            LIMIT 15;
            "
            
            echo ""
            read -p "Escribí el nombre parcial (ej. Git, PyTorch, OSINT): " BUSQUEDA
            
            SELECCIONADO=$(duckdb "$DB" -csv -noheader -c "
            SELECT t.video FROM terminos_raw t
            JOIN progreso p ON t.video = p.video
            LEFT JOIN alias a ON t.video = a.video
            WHERE p.estado = 'pendiente'
            AND (t.video LIKE '%$BUSQUEDA%' OR a.nombre_amigable LIKE '%$BUSQUEDA%')
            GROUP BY t.video
            ORDER BY SUM(t.frequency) DESC
            LIMIT 1;
            " 2>/dev/null | head -1 | tr -d '\r')
            
            if [ -z "$SELECCIONADO" ]; then
                echo "❌ No se encontró contenido con '$BUSQUEDA'"
                CONTENIDO="$PRIMERO"
            else
                CONTENIDO="$SELECCIONADO"
                validar_archivos "$CONTENIDO"
            fi
            ;;
        3)
            return
            ;;
        *)
            echo "❌ Opción inválida. Usando contenido sugerido."
            CONTENIDO="$PRIMERO"
            ;;
    esac
    
    NOMBRE_LEGIBLE=$(get_nombre_legible "$CONTENIDO")
    LINK=$(get_link "$CONTENIDO")
    
    echo -e "\n✅ Contenido seleccionado: $NOMBRE_LEGIBLE ($CONTENIDO)"
    if [ -n "$LINK" ]; then
        echo "🔗 Link: $LINK"
    fi
}

mostrar_opciones_estudio() {
    local video="$1"
    validar_archivos "$video"
    
    NOMBRE_LEGIBLE=$(get_nombre_legible "$video")
    LINK=$(get_link "$video")
    
    echo -e "\n${AZUL}📚 OPCIONES DE ESTUDIO${NC}"
    echo "=========================="
    if [ -n "$NOMBRE_LEGIBLE" ]; then
        echo "📌 $NOMBRE_LEGIBLE"
        if [ -n "$LINK" ]; then
            echo "🔗 $LINK"
        fi
        echo "🆔 $video"
    else
        echo "📌 $video"
    fi
    echo ""
    
    echo "  1. 📖 Ver resumen 80/20"
    if [ -f "$RUTA_ANALISIS" ]; then
        echo "     ✅ Disponible"
    else
        echo "     ❌ Faltante"
    fi
    
    echo "  2. 🎧 Escuchar audio del resumen"
    if [ -f "$RUTA_AUDIO" ]; then
        echo "     ✅ Disponible"
    else
        echo "     ❌ Faltante"
    fi
    
    echo "  3. 📄 Ver transcripción completa (less)"
    if [ -f "$RUTA_TXT" ]; then
        echo "     ✅ Disponible"
    else
        echo "     ❌ Faltante"
    fi
    
    echo "  4. 🔍 Buscar término en transcripción"
    if [ -f "$RUTA_TXT" ]; then
        echo "     ✅ Disponible"
    else
        echo "     ❌ Faltante (sin transcripción)"
    fi
    
    echo "  5. 📊 Ver progreso general"
    echo "  6. ✅ Marcar como completado"
    echo "  7. 🔄 Seleccionar otro contenido"
    echo "  8. 🚪 Salir"
    echo "  9. 🔗 Abrir link (si tiene)"
    echo "  0. ⚙️  Generar análisis faltante (si hay transcripción)"
    echo ""
    read -p "Elegí una opción (0-9): " OPCION
    
    case $OPCION in
        1)
            if [ -f "$RUTA_ANALISIS" ]; then
                echo -e "\n${AZUL}📖 RESUMEN 80/20${NC}"
                echo "=========================="
                ~/resumen_rapido.sh "$RUTA_ANALISIS" "$LINK"
                echo ""
                read -p "Presioná Enter para volver..."
            else
                echo "❌ No hay análisis disponible para este contenido."
                read -p "Presioná Enter para volver..."
            fi
            ;;
        2)
            if [ -f "$RUTA_AUDIO" ]; then
                echo -e "\n${AZUL}🎧 AUDIO DEL RESUMEN${NC}"
                echo "=========================="
                mpv "$RUTA_AUDIO"
                read -p "Presioná Enter para volver..."
            else
                echo "❌ No hay audio disponible para este contenido."
                read -p "Presioná Enter para volver..."
            fi
            ;;
        3)
            if [ -f "$RUTA_TXT" ]; then
                echo -e "\n${AZUL}📄 TRANSCRIPCIÓN COMPLETA${NC}"
                echo "=========================="
                echo "💡 Dentro de less: Espacio=avanzar, b=retroceder, /buscar, q=salir"
                echo ""
                read -p "Presioná Enter para abrir..."
                less "$RUTA_TXT"
            else
                echo "❌ No hay transcripción disponible para este contenido."
                read -p "Presioná Enter para volver..."
            fi
            ;;
        4)
            if [ -f "$RUTA_TXT" ]; then
                echo -e "\n${AZUL}🔍 BUSCAR EN TRANSCRIPCIÓN${NC}"
                echo "=========================="
                read -p "Término a buscar: " TERMINO
                echo ""
                grep -i "$TERMINO" "$RUTA_TXT" | head -20
                echo ""
                read -p "Presioná Enter para volver..."
            else
                echo "❌ No hay transcripción disponible para este contenido."
                read -p "Presioná Enter para volver..."
            fi
            ;;
        5)
            mostrar_progreso
            read -p "Presioná Enter para volver..."
            ;;
        6)
            echo -e "\n${AZUL}✅ MARCAR COMO COMPLETADO${NC}"
            echo "=========================="
            ~/completar.sh "$video"
            echo ""
            read -p "Presioná Enter para volver..."
            CONTENIDO=""
            ;;
        7)
            CONTENIDO=""
            seleccionar_contenido
            ;;
        8)
            echo -e "\n${VERDE}¡Seguí aprendiendo! 🚀${NC}"
            exit 0
            ;;
        9)
            if [ -n "$LINK" ]; then
                echo -e "\n🔗 Abriendo link: $LINK"
                termux-open "$LINK" 2>/dev/null || echo "📋 Copiá el link: $LINK"
            else
                echo "❌ No hay link disponible para este contenido."
            fi
            read -p "Presioná Enter para volver..."
            ;;
        0)
            if [ -f "$RUTA_TXT" ]; then
                echo -e "\n${AZUL}⚙️  GENERANDO ANÁLISIS FALTANTE${NC}"
                echo "=========================="
                echo "📊 Analizando: $(basename "$RUTA_TXT")"
                
                if [ -f "$SCRIPT_ANALISIS" ]; then
                    python3 "$SCRIPT_ANALISIS" "$RUTA_TXT"
                    echo "✅ Análisis generado. Volvé a seleccionar el contenido."
                else
                    echo "❌ Script de análisis no encontrado: $SCRIPT_ANALISIS"
                fi
            else
                echo "❌ No hay transcripción para analizar."
            fi
            read -p "Presioná Enter para volver..."
            ;;
        *)
            echo "❌ Opción inválida."
            read -p "Presioná Enter para volver..."
            ;;
    esac
}

# ==============================================
# PROGRAMA PRINCIPAL
# ==============================================

clear
echo -e "${VERDE}==========================================${NC}"
echo -e "${VERDE}   🚀 SCRIPT MAESTRO DE APRENDIZAJE V2${NC}"
echo -e "${VERDE}==========================================${NC}"

while true; do
    mostrar_progreso
    
    if [ -z "$CONTENIDO" ]; then
        seleccionar_contenido
        if [ -z "$CONTENIDO" ]; then
            echo "👋 ¡Hasta luego!"
            exit 0
        fi
    fi
    
    mostrar_opciones_estudio "$CONTENIDO"
done
