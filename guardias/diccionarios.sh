#!/bin/bash
# Guardia: verifica diccionarios cargados

echo "📖 Verificando diccionarios..."

python3 -c "
import json
from pathlib import Path

clinico = Path.home() / 'proyectos/nlp/diccionario_clinico.json'
nichos = Path.home() / 'proyectos/nlp/diccionario_nichos.json'

assert clinico.exists(), 'diccionario_clinico.json no existe'
assert nichos.exists(), 'diccionario_nichos.json no existe'

clinico_data = json.loads(clinico.read_text())
nichos_data = json.loads(nichos.read_text())

assert len(clinico_data) > 0
assert len(nichos_data) > 0
print(f'✅ Diccionarios OK (clínico: {len(clinico_data)}, nichos: {len(nichos_data)})')
" || exit 1
