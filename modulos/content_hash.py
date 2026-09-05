#!/data/data/com.termux/files/usr/bin/python3
"""
Generación de hash para detección de cambios en contenido.
"""

import hashlib
import json
from typing import Dict, Any, Optional


def generar_content_hash(
    contenido: str,
    source_url: str = '',
    parametros: Optional[Dict[str, Any]] = None
) -> str:
    """
    Genera hash SHA-256 para detectar cambios en contenido.
    
    Args:
        contenido: Texto o transcripción completa
        source_url: URL de origen
        parametros: Parámetros de análisis (nicho, modo, etc.)
        
    Returns:
        Hash SHA-256 hexadecimal
    """
    datos = {
        'contenido': contenido,
        'source_url': source_url,
        'parametros': parametros or {}
    }
    
    # Serializar de forma estable
    serializado = json.dumps(datos, sort_keys=True, ensure_ascii=False)
    
    return hashlib.sha256(serializado.encode('utf-8')).hexdigest()


def verificar_cambio(
    content_id: str,
    contenido: str,
    hash_anterior: str,
    source_url: str = ''
) -> bool:
    """
    Verifica si el contenido cambió comparando hashes.
    
    Returns:
        True si el contenido cambió
    """
    hash_actual = generar_content_hash(contenido, source_url)
    return hash_actual != hash_anterior
