<<<<<<< HEAD
# BrainHub

Sistema de procesamiento de conocimiento técnico con NLP, grafos y gestión de aprendizaje.

Sistema de procesamiento de contenido técnico con NLP, gestión de aprendizaje y generación de grafos de conocimiento.

## Características

- Pipeline completo: procesar, analizar, consolidar
- 20+ módulos especializados
- Grafo de conocimiento visual
- Detector de hablantes con modos (tutorial, ateneo, legal, auto)
- Stopwords dinámicas (334 palabras en 5 capas)
- 36 tests automatizados
- 7 formatos de salida (JSON, TXT, MD, SQLite, MP3, Parquet, DuckDB)

## Comandos

| Comando | Entrada | Salida | Descripción |
|---------|---------|--------|-------------|
| `procesar URL` | URL de YouTube | Transcripción .txt + VTT | Descarga con fallback |
| `analizar archivo.txt` | Archivo de texto | Análisis NLP completo | Nicho, sentimiento, términos |
| `consolidar` | SQLite | DuckDB | Consolida términos |

## Aprendizaje

| Comando | Descripción |
|---------|-------------|
| `aprender` | Menú interactivo maestro |
| `sigue` | Próximo contenido pendiente |
| `listo <id>` | Marca contenido como completado |
| `estado` | Muestra progreso general |

## Flujo completo

# 1. Descargar transcripción
procesar "https://youtu.be/VIDEO_ID"

# 2. Analizar contenido
analizar /sdcard/Download/Transcript_VIDEO_ID.txt

# 3. Ver grafo de conocimiento
python3 generar_grafo_optimizado.py

## Requisitos

- Python 3.8+
- DuckDB CLI
- Termux (Android) o Linux

## Instalación

git clone https://github.com/tu-usuario/ecosistema-nlp.git
cd ecosistema-nlp
pip install -r requirements.txt

## Tests

python3 -m pytest tests/ -v

## Métricas

- Módulos: 20+
- Tests: 48
- Stopwords: 334
- Nodos en grafo: 96
- Cobertura: 39%


=======
# Brainhub
BrainHub es un ecosistema de aprendizaje personal que procesa  contenido técnico (videos, papers, transcripciones) y lo transforma  en conocimiento estructurado: grafos, jerarquías de nichos, resúmenes  80/20 y preguntas de debate.  No es una herramienta de vigilancia epidemiológica. Es un sistema  de aprendizaje extensible.
>>>>>>> 4ed5a04c9bfba0f2e3adaa252bba0c77cee21a99
