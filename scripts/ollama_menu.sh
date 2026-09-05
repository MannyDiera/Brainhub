#!/bin/bash

SESSION="ollama"

# Verificar si la sesión tmux ya existe
tmux has-session -t $SESSION 2>/dev/null
if [ $? != 0 ]; then
  echo "⚙️ Arrancando servidor Ollama en sesión tmux..."
  tmux new-session -d -s $SESSION "ollama serve"
else
  echo "✅ Servidor Ollama ya está activo en sesión tmux."
fi

# Instalar modelos si no están presentes
echo "📥 Verificando modelos..."
ollama list | grep -q "phi3:mini" || ollama pull phi3:mini
ollama list | grep -q "gemma:2b" || ollama pull gemma:2b
ollama list | grep -q "tinyllama" || ollama pull tinyllama

# Menú interactivo
echo "Selecciona modelo:"
echo "1) phi3:mini (código, pandas, scikit-learn)"
echo "2) gemma:2b (chat general, multilingüe)"
echo "3) tinyllama (ultraligero, respaldo)"
read opt

case $opt in
  1) ollama run phi3:mini ;;
  2) ollama run gemma:2b ;;
  3) ollama run tinyllama ;;
  *) echo "Opción inválida" ;;
esac
