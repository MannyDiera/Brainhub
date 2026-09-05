#!/data/data/com.termux/files/usr/bin/python3
"""
Configuración de modos para DetectorHablantes.
Separado para evitar hardcodear en el detector.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class ConfiguracionModo:
    """Configuración para cada modo de detección."""
    max_hablantes: int
    umbral_segmentos: float
    detectar_roles: bool = False
    anonimizar: bool = False
    ignorar_menciones: bool = True


def obtener_modos() -> Dict[str, ConfiguracionModo]:
    """Retorna diccionario de modos configurados."""
    return {
        'tutorial': ConfiguracionModo(
            max_hablantes=1,
            umbral_segmentos=0.05,
            detectar_roles=False,
            anonimizar=False,
            ignorar_menciones=True
        ),
        'ateneo': ConfiguracionModo(
            max_hablantes=10,
            umbral_segmentos=0.02,
            detectar_roles=True,
            anonimizar=False,
            ignorar_menciones=False
        ),
        'legal': ConfiguracionModo(
            max_hablantes=20,
            umbral_segmentos=0.01,
            detectar_roles=True,
            anonimizar=True,
            ignorar_menciones=False
        ),
        'auto': ConfiguracionModo(
            max_hablantes=10,
            umbral_segmentos=0.03,
            detectar_roles=True,
            anonimizar=False,
            ignorar_menciones=False
        )
    }
