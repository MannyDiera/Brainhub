#!/data/data/com.termux/files/usr/bin/python3
"""
Shadow Testing para BrainHub.
Compara versión actual vs versión nueva sin afectar producción.
"""

import json
import subprocess
from typing import Dict, List
from pathlib import Path


class ShadowTest:
    """Ejecuta pruebas de sombra para detectar regresiones."""
    
    def __init__(self):
        self.resultados = []
    
    def comparar_analisis(
        self,
        archivo_entrada: str,
        version_actual: str = 'analisis_completo_v6.5.py',
        version_nueva: str = None
    ) -> Dict:
        """
        Compara dos versiones del pipeline sobre el mismo archivo.
        
        Returns:
            {'diferencias': [...], 'regresion': bool}
        """
        import time
        
        # 1. Ejecutar versión actual
        inicio = time.time()
        resultado_actual = subprocess.run(
            ['python3', f'~/proyectos/nlp/{version_actual}', archivo_entrada],
            capture_output=True, text=True, timeout=60
        )
        tiempo_actual = time.time() - inicio
        
        # 2. Ejecutar versión nueva (si existe)
        if version_nueva:
            inicio = time.time()
            resultado_nueva = subprocess.run(
                ['python3', f'~/proyectos/nlp/{version_nueva}', archivo_entrada],
                capture_output=True, text=True, timeout=60
            )
            tiempo_nueva = time.time() - inicio
        else:
            return {'mensaje': 'No hay versión nueva para comparar'}
        
        # 3. Comparar resultados
        diferencias = self._comparar_salidas(
            resultado_actual.stdout,
            resultado_nueva.stdout
        )
        
        # 4. Comparar tiempos
        regresion_tiempo = tiempo_nueva > tiempo_actual * 1.5
        
        return {
            'tiempo_actual': round(tiempo_actual, 3),
            'tiempo_nueva': round(tiempo_nueva, 3),
            'regresion_tiempo': regresion_tiempo,
            'diferencias': diferencias,
            'regresion': len(diferencias) > 0 or regresion_tiempo
        }
    
    def _comparar_salidas(self, salida_a: str, salida_b: str) -> List[str]:
        """Compara salidas y detecta diferencias clave."""
        diferencias = []
        
        # Extraer nicho detectado
        nicho_a = self._extraer_nicho(salida_a)
        nicho_b = self._extraer_nicho(salida_b)
        
        if nicho_a != nicho_b:
            diferencias.append(f"Nicho cambió: {nicho_a} → {nicho_b}")
        
        # Extraer términos clave
        terminos_a = self._extraer_terminos(salida_a)
        terminos_b = self._extraer_terminos(salida_b)
        
        if terminos_a != terminos_b:
            diferencias.append(
                f"Términos cambiaron: {len(terminos_a)} → {len(terminos_b)}"
            )
        
        return diferencias
    
    def _extraer_nicho(self, salida: str) -> str:
        """Extrae nicho de la salida."""
        for linea in salida.split('\n'):
            if 'Nicho detectado' in linea:
                return linea.split(':')[-1].strip()
        return 'NO_DETECTADO'
    
    def _extraer_terminos(self, salida: str) -> List[str]:
        """Extrae términos clave de la salida."""
        terminos = []
        capturando = False
        
        for linea in salida.split('\n'):
            if 'Términos clave' in linea:
                capturando = True
                continue
            if capturando and linea.strip().startswith('-'):
                terminos.append(linea.strip())
            elif capturando and linea.strip() == '':
                break
        
        return terminos[:10]


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("❌ Uso: shadow_test.py archivo_entrada.txt [version_nueva.py]")
        sys.exit(1)
    
    archivo = sys.argv[1]
    version_nueva = sys.argv[2] if len(sys.argv) > 2 else None
    
    tester = ShadowTest()
    resultado = tester.comparar_analisis(archivo, version_nueva=version_nueva)
    
    print("🧪 SHADOW TESTING")
    print("=" * 50)
    
    if 'mensaje' in resultado:
        print(f"   {resultado['mensaje']}")
    else:
        print(f"   Tiempo actual: {resultado['tiempo_actual']}s")
        print(f"   Tiempo nueva: {resultado['tiempo_nueva']}s")
        print(f"   Regresión tiempo: {'⚠️ Sí' if resultado['regresion_tiempo'] else '✅ No'}")
        print(f"\n   Diferencias: {len(resultado['diferencias'])}")
        for dif in resultado['diferencias']:
            print(f"      • {dif}")
        
        print(f"\n   Resultado: {'⚠️ REGRESIÓN' if resultado['regresion'] else '✅ OK'}")
