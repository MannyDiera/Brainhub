#!/data/data/com.termux/files/usr/bin/python3
"""Módulo de analogías como metadata de nodos para BrainHub."""

from typing import Dict, List, Optional
import json


class AnalogiasManager:
    """Gestiona analogías como metadata de nodos del grafo."""
    
    # Analogías como metadata de nodos
    NODOS_ANALOGIAS = {
        'lambda': {
            'tipo': 'concepto_python',
            'analogia': 'Cupón de descuento rápido',
            'explicacion': 'Regla simple de un solo uso que toma un valor y da resultado al instante',
            'ejemplo_codigo': 'lambda x: x * 0.9',
            'relaciones': ['funcion', 'expresion']
        },
        'decorator': {
            'tipo': 'concepto_python',
            'analogia': 'Ingredientes extra de una hamburguesa',
            'explicacion': 'Modifica el comportamiento sin cambiar la receta original',
            'ejemplo_codigo': '@decorator\ndef funcion(): pass',
            'relaciones': ['funcion', 'modificacion']
        },
        'generator': {
            'tipo': 'concepto_python',
            'analogia': 'Dispensador de turnos en banco',
            'explicacion': 'Genera un valor a la vez, ahorrando memoria',
            'ejemplo_codigo': 'def gen():\n    yield valor',
            'relaciones': ['iteracion', 'memoria']
        },
        'context_manager': {
            'tipo': 'concepto_python',
            'analogia': 'Alquilar cancha de fútbol 5',
            'explicacion': 'Abre y cierra recursos automáticamente',
            'ejemplo_codigo': 'with open(archivo) as f:\n    procesar(f)',
            'relaciones': ['recurso', 'limpieza']
        }
    }
    
    def enriquecer_nodo(self, termino: str) -> Dict:
        """
        Agrega metadata de analogía a un nodo del grafo.
        
        Args:
            termino: Nombre del término
            
        Returns:
            Dict con metadata del nodo si existe analogía
        """
        termino_norm = termino.lower().strip()
        
        if termino_norm in self.NODOS_ANALOGIAS:
            metadata = self.NODOS_ANALOGIAS[termino_norm].copy()
            metadata['termino'] = termino_norm
            return metadata
        
        return {'termino': termino_norm, 'tipo': 'general'}
    
    def enriquecer_grafo(self, ruta_json: str, ruta_salida: str = None):
        """
        Enriquece el JSON del grafo con analogías como metadata.
        
        Args:
            ruta_json: Ruta del grafo JSON
            ruta_salida: Ruta de salida (opcional)
        """
        with open(ruta_json, 'r', encoding='utf-8') as f:
            grafo = json.load(f)
        
        nodos_enriquecidos = []
        for nodo in grafo.get('nodos', []):
            termino = nodo.get('id', nodo.get('label', ''))
            metadata = self.enriquecer_nodo(termino)
            nodo['metadata'] = metadata
            nodos_enriquecidos.append(nodo)
        
        grafo['nodos'] = nodos_enriquecidos
        grafo['metadata'] = {
            'analogias_integradas': len(self.NODOS_ANALOGIAS)
        }
        
        if ruta_salida:
            with open(ruta_salida, 'w', encoding='utf-8') as f:
                json.dump(grafo, f, indent=2, ensure_ascii=False)
            print(f"✅ Grafo enriquecido guardado en: {ruta_salida}")
        
        return grafo
    
    def buscar_concepto(self, termino: str) -> Optional[Dict]:
        """Busca metadata de un concepto específico."""
        termino_norm = termino.lower().strip()
        
        for clave, metadata in self.NODOS_ANALOGIAS.items():
            if clave in termino_norm:
                return metadata
        
        return None


if __name__ == '__main__':
    manager = AnalogiasManager()
    
    print("📚 Metadata de nodos:")
    for termino, metadata in manager.NODOS_ANALOGIAS.items():
        print(f"\n   [{termino}]")
        print(f"   → {metadata['analogia']}")
        print(f"   → {metadata['explicacion']}")
        print(f"   → {metadata['ejemplo_codigo'][:40]}...")
        print(f"   → Relaciones: {', '.join(metadata['relaciones'])}")
    
    # Probar enriquecer un nodo
    print(f"\n🔍 Enriquecer 'lambda':")
    print(json.dumps(manager.enriquecer_nodo('lambda'), indent=2, ensure_ascii=False))
