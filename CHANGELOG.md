# Changelog - BrainHub

## [6.5.1] - 2026-09-07

### Mejoras
- **Preguntas dinámicas**: reemplazadas plantillas fijas por generación basada en co-ocurrencias reales
- **Detección de idioma**: preguntas se generan en ES o EN según el documento
- **Coherencia de nichos**: nuevo módulo `coherencia_nichos.py` valida jerarquía lógica
- **Scoring por densidad**: `detectar_nicho.py` ahora clasifica por evidencia, no por prioridad
- **Dominio COMPRAS_PUBLICAS**: nuevo nicho con 11 términos

### Cambios técnicos
- `preguntas_debate.py`: plantillas morfológicas + datos reales
- `coherencia_nichos.py`: reglas de herramientas y contextos válidos por nicho
- `detectar_nicho.py`: scoring por densidad en vez de prioridad dura
- `diccionario_nichos.json`: agregado COMPRAS_PUBLICAS

### Problemas resueltos
- Falso positivo: defensa de tesis COMPRAR detectada como SALUD
- Falso positivo: documento RAG con herramienta CIBERSEGURIDAD
- Preguntas genéricas que no usaban el contenido del documento

## [6.5.0] - 2026-09-05

### Mejoras
- **RAG simple**: BM25 con Recall@3 = 1.0
- **Guardias de startup**: 4 precondiciones (identidad, schema, stopwords, diccionarios)
- **Adapters por fuente**: YouTube, GitHub, PDF, texto
- **Schemas Pydantic**: validación opcional
- **Fuzzy matching**: tolerancia a errores de transcripción

### Módulos nuevos (12)
- schemas.py, adapters_fuente.py, rag_simple.py
- fuzzy_nicho.py, nicho_multietiqueta.py, etiquetas_hibridas.py
- ponderacion_nichos.py, generar_abstract.py, preguntas_debate.py
- generar_documento.py, metricas.py, coherencia_nichos.py

## [6.4.0] - 2026-09-03

### Pipeline
- Eliminado DEBUG hardcodeado
- Eliminado nombres hardcodeados (Ana Brusco)
- DetectorHablantes con modos (tutorial, ateneo, legal, auto)
- Timestamps VTT con grounding temporal
- Métricas KISS por etapa

## [6.3.0] - 2026-08

### Base
- Pipeline NLP funcional
- 11 tests críticos
- Stopwords dinámicas desde JSON
- DuckDB como base analítica
- Detección de nicho básica

## [6.5.2] - 2026-09-07

### Mejoras
- **Paginación DuckDB**: cursor pagination para datasets grandes
- **Reflexión post-análisis**: insights automáticos sobre resultados
- **Preguntas bilingües**: detección de idioma ES/EN
- **Co-ocurrencias reales**: preguntas basadas en datos del documento

### Módulos nuevos
- paginacion.py: consultas paginadas
- reflexion.py: reflexiones post-análisis

### Correcciones
- GeneradorDocumento: sección de reflexiones integrada
- Scoring por densidad en detectar_nicho
