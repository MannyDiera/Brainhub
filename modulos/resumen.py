#!/usr/bin/env python3
"""
Módulo para generar resúmenes 80/20 desde archivos JSON de análisis.
Uso: from modulos.resumen import extraer_resumen, resumen_a_texto
"""

import json
import os

def cargar_analisis(ruta_json):
    """Carga un archivo JSON de análisis."""
    if not os.path.exists(ruta_json):
        raise FileNotFoundError(f"❌ Archivo no encontrado: {ruta_json}")
    
    with open(ruta_json, 'r', encoding='utf-8') as f:
        return json.load(f)

def extraer_terminos_clave(datos, top_n=10):
    """Extrae los términos clave más frecuentes."""
    return datos.get('terminos_clave', [])[:top_n]

def extraer_preguntas(datos, top_n=5):
    """Extrae las preguntas clave."""
    return datos.get('preguntas', [])[:top_n]

def extraer_oportunidades(datos, top_n=5):
    """Extrae las oportunidades detectadas."""
    return datos.get('oportunidades', [])[:top_n]

def extraer_definiciones(datos, top_n=5):
    """Extrae las definiciones clave."""
    return datos.get('definiciones', [])[:top_n]

def extraer_conceptos(datos, top_n=5):
    """Extrae los conceptos dominantes."""
    return datos.get('conceptos', [])[:top_n]

def extraer_sentimiento(datos):
    """Extrae el análisis de sentimiento."""
    return datos.get('sentimiento_global', {})

def extraer_resumen_completo(ruta_json):
    """Extrae todas las secciones del resumen en un diccionario."""
    datos = cargar_analisis(ruta_json)
    
    return {
        'terminos_clave': extraer_terminos_clave(datos),
        'preguntas': extraer_preguntas(datos),
        'oportunidades': extraer_oportunidades(datos),
        'definiciones': extraer_definiciones(datos),
        'conceptos': extraer_conceptos(datos),
        'sentimiento': extraer_sentimiento(datos)
    }

def resumen_a_texto(resumen, link=None):
    """Convierte un resumen (diccionario) a texto formateado."""
    lineas = []
    
    lineas.append("📌 TÉRMINOS CLAVE:")
    for term, freq in resumen.get('terminos_clave', []):
        lineas.append(f"  {term}: {freq}")
    
    lineas.append("\n❓ PREGUNTAS CLAVE:")
    for q in resumen.get('preguntas', []):
        lineas.append(f"  {q}")
    
    lineas.append("\n🎯 OPORTUNIDADES:")
    for o in resumen.get('oportunidades', []):
        lineas.append(f"  {o}")
    
    lineas.append("\n📖 DEFINICIONES:")
    for d in resumen.get('definiciones', []):
        lineas.append(f"  {d}")
    
    lineas.append("\n🔍 CONCEPTOS DOMINANTES:")
    for concepto, freq in resumen.get('conceptos', []):
        lineas.append(f"  {concepto}: {freq}")
    
    sent = resumen.get('sentimiento', {})
    if sent:
        lineas.append("\n😊 SENTIMIENTO:")
        lineas.append(f"  Polaridad: {sent.get('polaridad', 0)}")
        lineas.append(f"  Subjetividad: {sent.get('subjetividad', 0)}")
    
    if link:
        lineas.append(f"\n🔗 VIDEO ORIGINAL:\n{link}")
    
    return '\n'.join(lineas)

if __name__ == "__main__":
    # Test rápido
    import sys
    if len(sys.argv) > 1:
        resumen = extraer_resumen_completo(sys.argv[1])
        print(resumen_a_texto(resumen))
