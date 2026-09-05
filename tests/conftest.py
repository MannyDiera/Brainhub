import json
import pytest
from pathlib import Path

@pytest.fixture
def contenido_youtube_salud():
    return {
        "content_id": "youtube:test_epidemiologia_001",
        "source_type": "youtube",
        "source_url": "https://www.youtube.com/watch?v=test_epidemiologia_001",
        "title": "Vigilancia epidemiológica y modelos predictivos",
        "author": "Canal de prueba",
        "language_original": "es",
        "raw_text": "Este contenido explica vigilancia epidemiológica, salud pública, pacientes y modelos predictivos para detectar brotes de enfermedades.",
        "pipeline_version": "6.4-test"
    }

@pytest.fixture
def json_contenido_salud(tmp_path, contenido_youtube_salud):
    ruta_json = tmp_path / "contenido_salud.json"
    ruta_json.write_text(
        json.dumps(contenido_youtube_salud, ensure_ascii=False),
        encoding="utf-8"
    )
    return ruta_json

@pytest.fixture
def sqlite_temporal(tmp_path):
    return tmp_path / "analisis_test.sqlite"
