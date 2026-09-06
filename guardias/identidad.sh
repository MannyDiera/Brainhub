#!/bin/bash
# Guardia: verifica identidad de contenido

echo "🔐 Verificando identidad de contenido..."

python3 -c "
from modulos.content_id import generar_content_id
from modulos.content_id import generar_hash

# Verificaciones idempotentes
assert generar_content_id('https://youtu.be/abc123xyz') == 'youtube:abc123xyz'
assert generar_hash('contenido') == generar_hash('contenido')
print('✅ content_id y content_hash OK')
" || exit 1
