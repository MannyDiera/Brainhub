#!/data/data/com.termux/files/usr/bin/python3
"""
Tests para DetectorHablantes.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.expanduser('~/proyectos/nlp'))

from modulos.detector_hablantes import DetectorHablantes, Hablante


@pytest.mark.unit
class TestDetectorHablantes:
    
    def test_modo_tutorial_ignora_menciones(self):
        """Modo tutorial ignora nombres mencionados."""
        texto = """
        En este tutorial de machine learning.
        Como dice la Abogada Ana Brusco en su paper.
        Python y PyTorch son las herramientas.
        """
        
        detector = DetectorHablantes(modo='tutorial')
        hablantes = detector.detectar(texto, [''] * 75)
        
        assert len(hablantes) == 0
    
    def test_modo_legal_detecta_profesiones(self):
        """Modo legal detecta hablantes con profesión."""
        texto = """
        La Dra. María González presenta el caso.
        El Abogado Juan Pérez responde.
        La testigo declara los hechos.
        """
        
        detector = DetectorHablantes(modo='legal')
        hablantes = detector.detectar(texto, [''] * 100)
        
        assert len(hablantes) >= 3
        
        nombres = [h.nombre for h in hablantes]
        assert any('testigo' in n.lower() for n in nombres)
        assert not any('declara' in n for n in nombres)
    
    def test_modo_legal_anonimiza(self):
        """Modo legal asigna anónimos si no hay nombres."""
        texto = "Este es un testimonio sin nombres propios."
        
        detector = DetectorHablantes(modo='legal')
        hablantes = detector.detectar(texto, [''] * 100)
        
        nombres = [h.nombre for h in hablantes]
        assert any('persona' in n for n in nombres)
    
    def test_config_modos_cargados(self):
        """Los modos se cargan desde config_modos."""
        detector = DetectorHablantes(modo='auto')
        
        assert 'tutorial' in detector.MODOS
        assert 'ateneo' in detector.MODOS
        assert 'legal' in detector.MODOS
        assert 'auto' in detector.MODOS
    
    def test_resumen_estructura(self):
        """El resumen tiene estructura correcta."""
        detector = DetectorHablantes(modo='legal')
        detector.detectar("La Dra. María González presenta.", [''] * 100)
        
        resumen = detector.obtener_resumen()
        
        assert 'modo' in resumen
        assert 'total_hablantes' in resumen
        assert 'hablantes' in resumen
        assert isinstance(resumen['hablantes'], list)
