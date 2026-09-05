#!/data/data/com.termux/files/usr/bin/python3
"""
Detección automática del modo de hablantes según contenido.
"""

import re
from typing import List, Optional


def detectar_modo_automatico(texto: str) -> str:
    """
    Detecta el modo adecuado según características del contenido.
    
    Returns:
        'tutorial', 'ateneo', 'legal', o 'auto'
    """
    # 1. Detectar términos legales
    terminos_legales = [
        'expediente', 'juzgado', 'fiscal', 'demandante', 'demandado',
        'testimonio', 'declaración', 'declaracion', 'ley', 'artículo',
        'articulo', 'inciso', 'jurisprudencia', 'fallo', 'sentencia'
    ]
    texto_lower = texto.lower()
    
    if any(termino in texto_lower for termino in terminos_legales):
        return 'legal'
    
    # 2. Detectar múltiples hablantes
    patrones_hablante = [
        r'\b(Dr\.?|Dra\.?|Médico|Medico|Especialista)\s+[A-ZÁÉÍÓÚ]',
        r'\b(Moderador|Expositor|Panelista)\s*:',
        r'\b(Pregunta|Respuesta)\s*:'
    ]
    
    n_menciones = 0
    for patron in patrones_hablante:
        n_menciones += len(re.findall(patron, texto, re.IGNORECASE))
    
    if n_menciones > 5:
        return 'ateneo'
    
    # 3. Detectar tutorial (baja densidad de hablantes)
    n_segmentos = len(texto.split('\n'))
    if n_menciones <= 1 and n_segmentos > 20:
        return 'tutorial'
    
    return 'auto'
