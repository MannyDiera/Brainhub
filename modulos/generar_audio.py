#!/usr/bin/env python3
"""
Módulo opcional para generar audio desde un análisis JSON.
Usa stopwords para filtrar términos y decidir si vale la pena.
"""

import os
import json
import subprocess
from pathlib import Path

# Importar gestor de stopwords
try:
    from .stopwords_manager import get_stopwords
except ImportError:
    def get_stopwords(nicho='GENERAL', lang='es'):
        return set()

# Nichos que siempre generan audio
NICHOS_AUDIO_SIEMPRE = {
    'REFLEXIVO', 'SALUD', 'LEGAL', 'ENTREVISTA'
}

# Palabras clave que activan audio en nichos técnicos
PALABRAS_AUDIO_TECNICO = {
    'inteligencia', 'ética', 'presencia', 'futuro',
    'humano', 'memoria', 'identidad', 'impacto',
    'salud', 'seguridad', 'justicia', 'derechos'
}

def debe_generar_audio(nicho: str, terminos_clave: list, stopwords: set) -> bool:
    """
    Decide si el contenido merece audio.
    """
    # 1. Nichos que siempre generan audio
    if nicho in NICHOS_AUDIO_SIEMPRE:
        return True
    
    # 2. Nichos técnicos con palabras clave especiales
    if nicho == 'TECNOLOGIA':
        # Filtrar stopwords de los términos clave
        terminos_limpios = [t.lower() for t, f in terminos_clave 
                           if t.lower() not in stopwords]
        terminos_str = ' '.join(terminos_limpios)
        for palabra in PALABRAS_AUDIO_TECNICO:
            if palabra in terminos_str:
                return True
        return False
    
    # 3. Otros nichos: no generar audio por defecto
    return False

def extraer_texto_para_audio(datos: dict, nicho: str) -> str:
    """
    Genera un texto legible para el audio a partir del análisis,
    usando stopwords para filtrar.
    """
    # Obtener stopwords
    stopwords = get_stopwords(nicho, 'es')
    
    lineas = []
    
    # 1. Términos clave (filtrados)
    lineas.append("📌 TÉRMINOS CLAVE:")
    terminos_filtrados = []
    for term, freq in datos.get('terminos_clave', [])[:20]:
        term_limpio = term.lower().strip()
        if term_limpio not in stopwords and len(term_limpio) > 3:
            terminos_filtrados.append((term, freq))
    
    for term, freq in terminos_filtrados[:10]:
        lineas.append(f"{term}: {freq}")
    lineas.append("")
    
    # 2. Nicho y sentimiento
    sentimiento = datos.get('sentimiento_global', {})
    polaridad = sentimiento.get('polaridad', 0)
    
    lineas.append(f"Nicho: {nicho}")
    if polaridad > 0.1:
        lineas.append("Tono: Positivo")
    elif polaridad < -0.1:
        lineas.append("Tono: Negativo")
    else:
        lineas.append("Tono: Neutral")
    lineas.append("")
    
    # 3. Preguntas clave
    preguntas = datos.get('preguntas', [])
    if preguntas:
        lineas.append("❓ PREGUNTAS CLAVE:")
        for q in preguntas[:3]:
            lineas.append(f"{q}")
        lineas.append("")
    
    # 4. Conceptos dominantes
    conceptos = datos.get('conceptos', [])
    if conceptos:
        lineas.append("📊 CONCEPTOS DOMINANTES:")
        for concepto, freq in conceptos[:3]:
            lineas.append(f"{concepto}: {freq}")
    
    return '\n'.join(lineas)

def generar_audio_si_aplica(json_path: str) -> bool:
    """
    Genera audio solo si el contenido lo merece.
    Retorna True si se generó, False si no.
    """
    json_path = Path(json_path)
    
    if not json_path.exists():
        print(f"⚠️ JSON no encontrado: {json_path}")
        return False
    
    # Cargar JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    nicho = data.get('nicho', 'GENERAL')
    terminos_clave = data.get('terminos_clave', [])
    
    # Obtener stopwords para el nicho
    stopwords = get_stopwords(nicho, 'es')
    
    # Decidir si generar audio
    if not debe_generar_audio(nicho, terminos_clave, stopwords):
        print(f"⏭️ Audio no necesario para {nicho}")
        return False
    
    # Extraer texto para audio (con stopwords)
    texto = extraer_texto_para_audio(data, nicho)
    
    # Guardar temporalmente
    audio_text_path = json_path.with_name(f"{json_path.stem}_audio.txt")
    with open(audio_text_path, 'w', encoding='utf-8') as f:
        f.write(texto)
    
    # Generar audio
    try:
        audio_path = json_path.with_name(f"{json_path.stem}_resumen_pro.mp3")
        subprocess.run([
            'espeak-ng', '-v', 'spanish',
            '-f', str(audio_text_path),
            '-w', str(audio_path.with_suffix('.wav')),
            '-s', '135'
        ], check=True, capture_output=True)
        
        # Convertir a MP3 (si ffmpeg está disponible)
        subprocess.run([
            'ffmpeg', '-i', str(audio_path.with_suffix('.wav')),
            '-y', str(audio_path)
        ], check=True, capture_output=True)
        
        # Limpiar WAV
        audio_path.with_suffix('.wav').unlink()
        audio_text_path.unlink()
        
        print(f"🎧 Audio generado: {audio_path}")
        return True
        
    except Exception as e:
        print(f"⚠️ Error generando audio: {e}")
        return False

# ============================================================
# FUNCIÓN DE CONVENIENCIA
# ============================================================

def audio_desde_json(json_path: str) -> bool:
    """Función principal para usar desde scripts."""
    return generar_audio_si_aplica(json_path)

if __name__ == "__main__":
    # Test rápido
    import sys
    if len(sys.argv) > 1:
        generar_audio_si_aplica(sys.argv[1])
