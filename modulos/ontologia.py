#!/data/data/com.termux/files/usr/bin/python3
"""
Módulo de Ontología para BrainHub.
Clase base genérica + clase heredada para Salud.
"""

from typing import Dict, List, Tuple, Optional
from collections import defaultdict
import json


class OntologyEngine:
    """Clase base genérica para ontologías."""
    
    def __init__(self):
        self.grafo = defaultdict(dict)  # nodo -> {vecino: peso}
        self.nodos = set()
        self.sinonimos = {}  # término normalizado -> [variantes]
        self.stopwords = set()
    
    def add_concept(self, term: str, domain: str = 'general'):
        """Registra un nodo de forma estandarizada."""
        term_normalizado = self._normalizar(term)
        self.nodos.add(term_normalizado)
        if domain not in self.sinonimos:
            self.sinonimos[domain] = {}
        self.sinonimos[domain][term_normalizado] = [term]
    
    def connect_concepts(self, source: str, target: str, weight: float):
        """Registra una arista entre conceptos."""
        source_norm = self._normalizar(source)
        target_norm = self._normalizar(target)
        self.grafo[source_norm][target_norm] = weight
        self.grafo[target_norm][source_norm] = weight
        self.nodos.add(source_norm)
        self.nodos.add(target_norm)
    
    def get_metrics(self):
        """Calcula centralidad de intermediación."""
        from modulos.centralidad import BetweennessCentrality
        
        bc = BetweennessCentrality()
        for origen in self.grafo:
            for destino, peso in self.grafo[origen].items():
                bc.agregar_relacion(origen, destino, peso)
        
        return bc.calcular()
    
    def _normalizar(self, term: str) -> str:
        """Normaliza término: minúsculas, sin espacios extra."""
        return term.lower().strip()
    
    def cargar_grafo(self, ruta_json: str):
        """Carga grafo desde JSON."""
        with open(ruta_json, 'r', encoding='utf-8') as f:
            datos = json.load(f)
        
        for arista in datos.get('aristas', []):
            self.connect_concepts(
                arista['origen'],
                arista['destino'],
                arista.get('peso', 1.0)
            )


class HealthOntology(OntologyEngine):
    """Ontología específica para dominio de Salud."""
    
    # Mapeo de términos clínicos (simulación de UMLS/SNOMED)
    DICCIONARIO_CLINICO = {
        'historia clinica': 'ehr_concept',
        'historia clínica': 'ehr_concept',
        'registro electronico de salud': 'ehr_concept',
        'registro electrónico de salud': 'ehr_concept',
        'data de pacientes': 'ehr_concept',
        'hc': 'ehr_concept',
        'hce': 'ehr_concept',
        'clinical history': 'ehr_concept',
        
        'interoperabilidad': 'interoperabilidad_fhir',
        'interoperability': 'interoperabilidad_fhir',
        'fhir': 'interoperabilidad_fhir',
        'hl7': 'interoperabilidad_fhir',
        
        'diagnostico': 'diagnostico_clinico',
        'diagnóstico': 'diagnostico_clinico',
        'sintoma': 'sintoma_clinico',
        'síntoma': 'sintoma_clinico',
        'tratamiento': 'tratamiento_clinico',
        'paciente': 'paciente_clinico',
    }
    
    # Multiplicador de peso para relaciones clínicas
    MULTIPLICADOR_CLINICO = 1.5
    
    # Términos que indican contexto clínico
    TERMINOS_CLINICOS = {
        'paciente', 'diagnostico', 'diagnóstico', 'tratamiento',
        'sintoma', 'síntoma', 'salud', 'ehr_concept',
        'interoperabilidad_fhir', 'diagnostico_clinico',
        'sintoma_clinico', 'tratamiento_clinico', 'paciente_clinico'
    }
    
    # Puentes de control entre dominios
    PUENTES_CONTROL = {
        ('fabric', 'hospital'): 'interoperabilidad_fhir',
        ('microsoft', 'salud'): 'interoperabilidad_fhir',
        ('datos', 'paciente'): 'ehr_concept',
        ('codigo', 'diagnostico'): 'diagnostico_clinico',
    }
    
    def __init__(self):
        super().__init__()
        self.domain = 'salud'
    
    def _normalizar(self, term: str) -> str:
        """Normaliza y mapea a concepto clínico si existe."""
        term_norm = term.lower().strip()
        
        # Buscar en diccionario clínico
        if term_norm in self.DICCIONARIO_CLINICO:
            return self.DICCIONARIO_CLINICO[term_norm]
        
        return term_norm
    
    def _es_clinico(self, term: str) -> bool:
        """Verifica si un término es clínico."""
        return term in self.TERMINOS_CLINICOS
    
    def connect_concepts(self, source: str, target: str, weight: float):
        """Sobreescribe con ponderación semántica asimétrica."""
        source_norm = self._normalizar(source)
        target_norm = self._normalizar(target)
        
        # Ponderación asimétrica: clínico > ingeniería
        peso_final = weight
        if self._es_clinico(source_norm) or self._es_clinico(target_norm):
            peso_final = weight * self.MULTIPLICADOR_CLINICO
        
        # Inyectar puentes de control
        clave = (source_norm, target_norm)
        if clave in self.PUENTES_CONTROL:
            puente = self.PUENTES_CONTROL[clave]
            self.nodos.add(puente)
            # Conectar ambos al puente
            self.grafo[source_norm][puente] = peso_final * 2.0
            self.grafo[puente][source_norm] = peso_final * 2.0
            self.grafo[target_norm][puente] = peso_final * 2.0
            self.grafo[puente][target_norm] = peso_final * 2.0
        
        super().connect_concepts(source_norm, target_norm, peso_final)
    
    def get_metrics(self) -> Dict:
        """Calcula métricas y retorna análisis de centralidad."""
        centralidad = super().get_metrics()
        
        # Análisis específico
        analisis = {
            'centralidad': centralidad,
            'salud_centralidad': centralidad.get('ehr_concept', centralidad.get('salud', 0)),
            'datos_centralidad': centralidad.get('datos', 0),
            'puentes_clinicos': [
                nodo for nodo in centralidad 
                if nodo in self.TERMINOS_CLINICOS
            ]
        }
        
        return analisis


# Test
if __name__ == '__main__':
    # Ontología genérica
    print("🔧 OntologyEngine genérica:")
    engine = OntologyEngine()
    engine.add_concept('datos', 'general')
    engine.add_concept('salud', 'general')
    engine.connect_concepts('datos', 'salud', 5.0)
    print(f"   Nodos: {len(engine.nodos)}")
    
    # Ontología de salud
    print("\n🏥 HealthOntology:")
    salud_onto = HealthOntology()
    
    # Mapeo de sinónimos
    salud_onto.add_concept('historia clinica', 'salud')
    salud_onto.add_concept('registro electronico de salud', 'salud')
    salud_onto.connect_concepts('historia clinica', 'paciente', 5.0)
    
    print(f"   Nodos normalizados: {len(salud_onto.nodos)}")
    print(f"   Sinónimos mapeados: {len(salud_onto.DICCIONARIO_CLINICO)}")
