#!/data/data/com.termux/files/usr/bin/python3
"""Tests para reflexion."""
import sys
import os
import pytest

sys.path.insert(0, os.path.expanduser('~/proyectos/nlp'))
from modulos.reflexion import ReflexionPostAnalisis


@pytest.mark.unit
class TestReflexion:
    
    def test_reflexion_genera_insights(self):
        reflexion = ReflexionPostAnalisis()
        analisis = {
            'nicho': 'TECNOLOGIA',
            'terminos_clave': [('reflection', 45)],
            'coocurrencias': [[['reflection', 'documents'], 19]]
        }
        reflexiones = reflexion.reflexionar(analisis)
        assert len(reflexiones) > 0
    
    def test_reflexion_termino_dominante(self):
        reflexion = ReflexionPostAnalisis()
        analisis = {
            'nicho': 'TECNOLOGIA',
            'terminos_clave': [('datos', 100)],
            'coocurrencias': []
        }
        reflexiones = reflexion.reflexionar(analisis)
        assert any('datos' in r for r in reflexiones)
