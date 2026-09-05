#!/data/data/com.termux/files/usr/bin/python3
"""
Grounding de entidades: trazabilidad completa de menciones.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class Grounding:
    """Información de grounding para una entidad."""
    documento: str
    fragmento: str
    posicion: Optional[int] = None
    confianza: float = 0.0


def agregar_grounding(
    entidad: Dict,
    documento: str,
    fragmento: str,
    posicion: Optional[int] = None,
    confianza: float = 0.0
) -> Dict:
    """
    Agrega grounding a una entidad.
    
    Args:
        entidad: Diccionario de entidad existente
        documento: Documento o video ID
        fragmento: Fragmento donde aparece
        posicion: Posición en el documento
        confianza: Score de confianza (0-1)
        
    Returns:
        Entidad con grounding
    """
    if 'grounding' not in entidad:
        entidad['grounding'] = []
    
    entidad['grounding'].append({
        'documento': documento,
        'fragmento': fragmento,
        'posicion': posicion,
        'confianza': confianza
    })
    
    return entidad


def fusionar_groundings(
    entidad1: Dict,
    entidad2: Dict
) -> Dict:
    """
    Fusiona groundings de dos entidades iguales.
    """
    fusionada = entidad1.copy()
    
    if 'grounding' in entidad2:
        if 'grounding' not in fusionada:
            fusionada['grounding'] = []
        fusionada['grounding'].extend(entidad2['grounding'])
    
    return fusionada
