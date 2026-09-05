#!/data/data/com.termux/files/usr/bin/python3
"""
Integra extracción de relaciones con el pipeline NLP existente.
"""

import sys
import json
from pathlib import Path

PROJECT_DIR = Path(__file__).parent
sys.path.insert(0, str(PROJECT_DIR))

from modulos.relaciones import RelacionesManager, IntegradorRelaciones


def procesar_contenido(content_data: dict) -> dict:
    """Procesa contenido y extrae relaciones."""
    
    manager = RelacionesManager()
    segmentos = content_data.get('segmentos', [])
    relaciones = manager.extraer_de_segmentos(segmentos)
    entidades = content_data.get('entidades', [])
    
    return {
        'content_id': content_data.get('content_id', ''),
        'relaciones': relaciones,
        'entidades': entidades,
        'cypher': manager.exportar_cypher(relaciones, entidades),
        'gexf': manager.exportar_gexf(relaciones, entidades),
        'json_grafo': manager.exportar_json_grafo(relaciones, entidades)
    }


def main():
    """Prueba de integración."""
    
    content_test = {
        'content_id': 'test_grafo',
        'segmentos': [
            {
                'texto': 'Python usa PyTorch para machine learning',
                'entidades': ['Python', 'PyTorch', 'machine learning']
            },
            {
                'texto': 'El modelo mejora la precisión',
                'entidades': ['modelo', 'precisión']
            }
        ],
        'entidades': [
            {'nombre': 'Python', 'tipo': 'lenguaje'},
            {'nombre': 'PyTorch', 'tipo': 'framework'},
            {'nombre': 'machine learning', 'tipo': 'tecnologia'}
        ]
    }
    
    resultado = procesar_contenido(content_test)
    
    print(f"✅ Relaciones: {len(resultado['relaciones'])}")
    print(f"📝 Cypher: {len(resultado['cypher'])} caracteres")
    print(f"📊 GEXF: {len(resultado['gexf'])} caracteres")
    print(f"🗂️ JSON grafo: {len(resultado['json_grafo']['nodos'])} nodos")


if __name__ == '__main__':
    main()
