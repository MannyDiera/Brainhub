#!/data/data/com.termux/files/usr/bin/python3
"""
Self-RAG simple para BrainHub.
Evalúa si hay suficiente evidencia antes de responder.
Sin LLMs: usa scoring de BM25 como señal de confianza.
"""

from typing import Dict, List, Optional


class SelfRAG:
    """RAG con auto-evaluación de evidencia."""
    
    UMBRAL_CONFIANZA = 0.3
    
    def __init__(self, rag_engine=None):
        self.rag = rag_engine
        self.historial = []
    
    def buscar_con_reflexion(self, consulta: str, top_k: int = 3) -> Dict:
        """
        Busca con auto-evaluación.
        
        Returns:
            {'respuesta': [...], 'confianza': float, 'accion': 'responder|ampliar|declinar'}
        """
        if not self.rag:
            return {'respuesta': [], 'confianza': 0, 'accion': 'sin_rag'}
        
        # 1. Buscar inicial
        resultados = self.rag.buscar(consulta, top_k)
        
        if not resultados:
            return {
                'respuesta': [],
                'confianza': 0,
                'accion': 'ampliar',
                'mensaje': 'Sin resultados. Ampliar búsqueda.'
            }
        
        # 2. Evaluar confianza
        mejor_score = resultados[0]['score']
        confianza = min(mejor_score / 10, 1.0)
        
        # 3. Decidir acción
        if confianza >= self.UMBRAL_CONFIANZA:
            accion = 'responder'
            mensaje = f'Evidencia suficiente (confianza: {confianza:.2f})'
        elif confianza >= 0.1:
            accion = 'ampliar'
            mensaje = f'Evidencia débil. Buscar más contexto.'
        else:
            accion = 'declinar'
            mensaje = 'Evidencia insuficiente para responder.'
        
        self.historial.append({
            'consulta': consulta,
            'confianza': confianza,
            'accion': accion
        })
        
        return {
            'respuesta': resultados,
            'confianza': round(confianza, 2),
            'accion': accion,
            'mensaje': mensaje
        }
    
    def ampliar_busqueda(self, consulta: str, top_k: int = 10) -> List[Dict]:
        """Amplía búsqueda cuando la evidencia es débil."""
        return self.rag.buscar(consulta, top_k)
    
    def obtener_historial(self) -> List[Dict]:
        """Retorna historial de reflexiones."""
        return self.historial


if __name__ == '__main__':
    from modulos.rag_simple import RAGSimple
    
    # Crear RAG simple
    rag = RAGSimple()
    documentos = [
        "RAG retrieval augmented generation vector database",
        "machine learning deep learning neural networks",
        "retrieval query vector index evidence",
        "python programacion codigo datos",
        "salud paciente diagnostico tratamiento"
    ]
    rag.indexar(documentos)
    
    # Crear Self-RAG
    self_rag = SelfRAG(rag)
    
    print("🧠 SELF-RAG TEST")
    print("=" * 50)
    
    # Test 1: consulta con evidencia
    resultado = self_rag.buscar_con_reflexion('retrieval vector')
    print(f"\nConsulta: 'retrieval vector'")
    print(f"   Acción: {resultado['accion']}")
    print(f"   Confianza: {resultado['confianza']}")
    print(f"   {resultado['mensaje']}")
    
    # Test 2: consulta sin evidencia
    resultado = self_rag.buscar_con_reflexion('blockchain quantum')
    print(f"\nConsulta: 'blockchain quantum'")
    print(f"   Acción: {resultado['accion']}")
    print(f"   Confianza: {resultado['confianza']}")
    print(f"   {resultado['mensaje']}")
    
    print(f"\n📊 Historial: {len(self_rag.obtener_historial())} consultas")
