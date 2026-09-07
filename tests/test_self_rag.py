#!/data/data/com.termux/files/usr/bin/python3
"""Tests para self_rag."""
import sys
import os
import pytest

sys.path.insert(0, os.path.expanduser('~/proyectos/nlp'))
from modulos.self_rag import SelfRAG
from modulos.rag_simple import RAGSimple


@pytest.fixture
def rag_engine():
    rag = RAGSimple()
    docs = [
        "RAG retrieval augmented generation",
        "machine learning deep learning",
        "python programacion datos"
    ]
    rag.indexar(docs)
    return rag


@pytest.mark.unit
class TestSelfRAG:
    
    def test_buscar_con_evidencia(self, rag_engine):
        self_rag = SelfRAG(rag_engine)
        resultado = self_rag.buscar_con_reflexion('retrieval augmented')
        assert resultado['accion'] in ['responder', 'ampliar']
    
    def test_buscar_sin_evidencia(self, rag_engine):
        self_rag = SelfRAG(rag_engine)
        resultado = self_rag.buscar_con_reflexion('blockchain quantum')
        assert resultado['accion'] in ['ampliar', 'declinar']
    
    def test_historial(self, rag_engine):
        self_rag = SelfRAG(rag_engine)
        self_rag.buscar_con_reflexion('python')
        assert len(self_rag.obtener_historial()) == 1
