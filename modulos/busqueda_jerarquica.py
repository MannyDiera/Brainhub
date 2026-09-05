#!/data/data/com.termux/files/usr/bin/python3
"""
Búsqueda jerárquica para BrainHub.
Filtra contenidos por nicho principal, herramienta y contexto.
"""

import os
import json
from typing import List, Dict, Optional


class BusquedaJerarquica:
    """Busca contenidos según jerarquía de nichos."""
    
    def __init__(self, directorio_busqueda: str = None):
        self.directorio = directorio_busqueda or os.path.expanduser('~')
    
    def buscar_jsons(self) -> List[str]:
        """Encuentra todos los JSON de análisis."""
        jsons = []
        for archivo in os.listdir(self.directorio):
            if archivo.endswith('_analisis_completo.json'):
                jsons.append(os.path.join(self.directorio, archivo))
        return jsons
    
    def filtrar(
        self,
        principal: str = None,
        herramienta: str = None,
        contexto: str = None
    ) -> List[Dict]:
        """
        Filtra contenidos por jerarquía.
        
        Args:
            principal: Nicho principal (ej. 'SALUD')
            herramienta: Nicho herramienta (ej. 'TECNOLOGIA')
            contexto: Nicho contexto (ej. 'LEGAL')
        
        Returns:
            Lista de contenidos que coinciden
        """
        resultados = []
        
        for json_path in self.buscar_jsons():
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                
                nicho = datos.get('nicho', 'GENERAL')
                nombre = os.path.basename(json_path).replace('_analisis_completo.json', '')
                
                # Aplicar filtros
                cumple = True
                
                if principal and nicho != principal:
                    cumple = False
                
                if herramienta and datos.get('herramienta') != herramienta:
                    cumple = False
                
                if contexto and datos.get('contexto') != contexto:
                    cumple = False
                
                if cumple:
                    resultados.append({
                        'contenido': nombre,
                        'nicho': nicho,
                        'herramienta': datos.get('herramienta', ''),
                        'contexto': datos.get('contexto', ''),
                        'terminos': len(datos.get('terminos_clave', []))
                    })
            
            except Exception:
                continue
        
        return resultados
    
    def resumen_por_nicho(self) -> Dict[str, int]:
        """Cuenta contenidos por nicho principal."""
        conteo = {}
        
        for json_path in self.buscar_jsons():
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                
                nicho = datos.get('nicho', 'GENERAL')
                conteo[nicho] = conteo.get(nicho, 0) + 1
            except Exception:
                continue
        
        return conteo


if __name__ == '__main__':
    buscador = BusquedaJerarquica()
    
    print("📊 RESUMEN POR NICHO")
    print("=" * 40)
    resumen = buscador.resumen_por_nicho()
    for nicho, cantidad in sorted(resumen.items(), key=lambda x: x[1], reverse=True):
        print(f"   {nicho:20s} {cantidad}")
    
    print(f"\n🔍 BUSCAR: SALUD")
    resultados = buscador.filtrar(principal='SALUD')
    for r in resultados[:10]:
        print(f"   {r['contenido']}")
