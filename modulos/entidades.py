#!/usr/bin/env python3
"""
Módulo de entidades y relaciones para el ecosistema NLP.
Uso: from modulos.entidades import Entity, Relation, EntityManager
"""

import re
import hashlib
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Set
from datetime import datetime
from collections import defaultdict

# ============================================================
# CLASE ENTITY
# ============================================================

@dataclass
class Entity:
    """
    Representa una entidad extraída de un contenido.
    """
    nombre: str
    tipo: str  # "Persona", "Organización", "Tecnología", "Concepto", "Lugar", "Evento"
    video_id: str
    timestamp: Optional[str] = None
    fragmento: Optional[str] = None
    descripcion: Optional[str] = None
    frecuencia: int = 1
    relevancia: float = 0.5
    metadatos: Dict[str, Any] = field(default_factory=dict)
    relaciones: List['Relation'] = field(default_factory=list)
    grounding: Optional[Dict[str, Any]] = field(default_factory=dict)
    fecha_creacion: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def __post_init__(self):
        if not hasattr(self, '_id') or not self._id:
            self._id = self.generar_id()
    
    @property
    def id(self) -> str:
        return self._id
    
    def generar_id(self) -> str:
        """Genera un ID único basado en nombre y tipo."""
        contenido = f"{self.nombre.lower()}_{self.tipo.lower()}"
        return f"ent:{hashlib.md5(contenido.encode()).hexdigest()[:12]}"
    
    def agregar_relacion(self, relacion: 'Relation'):
        self.relaciones.append(relacion)
    
    def actualizar_frecuencia(self):
        self.frecuencia += 1
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "tipo": self.tipo,
            "video_id": self.video_id,
            "timestamp": self.timestamp,
            "fragmento": self.fragmento,
            "descripcion": self.descripcion,
            "frecuencia": self.frecuencia,
            "relevancia": self.relevancia,
            "relaciones": [r.to_dict() for r in self.relaciones],
            "grounding": self.grounding,
            "fecha_creacion": self.fecha_creacion
        }
    
    def to_cypher(self) -> str:
        fragmento_limpio = self.fragmento.replace("'", "\\'")[:100] if self.fragmento else ""
        return f"""
CREATE (e:Entidad {{
    id: '{self.id}',
    nombre: '{self.nombre}',
    tipo: '{self.tipo}',
    video_id: '{self.video_id}',
    timestamp: '{self.timestamp}',
    fragmento: '{fragmento_limpio}...',
    frecuencia: {self.frecuencia},
    relevancia: {self.relevancia},
    fecha_creacion: '{self.fecha_creacion}'
}})
"""
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        if isinstance(other, Entity):
            return self.id == other.id
        return False


# ============================================================
# CLASE RELATION
# ============================================================

@dataclass
class Relation:
    origen: str  # ID de la entidad origen
    destino: str  # ID de la entidad destino
    tipo: str  # "usa", "creado_por", "parte_de", "relacionado_con", "menciona", "trabaja_en"
    video_id: str
    timestamp: Optional[str] = None
    fragmento: Optional[str] = None
    confianza: float = 0.5
    
    def to_dict(self) -> dict:
        return {
            "origen": self.origen,
            "destino": self.destino,
            "tipo": self.tipo,
            "video_id": self.video_id,
            "timestamp": self.timestamp,
            "fragmento": self.fragmento,
            "confianza": self.confianza
        }
    
    def to_cypher(self) -> str:
        return f"""
MATCH (a:Entidad {{id: '{self.origen}'}})
MATCH (b:Entidad {{id: '{self.destino}'}})
CREATE (a)-[:{self.tipo.upper()} {{
    video_id: '{self.video_id}',
    timestamp: '{self.timestamp}',
    confianza: {self.confianza}
}}]->(b)
"""


# ============================================================
# CLASE ENTITY MANAGER
# ============================================================

class EntityManager:
    """Gestiona entidades y relaciones en el ecosistema."""
    
    def __init__(self):
        self.entidades: Dict[str, Entity] = {}
        self.relaciones: List[Relation] = []
    
    def agregar_entidad(self, entidad: Entity):
        if entidad.id in self.entidades:
            self.entidades[entidad.id].actualizar_frecuencia()
            self.entidades[entidad.id].metadatos.update(entidad.metadatos)
        else:
            self.entidades[entidad.id] = entidad
    
    def agregar_relacion(self, relacion: Relation):
        self.relaciones.append(relacion)
    
    def buscar_por_nombre(self, nombre: str) -> List[Entity]:
        nombre_lower = nombre.lower()
        return [e for e in self.entidades.values() if nombre_lower in e.nombre.lower()]
    
    def buscar_por_tipo(self, tipo: str) -> List[Entity]:
        return [e for e in self.entidades.values() if e.tipo == tipo]
    
    def buscar_por_video(self, video_id: str) -> List[Entity]:
        return [e for e in self.entidades.values() if e.video_id == video_id]
    
    def entidades_mas_frecuentes(self, top_n: int = 10) -> List[Entity]:
        return sorted(self.entidades.values(), key=lambda e: e.frecuencia, reverse=True)[:top_n]
    
    def grafo_to_json(self) -> dict:
        return {
            "entidades": [e.to_dict() for e in self.entidades.values()],
            "relaciones": [r.to_dict() for r in self.relaciones]
        }
    
    def grafo_to_cypher(self) -> str:
        cypher = []
        for e in self.entidades.values():
            cypher.append(e.to_cypher())
        for r in self.relaciones:
            cypher.append(r.to_cypher())
        return "\n".join(cypher)
    
    def fusionar_entidades(self, entidad1_id: str, entidad2_id: str) -> Optional[Entity]:
        if entidad1_id not in self.entidades or entidad2_id not in self.entidades:
            return None
        
        e1 = self.entidades[entidad1_id]
        e2 = self.entidades[entidad2_id]
        
        entidad_fusionada = Entity(
            nombre=e1.nombre,
            tipo=e1.tipo,
            video_id=e1.video_id,
            timestamp=e1.timestamp or e2.timestamp,
            fragmento=e1.fragmento or e2.fragmento,
            descripcion=e1.descripcion or e2.descripcion,
            frecuencia=e1.frecuencia + e2.frecuencia,
            relevancia=max(e1.relevancia, e2.relevancia),
            metadatos={**e1.metadatos, **e2.metadatos},
            grounding=e1.grounding or e2.grounding
        )
        
        del self.entidades[entidad1_id]
        del self.entidades[entidad2_id]
        self.entidades[entidad_fusionada.id] = entidad_fusionada
        
        return entidad_fusionada
    
    def estadisticas(self) -> dict:
        tipos = defaultdict(int)
        for e in self.entidades.values():
            tipos[e.tipo] += 1
        
        return {
            "total_entidades": len(self.entidades),
            "total_relaciones": len(self.relaciones),
            "tipos": dict(tipos),
            "entidades_mas_frecuentes": [
                {"nombre": e.nombre, "frecuencia": e.frecuencia} 
                for e in self.entidades_mas_frecuentes(5)
            ]
        }
    
    def desde_terminos(self, terminos: List[tuple], video_id: str) -> List[Entity]:
        """
        Crea entidades a partir de una lista de términos clave.
        """
        entidades = []
        for term, freq in terminos:
            tipo = self._detectar_tipo(term)
            entidad = Entity(
                nombre=term,
                tipo=tipo,
                video_id=video_id,
                frecuencia=freq,
                relevancia=min(freq / 10, 1.0)  # Normalizar frecuencia
            )
            entidades.append(entidad)
            self.agregar_entidad(entidad)
        return entidades
    
    def _detectar_tipo(self, term: str) -> str:
        """Detecta el tipo de una entidad basado en el término."""
        term_lower = term.lower()
        
        # Tecnologías
        tecnologias = {'pytorch', 'python', 'langchain', 'tensorflow', 'keras', 'pandas', 'numpy', 'scikit-learn'}
        if term_lower in tecnologias:
            return "Tecnología"
        
        # Personas
        personas = {'daniel bourke', 'juan gabriel gomila'}
        if term_lower in personas:
            return "Persona"
        
        # Organizaciones
        organizaciones = {'meta', 'google', 'openai', 'microsoft', 'ibm'}
        if term_lower in organizaciones:
            return "Organización"
        
        # Conceptos
        conceptos = {'machine learning', 'deep learning', 'neural network', 'tensor', 'gradient'}
        if any(c in term_lower for c in conceptos):
            return "Concepto"
        
        return "Concepto"  # Default


# ============================================================
# FUNCIÓN DE CONVENIENCIA
# ============================================================

def crear_entidades_desde_analisis(json_path: str, video_id: str) -> EntityManager:
    """
    Crea un EntityManager a partir de un archivo de análisis JSON.
    """
    import json
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    manager = EntityManager()
    terminos = data.get('terminos_clave', [])
    
    manager.desde_terminos(terminos, video_id)
    
    return manager
