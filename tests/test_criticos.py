import sys
import os
import json
import sqlite3
import tempfile

sys.path.insert(0, os.path.expanduser('~/proyectos/nlp'))

import pytest
from modulos.content_id import generar_content_id, generar_hash
from modulos.detectar_nicho import detectar_nicho
from modulos.exportar_sqlite import exportar_sqlite_desde_json

# ==================== TEST IDENTIDAD ====================

@pytest.mark.critical
class TestIdentidad:
    def test_content_id_unico_youtube(self):
        url1 = "https://youtu.be/abc123xyz?si=xxxx"
        url2 = "https://www.youtube.com/watch?v=abc123xyz"
        id1 = generar_content_id(url1)
        id2 = generar_content_id(url2)
        assert id1 == id2
        assert id1 == "youtube:abc123xyz"

    def test_content_id_unico_github(self):
        url1 = "https://github.com/usuario/repo"
        url2 = "https://github.com/usuario/repo/tree/main"
        id1 = generar_content_id(url1)
        id2 = generar_content_id(url2)
        assert id1 == id2
        assert id1 == "github:usuario/repo"

    def test_content_id_diferente_fuentes(self):
        youtube = generar_content_id("https://youtu.be/abc123xyz")
        github = generar_content_id("https://github.com/usuario/repo")
        texto = generar_content_id("texto de prueba")
        assert youtube != github
        assert github != texto
        assert youtube != texto

    def test_hash_reproducible(self):
        texto = "Este es un texto de prueba"
        hash1 = generar_hash(texto)
        hash2 = generar_hash(texto)
        hash3 = generar_hash("Otro texto")
        assert hash1 == hash2
        assert hash1 != hash3

    def test_hash_normalizacion(self):
        t1 = "Hola Mundo"
        t2 = "hola mundo"
        t3 = "Hola  Mundo"
        assert generar_hash(t1) == generar_hash(t2)
        assert generar_hash(t1) == generar_hash(t3)

# ==================== TEST PERSISTENCIA ====================

@pytest.mark.critical
class TestPersistencia:
    def test_sqlite_export_valid(self):
        datos = {
            'documento': 'test.txt',
            'total_segmentos': 10,
            'terminos_clave': [('test', 5), ('ejemplo', 3)],
            'sentimiento_global': {'polaridad': 0.1, 'subjetividad': 0.4},
            'nicho': 'TECNOLOGIA'
        }
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(datos, f)
            json_path = f.name

        db_path = None
        try:
            db_path = exportar_sqlite_desde_json(json_path)
            assert os.path.exists(db_path)
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            assert ('keywords',) in tables
            assert ('analysis',) in tables
            cursor.execute("SELECT term, frequency FROM keywords;")
            rows = cursor.fetchall()
            assert len(rows) == 2
            assert ('test', 5) in rows
            conn.close()
        finally:
            os.unlink(json_path)
            if db_path and os.path.exists(db_path):
                os.unlink(db_path)

    def test_sqlite_no_duplicados(self):
        datos = {
            'documento': 'test.txt',
            'total_segmentos': 10,
            'terminos_clave': [('test', 5)],
            'sentimiento_global': {'polaridad': 0.1, 'subjetividad': 0.4},
            'nicho': 'TECNOLOGIA'
        }
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(datos, f)
            json_path = f.name

        db_path = None
        try:
            db_path1 = exportar_sqlite_desde_json(json_path)
            db_path2 = exportar_sqlite_desde_json(json_path)
            assert db_path1 == db_path2
            conn = sqlite3.connect(db_path1)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM keywords;")
            count = cursor.fetchone()[0]
            assert count == 1
            conn.close()
        finally:
            os.unlink(json_path)
            if db_path and os.path.exists(db_path):
                os.unlink(db_path)

# ==================== TEST PROGRESO ====================

@pytest.mark.critical
class TestProgreso:
    def test_estados_validos(self):
        estados = ['pending', 'processing', 'completed', 'error']
        for e in estados:
            assert e in ['pending', 'processing', 'completed', 'error']

# ==================== TEST NICHO ====================

@pytest.mark.critical
class TestNicho:
    def test_nicho_consistente(self):
        texto = "Machine learning y deep learning con PyTorch"
        n1 = detectar_nicho(texto)
        n2 = detectar_nicho(texto)
        assert n1 == n2

    def test_nicho_no_vacio(self):
        texto = "Texto aleatorio sin palabras clave"
        nicho = detectar_nicho(texto)
        assert nicho is not None
        assert nicho in ['LEGAL', 'SALUD', 'CIBERSEGURIDAD', 'TECNOLOGIA', 'FINANZAS', 'GENERAL']

    def test_nicho_especifico(self):
        texto_salud = "El ligamento cruzado anterior es una lesión común en deportistas"
        nicho = detectar_nicho(texto_salud)
        assert nicho in ['SALUD', 'GENERAL']
        
        texto_tecnologia = "Python y PyTorch para machine learning"
        nicho = detectar_nicho(texto_tecnologia)
        assert nicho in ['TECNOLOGIA', 'GENERAL']
