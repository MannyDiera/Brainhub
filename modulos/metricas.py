#!/data/data/com.termux/files/usr/bin/python3
"""
Métricas simples para BrainHub.
KISS: medir tiempo de cada etapa del pipeline.
"""

import time
import json
from typing import Dict


class MetricasPipeline:
    """Mide tiempo de ejecución de cada etapa."""
    
    def __init__(self):
        self.metricas = {}
        self.inicio_total = time.time()
    
    def medir(self, nombre: str):
        """Context manager para medir una etapa."""
        return _Medidor(self, nombre)
    
    def registrar(self, nombre: str, duracion: float):
        """Registra duración de una etapa."""
        self.metricas[nombre] = round(duracion, 3)
    
    def resumen(self) -> Dict:
        """Retorna resumen de métricas."""
        total = time.time() - self.inicio_total
        self.metricas['TOTAL'] = round(total, 3)
        self.metricas['suma_etapas'] = round(sum(
            v for k, v in self.metricas.items() if k != 'TOTAL'
        ), 3)
        return self.metricas
    
    def imprimir(self):
        """Imprime resumen en terminal."""
        print("\n📊 MÉTRICAS DE EJECUCIÓN")
        print("=" * 40)
        for etapa, duracion in self.metricas.items():
            print(f"   {etapa:30s} {duracion:>8.3f}s")
        
        total = self.metricas.get('TOTAL', sum(self.metricas.values()))
        print("-" * 40)
        print(f"   {'TOTAL':30s} {total:>8.3f}s")
        print("=" * 40)
    
    def exportar_json(self, ruta: str):
        """Exporta métricas a JSON."""
        with open(ruta, 'w', encoding='utf-8') as f:
            json.dump(self.resumen(), f, indent=2, ensure_ascii=False)
        print(f"✅ Métricas exportadas: {ruta}")


class _Medidor:
    """Context manager para medir."""
    
    def __init__(self, pipeline: MetricasPipeline, nombre: str):
        self.pipeline = pipeline
        self.nombre = nombre
        self.inicio = None
    
    def __enter__(self):
        self.inicio = time.time()
        return self
    
    def __exit__(self, *args):
        duracion = time.time() - self.inicio
        self.pipeline.registrar(self.nombre, duracion)


# Test
if __name__ == '__main__':
    metricas = MetricasPipeline()
    
    with metricas.medir('cargar_texto'):
        time.sleep(0.1)
    
    with metricas.medir('detectar_nicho'):
        time.sleep(0.05)
    
    with metricas.medir('filtrar_stopwords'):
        time.sleep(0.2)
    
    with metricas.medir('analizar_sentimiento'):
        time.sleep(0.3)
    
    metricas.imprimir()
