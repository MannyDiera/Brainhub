#!/data/data/com.termux/files/usr/bin/python3
"""Tests para grounding."""
import sys
import os
import pytest

sys.path.insert(0, os.path.expanduser('~/proyectos/nlp'))
from modulos.grounding import agregar_grounding, fusionar_groundings


@pytest.mark.unit
class TestGrounding:
    
    def test_agregar_grounding(self):
        """Agrega grounding a entidad."""
        entidad = {'nombre': 'PyTorch', 'tipo': 'framework'}
        entidad = agregar_grounding(entidad, 'video1', 'fragmento texto', 10, 0.9)
        
        assert 'grounding' in entidad
        assert len(entidad['grounding']) == 1
        assert entidad['grounding'][0]['documento'] == 'video1'
        assert entidad['grounding'][0]['confianza'] == 0.9
    
    def test_fusionar_groundings(self):
        """Fusiona groundings de dos entidades."""
        e1 = {'nombre': 'PyTorch', 'tipo': 'framework'}
        e1 = agregar_grounding(e1, 'video1', 'fragmento1', 10, 0.9)
        
        e2 = {'nombre': 'PyTorch', 'tipo': 'framework'}
        e2 = agregar_grounding(e2, 'video2', 'fragmento2', 20, 0.8)
        
        fusionada = fusionar_groundings(e1, e2)
        assert len(fusionada['grounding']) == 2
