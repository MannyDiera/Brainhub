#!/data/data/com.termux/files/usr/bin/python3
"""
Motor de etiquetas híbridas dinámicas para BrainHub.
Consulta diccionarios existentes: nichos_manager y diccionario_clinico.
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime

# Importar gestores existentes
try:
    from modulos.nichos_manager import NichosManager
except ImportError:
    NichosManager = None

try:
    from modulos.diccionario_clinico import DiccionarioClinico
except ImportError:
    DiccionarioClinico = None


class MotorEtiquetasHibridas:
    """Genera etiquetas híbridas usando diccionarios existentes."""
    
    # Raíces lingüísticas (solo nombres, no términos)
    RAICES = {
        'SALUD': 'HEALTH',
        'TECNOLOGIA': 'TECH',
        'FINANZAS': 'FIN',
        'LEGAL': 'LEGAL',
        'CIBERSEGURIDAD': 'SECURITY',
        'EDUCACION': 'EDU',
        'GENERAL': 'GEN'
    }
    
    CATALOGO_PATH = os.path.expanduser('~/proyectos/nlp/catalogo_hibridos.json')
    
    def __init__(self, umbral: float = 0.5):
        self.umbral = umbral
        self.catalogo = self._cargar_catalogo()
        
        # Cargar nichos desde gestor existente
        self.nichos_disponibles = []
        if NichosManager:
            manager = NichosManager()
            self.nichos_disponibles = manager.get_todos_nichos()
    
    def _cargar_catalogo(self) -> Dict:
        if os.path.exists(self.CATALOGO_PATH):
            with open(self.CATALOGO_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'hibridos': {}, 'pendientes_validacion': []}
    
    def _guardar_catalogo(self):
        with open(self.CATALOGO_PATH, 'w', encoding='utf-8') as f:
            json.dump(self.catalogo, f, indent=2, ensure_ascii=False)
    
    def _generar_nombre(self, nicho_a: str, nicho_b: str) -> str:
        """Genera nombre usando raíces."""
        raiz_a = self.RAICES.get(nicho_a, nicho_a[:4].upper())
        raiz_b = self.RAICES.get(nicho_b, nicho_b[:4].upper())
        return f"{raiz_a}-{raiz_b}"
    
    def generar_hibrido(self, nichos: Dict[str, float]) -> Optional[Dict]:
        """
        Genera etiqueta híbrida si dos nichos superan umbral.
        Los nichos vienen del análisis multietiqueta, no se recalculan.
        """
        nichos_altos = {
            n: c for n, c in nichos.items()
            if c >= self.umbral and n != 'GENERAL'
        }
        
        if len(nichos_altos) < 2:
            return None
        
        ordenados = sorted(nichos_altos.items(), key=lambda x: x[1], reverse=True)
        nicho_a, _ = ordenados[0]
        nicho_b, _ = ordenados[1]
        
        clave = frozenset([nicho_a, nicho_b])
        
        # Verificar si ya existe
        for nombre, datos in self.catalogo['hibridos'].items():
            if frozenset(datos['nichos']) == clave:
                return {'nombre': nombre, 'nichos': list(clave), 'nuevo': False}
        
        # Generar nuevo
        nombre = self._generar_nombre(nicho_a, nicho_b)
        
        self.catalogo['hibridos'][nombre] = {
            'nichos': list(clave),
            'validado': False,
            'fecha_creacion': None
        }
        self._guardar_catalogo()
        
        return {'nombre': nombre, 'nichos': list(clave), 'nuevo': True}
    
    def validar_hibrido(self, nombre: str) -> bool:
        if nombre in self.catalogo['hibridos']:
            self.catalogo['hibridos'][nombre]['validado'] = True
            self.catalogo['hibridos'][nombre]['fecha_creacion'] = datetime.now().isoformat()
            self._guardar_catalogo()
            return True
        return False
    
    def listar_hibridos(self) -> Dict:
        return self.catalogo['hibridos']


if __name__ == '__main__':
    motor = MotorEtiquetasHibridas()
    
    # Test
    tests = [
        {'SALUD': 0.85, 'TECNOLOGIA': 0.70},
        {'FINANZAS': 0.75, 'TECNOLOGIA': 0.65},
        {'LEGAL': 0.80, 'CIBERSEGURIDAD': 0.60},
    ]
    
    print("🏷️ MOTOR DE ETIQUETAS HÍBRIDAS")
    print(f"   Nichos disponibles: {motor.nichos_disponibles}")
    print("=" * 50)
    
    for confianzas in tests:
        resultado = motor.generar_hibrido(confianzas)
        if resultado:
            estado = "NUEVO" if resultado['nuevo'] else "EXISTENTE"
            print(f"\n   {resultado['nombre']} ({estado})")
            print(f"   Nichos: {', '.join(resultado['nichos'])}")
    
    print(f"\n📋 Catálogo:")
    for nombre, datos in motor.listar_hibridos().items():
        validado = "✅" if datos['validado'] else "⏳"
        print(f"   {validado} {nombre}")
