#!/data/data/com.termux/files/usr/bin/python3
"""Tests para ponderacion_nichos."""
import sys
import os
import pytest

sys.path.insert(0, os.path.expanduser('~/proyectos/nlp'))
from modulos.ponderacion_nichos import PonderacionNichos


@pytest.fixture
def diccionario():
    return {
        'SALUD': ['diagnóstico', 'paciente', 'tratamiento'],
        'TECNOLOGIA': ['software', 'algoritmo', 'datos'],
        'LEGAL': ['ley', 'juzgado', 'normativa']
    }


@pytest.mark.unit
class TestPonderacionNichos:
    
    def test_analizar_jerarquia(self, diccionario):
        ponderador = PonderacionNichos(diccionario)
        texto = "El software de diagnóstico para pacientes. La normativa legal."
        resultado = ponderador.analizar(texto)
        assert 'nicho_principal' in resultado
        assert 'scores' in resultado
    
    def test_scores_sum(self, diccionario):
        ponderador = PonderacionNichos(diccionario)
        texto = "software algoritmo datos"
        resultado = ponderador.analizar(texto)
        scores = resultado['scores']
        assert scores['TECNOLOGIA'] > 0
