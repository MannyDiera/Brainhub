#!/data/data/com.termux/files/usr/bin/python3
"""
Detector de Hablantes V1 - Clase con modos y objetos.
Usa configuración desde config_modos.py.
"""

import re
from typing import Dict, List, Optional
from dataclasses import dataclass, field

# Importar configuración de modos
try:
    from modulos.config_modos import ConfiguracionModo, obtener_modos
except ModuleNotFoundError:
    from config_modos import ConfiguracionModo, obtener_modos


@dataclass
class Hablante:
    """Objeto hablante detectado."""
    nombre: str
    rol: str = "desconocido"
    segmentos: int = 0
    sentimiento_promedio: float = 0.0
    mencionado: bool = False
    es_principal: bool = False


class DetectorHablantes:
    """Detector de hablantes con modos y objetos."""
    
    # Patrones de detección
    PATRON_NOMBRE_PROFESION = re.compile(
        r'(?:Dr\.?|Dra\.?|Abogad[oa]|Juez|Jueza|Fiscal|Defensor[ao]?)\s+([A-ZÁÉÍÓÚ][a-záéíóú]+(?:\s+[A-ZÁÉÍÓÚ][a-záéíóú]+)?)',
        re.IGNORECASE
    )
    
    # Testigo sin nombre específico
    PATRON_TESTIGO = re.compile(
        r'\b(Testigo|testigo)\b',
        re.IGNORECASE
    )
    
    PATRON_DIALOGO = re.compile(
        r'^([A-ZÁÉÍÓÚ][a-záéíóú]+(?:\s+[A-ZÁÉÍÓÚ][a-záéíóú]+)?):\s*(.+)$',
        re.MULTILINE
    )
    
    PATRON_ROL = re.compile(
        r'\b(Dr\.?|Dra\.?|Abogad[oa]|Juez|Jueza|Fiscal|Defensor[ao]?|Testigo|Moderador[ao]?|Expositor[ao]?)\b',
        re.IGNORECASE
    )
    
    def __init__(self, modo: str = 'auto'):
        """
        Inicializa el detector con un modo específico.
        
        Args:
            modo: 'tutorial', 'ateneo', 'legal', 'auto'
        """
        self.MODOS = obtener_modos()  # Cargar desde config_modos
        self.modo = modo if modo in self.MODOS else 'auto'
        self.config = self.MODOS[self.modo]
        self.hablantes: Dict[str, Hablante] = {}
        self.total_segmentos = 0
    
    def detectar(self, texto: str, segmentos: List[str] = None) -> List[Hablante]:
        """
        Detecta hablantes en el texto.
        
        Args:
            texto: Texto completo
            segmentos: Lista de segmentos (opcional)
            
        Returns:
            Lista de objetos Hablante
        """
        self.total_segmentos = len(segmentos) if segmentos else 75
        
        # 1. Detectar por patrón diálogo ("Nombre: texto")
        self._detectar_dialogos(texto)
        
        # 2. Detectar por nombre + profesión
        self._detectar_nombres_profesion(texto)
        
        # 3. Si modo legal y no hay hablantes, asignar anónimos
        if self.modo == 'legal' and not self.hablantes:
            self._asignar_anonimos(segmentos)
        
        # 4. Aplicar filtros según modo
        self._aplicar_filtros()
        
        return list(self.hablantes.values())
    
    def _detectar_dialogos(self, texto: str):
        """Detecta hablantes por patrón 'Nombre: texto'."""
        for match in self.PATRON_DIALOGO.finditer(texto):
            nombre = match.group(1).strip()
            self._agregar_hablante(nombre)
    
    def _detectar_nombres_profesion(self, texto: str):
        """Detecta hablantes por patrón 'Profesión + Nombre'."""
        for match in self.PATRON_NOMBRE_PROFESION.finditer(texto):
            nombre_completo = match.group(0).strip()
            rol = match.group(1) if match.lastindex else "desconocido"
            self._agregar_hablante(nombre_completo, rol)
        
        # Detectar testigos anónimos
        for match in self.PATRON_TESTIGO.finditer(texto):
            if self.modo == 'legal':
                self._agregar_hablante('testigo', 'testigo')
    
    def _agregar_hablante(self, nombre: str, rol: str = "desconocido"):
        """Agrega o actualiza un hablante."""
        if nombre not in self.hablantes:
            self.hablantes[nombre] = Hablante(
                nombre=nombre,
                rol=rol,
                segmentos=1,
                mencionado=False
            )
        else:
            self.hablantes[nombre].segmentos += 1
    
    def _asignar_anonimos(self, segmentos: List[str]):
        """Asigna hablantes anónimos {persona1, persona2, persona3}."""
        if not segmentos:
            return
        
        # Asignar números según longitud
        for i in range(min(3, len(segmentos))):
            nombre = f"persona{i+1}"
            self.hablantes[nombre] = Hablante(
                nombre=nombre,
                rol="anonimo",
                segmentos=1
            )
    
    def _aplicar_filtros(self):
        """Aplica filtros según configuración del modo."""
        # Calcular umbral de segmentos
        umbral = int(self.total_segmentos * self.config.umbral_segmentos)
        
        hablantes_filtrados = {}
        for nombre, hablante in self.hablantes.items():
            # Filtrar por umbral de segmentos
            if hablante.segmentos < umbral:
                continue
            
            # En modo tutorial, marcar menciones
            if self.modo == 'tutorial' and hablante.segmentos < umbral * 2:
                hablante.mencionado = True
                continue
            
            # Limitar máximo de hablantes
            if len(hablantes_filtrados) >= self.config.max_hablantes:
                break
            
            hablantes_filtrados[nombre] = hablante
        
        self.hablantes = hablantes_filtrados
        
        # Marcar hablante principal
        if self.hablantes:
            principal = max(self.hablantes.values(), key=lambda h: h.segmentos)
            principal.es_principal = True
    
    def obtener_resumen(self) -> Dict:
        """Retorna resumen de hablantes detectados."""
        return {
            'modo': self.modo,
            'total_hablantes': len(self.hablantes),
            'hablantes': [
                {
                    'nombre': h.nombre,
                    'rol': h.rol,
                    'segmentos': h.segmentos,
                    'es_principal': h.es_principal,
                    'mencionado': h.mencionado
                }
                for h in self.hablantes.values()
            ]
        }


# Test
if __name__ == '__main__':
    # Test tutorial (debería ignorar menciones)
    texto_tutorial = """
    En este tutorial vamos a aprender machine learning.
    Como dice la Abogada Ana Brusco en su paper...
    Python y PyTorch son las herramientas principales.
    """
    
    detector = DetectorHablantes(modo='tutorial')
    hablantes = detector.detectar(texto_tutorial, [''] * 75)
    print(f"📹 Modo tutorial: {len(hablantes)} hablantes")
    for h in hablantes:
        print(f"   {h.nombre} ({h.rol})")
    
    # Test legal (debería anonimizar)
    texto_legal = """
    Expediente 12345
    La Dra. María González presenta el caso.
    El Abogado Juan Pérez responde.
    La testigo declara los hechos.
    """
    
    detector_legal = DetectorHablantes(modo='legal')
    hablantes_legal = detector_legal.detectar(texto_legal, [''] * 100)
    print(f"\n⚖️ Modo legal: {len(hablantes_legal)} hablantes")
    for h in hablantes_legal:
        print(f"   {h.nombre} ({h.rol})")
