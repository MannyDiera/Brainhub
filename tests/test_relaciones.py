#!/data/data/com.termux/files/usr/bin/python3
import sys
import os
import pytest

sys.path.insert(0, os.path.expanduser('~/proyectos/nlp'))

from modulos.relaciones import RelacionesManager


@pytest.mark.unit
class TestRelaciones:
    
    def test_extraccion_basica(self):
        manager = RelacionesManager()
        texto = "Python usa PyTorch"
        entidades = ['Python', 'PyTorch']
        
        relaciones = manager.extraer_de_texto(texto, entidades)
        
        assert len(relaciones) > 0
        assert relaciones[0]['origen'] == 'python'
        assert relaciones[0]['destino'] == 'pytorch'
        assert relaciones[0]['tipo'] == 'usa'
    
    def test_consolidacion(self):
        manager = RelacionesManager()
        relaciones = [
            {'origen': 'a', 'destino': 'b', 'tipo': 'usa', 'peso': 1.0},
            {'origen': 'a', 'destino': 'b', 'tipo': 'usa', 'peso': 1.0},
            {'origen': 'a', 'destino': 'c', 'tipo': 'usa', 'peso': 1.0}
        ]
        
        consolidadas = manager.consolidar_relaciones(relaciones)
        
        assert len(consolidadas) == 2
        assert consolidadas[0]['frecuencia'] == 2
    
    def test_exportar_cypher(self):
        manager = RelacionesManager()
        relaciones = [
            {'origen': 'python', 'destino': 'pytorch', 'tipo': 'usa', 'peso': 1.0}
        ]
        
        cypher = manager.exportar_cypher(relaciones)
        
        assert 'MERGE' in cypher
        assert 'usa' in cypher
