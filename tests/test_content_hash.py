#!/data/data/com.termux/files/usr/bin/python3
"""Tests para content_hash."""
import sys
import os
import pytest

sys.path.insert(0, os.path.expanduser('~/proyectos/nlp'))
from modulos.content_hash import generar_content_hash, verificar_cambio


@pytest.mark.unit
class TestContentHash:
    
    def test_hash_reproducible(self):
        """El hash es reproducible para el mismo contenido."""
        h1 = generar_content_hash("hola mundo")
        h2 = generar_content_hash("hola mundo")
        assert h1 == h2
    
    def test_hash_cambia_con_contenido(self):
        """Hash diferente para contenido diferente."""
        h1 = generar_content_hash("hola mundo")
        h2 = generar_content_hash("hola mundos")
        assert h1 != h2
    
    def test_verificar_cambio(self):
        """Detecta cambios reales."""
        hash_original = generar_content_hash("contenido original")
        assert verificar_cambio("id1", "contenido original", hash_original) == False
        assert verificar_cambio("id1", "contenido cambiado", hash_original) == True
