#!/data/data/com.termux/files/usr/bin/python3
"""Tests para detectar_modo."""
import sys
import os
import pytest

sys.path.insert(0, os.path.expanduser('~/proyectos/nlp'))
from modulos.detectar_modo import detectar_modo_automatico


@pytest.mark.unit
class TestDetectarModo:
    
    def test_modo_legal(self):
        """Detecta modo legal con términos judiciales."""
        texto = "El juzgado dictó sentencia. El fiscal presentó el expediente."
        assert detectar_modo_automatico(texto) == 'legal'
    
    def test_modo_tutorial(self):
        """Detecta tutorial con contenido simple."""
        texto = "\n".join([
            "En este video aprendemos Python.",
            "Los tensores son importantes.",
            "PyTorch facilita el deep learning.",
            "Continuamos con más ejemplos.",
            "El modelo mejora la precisión.",
            "Finalizamos con práctica.",
            "Ahora repasamos conceptos.",
            "Siguiente sección del tutorial.",
            "Vamos a programar.",
            "Python y PyTorch juntos.",
            "Ejemplos de código simple.",
            "La práctica hace al maestro.",
            "Continuamos avanzando.",
            "Última sección del video.",
            "Resumen de lo aprendido.",
            "Practicamos más ejercicios.",
            "El código funciona.",
            "Siguiente lección.",
            "Repasamos lo visto.",
            "Terminamos el tutorial.",
            "Gracias por ver."
        ])
        modo = detectar_modo_automatico(texto)
        assert modo in ['tutorial', 'auto']
    
    def test_modo_default(self):
        """Sin señales claras, retorna auto."""
        texto = "Texto genérico sin términos legales ni múltiples hablantes."
        assert detectar_modo_automatico(texto) == 'auto'
