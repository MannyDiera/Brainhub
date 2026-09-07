#!/data/data/com.termux/files/usr/bin/python3
"""Tests para coherencia_nichos."""
import sys
import os
import pytest

sys.path.insert(0, os.path.expanduser('~/proyectos/nlp'))
from modulos.coherencia_nichos import CoherenciaNichos


@pytest.mark.unit
class TestCoherenciaNichos:
    
    def test_detectar_herramienta_rag(self):
        coherencia = CoherenciaNichos()
        texto = "rag retrieval documents"
        herramienta = coherencia.detectar_herramienta(texto, 'TECNOLOGIA')
        assert herramienta == 'RAG'
    
    def test_validar_jerarquia_correcta(self):
        coherencia = CoherenciaNichos()
        jerarquia = {
            'nicho_principal': 'TECNOLOGIA',
            'secundarios': {'herramienta': 'RAG'}
        }
        assert coherencia.validar_jerarquia(jerarquia) == True
    
    def test_corregir_jerarquia(self):
        coherencia = CoherenciaNichos()
        jerarquia = {
            'nicho_principal': 'TECNOLOGIA',
            'secundarios': {'herramienta': 'CIBERSEGURIDAD'}
        }
        corregida = coherencia.corregir_jerarquia(jerarquia, "rag retrieval")
        assert corregida['secundarios']['herramienta'] == 'RAG'
