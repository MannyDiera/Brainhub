#!/data/data/com.termux/files/usr/bin/python3
"""Tests para generar_abstract."""
import sys
import os
import pytest

sys.path.insert(0, os.path.expanduser('~/proyectos/nlp'))
from modulos.generar_abstract import GeneradorAbstract


@pytest.mark.unit
class TestGenerarAbstract:
    
    def test_generar_abstract(self):
        gen = GeneradorAbstract()
        jerarquia = {'nicho_principal': 'SALUD', 'secundarios': {'herramienta': 'TECNOLOGIA'}}
        terminos = ['diagnóstico', 'paciente', 'algoritmo']
        abstract = gen.generar(jerarquia, terminos)
        assert 'SALUD' in abstract
        assert 'TECNOLOGIA' in abstract
    
    def test_corregir_errores(self):
        gen = GeneradorAbstract()
        texto = "machin lerning para diagnóstico"
        corregido = gen.corregir_errores(texto)
        assert 'machine learning' in corregido
