#!/bin/bash

echo "🚀 Iniciando instalación de modelos LLM en Ollama..."

# Verificar que el servidor Ollama esté corriendo en tmux
SESSION="ollama"
tmux has-session -t $SESSION 2>/dev/null
if [ $? != 0 ]; then
  echo "⚙️ Arrancando servidor Ollama en sesión tmux..."
  tmux new-session -d -s $SESSION "ollama serve"
else
  echo "✅ Servidor Ollama ya está activo en sesión tmux."
fi

# Instalar phi3:mini
echo "📥 Descargando modelo phi3:mini..."
ollama pull phi3:mini

# Instalar Gemma 2B
echo "📥 Descargando modelo gemma:2b..."
ollama pull gemma:2b

echo "✅ Instalación completa. Modelos disponibles:"
echo " - phi3:mini"
echo " - gemma:2b"

echo "👉 Usá 'ollama run phi3:mini' o 'ollama run gemma:2b' para iniciar."
