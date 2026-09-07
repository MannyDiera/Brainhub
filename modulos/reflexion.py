#!/data/data/com.termux/files/usr/bin/python3
"""
Reflexión post-análisis para BrainHub.
Genera insights sobre los resultados del análisis.
"""

from typing import Dict, List


class ReflexionPostAnalisis:
    """Genera reflexiones sobre resultados de análisis."""
    
    def reflexionar(self, analisis: Dict) -> List[str]:
        """
        Genera reflexiones sobre el análisis.
        
        Args:
            analisis: dict con terminos_clave, coocurrencias, nicho
            
        Returns:
            Lista de reflexiones
        """
        reflexiones = []
        
        terminos = analisis.get('terminos_clave', [])
        coocurrencias = analisis.get('coocurrencias', [])
        nicho = analisis.get('nicho', 'GENERAL')
        
        # 1. ¿Qué sorprende del análisis?
        if terminos:
            termino_top = terminos[0][0] if isinstance(terminos[0], (list, tuple)) else terminos[0]
            reflexiones.append(
                f"El término dominante es '{termino_top}', lo que sugiere "
                f"que el contenido gira en torno a ese concepto."
            )
        
        # 2. ¿Qué relaciones son más fuertes?
        if coocurrencias:
            par_top = coocurrencias[0]
            if isinstance(par_top, list) and len(par_top) >= 2:
                origen, destino = par_top[0]
                frecuencia = par_top[1]
                reflexiones.append(
                    f"La relación más fuerte es '{origen}' + '{destino}' "
                    f"({frecuencia} menciones), indicando que son conceptos "
                    f"centrales e interdependientes."
                )
        
        # 3. ¿Qué falta explorar?
        if nicho == 'TECNOLOGIA':
            reflexiones.append(
                "El contenido es técnico. Conviene explorar aplicaciones "
                "prácticas o casos de uso reales."
            )
        elif nicho == 'COMPRAS_PUBLICAS':
            reflexiones.append(
                "El contenido es de compras públicas. Explorar patrones "
                "de proveedores y procesos podría revelar insights."
            )
        
        # 4. ¿Qué sigue?
        reflexiones.append(
            "Sugerencia: generar documento 80/20 y preguntas de debate "
            "para profundizar el estudio."
        )
        
        return reflexiones


if __name__ == '__main__':
    # Test
    analisis = {
        'nicho': 'TECNOLOGIA',
        'terminos_clave': [('reflection', 45), ('documents', 41)],
        'coocurrencias': [[['reflection', 'documents'], 19]]
    }
    
    reflexion = ReflexionPostAnalisis()
    resultados = reflexion.reflexionar(analisis)
    
    print("🧠 REFLEXIONES POST-ANÁLISIS:")
    for i, r in enumerate(resultados, 1):
        print(f"\n   {i}. {r}")
