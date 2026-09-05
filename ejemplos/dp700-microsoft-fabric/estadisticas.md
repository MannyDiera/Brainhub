# Estadísticas del grafo consolidado

## Métricas
- **Videos procesados**: 37
- **Dominios**: PyTorch, DP-700 (Fabric), DefCon, CAIS 2026, AFRICAI, Seguridad IA
- **Nodos (términos únicos)**: 124
- **Relaciones (co-ocurrencias)**: 456
- **Densidad**: 0.06 (sparse, legible)
- **Stopwords filtradas**: 372 (5 capas)
- **Tests automatizados**: 48

## Términos principales por dominio

| Dominio | Top términos |
|---------|--------------|
| Data Engineering | datos (40), código (27), utilizar (14) |
| IA | inteligencia (28), artificial (16), pensar (13) |
| ML/PyTorch | model (7), torch (7), loss |
| Salud (CAIS) | salud (13), paciente, datos |
| Seguridad (DefCon) | hacker, fbi, network |

## Clusters identificados

1. **Estructuras de datos**: array → list → currentnode → root
2. **Machine Learning**: model → loss → tensor → learning
3. **Data Engineering**: datos ↔ fabric ↔ microsoft ↔ examen
4. **Salud + IA**: salud ↔ inteligencia ↔ artificial
5. **Seguridad**: hacker ↔ fbi ↔ network

## Métricas de cobertura

| Módulo crítico | Cobertura |
|----------------|-----------|
| content_hash | 100% |
| config_modos | 100% |
| detectar_modo | 94% |
| detectar_nicho | 94% |
| grounding | 94% |
| content_id | 85% |

## Centralidad de Intermediación (Betweenness Centrality)

Mide qué tan estratégico es un término como puente entre otros conceptos.

| Nodo | Centralidad | Rol |
|------|-------------|-----|
| datos | 0.643 | Monopolio (64% del flujo) |
| código | 0.422 | Monopolio (42% del flujo) |
| inteligencia | 0.198 | Puente técnico |
| modelo | 0.142 | Puente ML |
| salud | 0.004 | **Periférico (0.4%)** |

### Interpretación

salud tiene centralidad 0.004: es un nodo terminal, no un puente.
El reto ontológico: lograr que términos clínicos conecten ingeniería con medicina.

### Centralidad actualizada (39 videos)
| Nodo | Centralidad | Cambio |
|------|-------------|--------|
| datos | 0.648 | = |
| salud | 0.037 | +925% |
| código | 0.391 | -7% |

**salud pasó de 0.004 a 0.037** al procesar CAIS 2 y 3. La ontología clínica funciona.
