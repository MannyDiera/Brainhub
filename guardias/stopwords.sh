#!/bin/bash
# Guardia: verifica stopwords cargadas

echo "📚 Verificando stopwords..."

python3 -c "
import json
from pathlib import Path

ruta = Path.home() / 'proyectos/nlp/stopwords.json'
datos = json.loads(ruta.read_text())

assert 'base' in datos
assert len(datos['base']['es']) > 0
assert len(datos['base']['en']) > 0
print(f'✅ Stopwords OK (ES: {len(datos[\"base\"][\"es\"])}, EN: {len(datos[\"base\"][\"en\"])})')
" || exit 1
