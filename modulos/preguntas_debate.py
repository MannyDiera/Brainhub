#!/data/data/com.termux/files/usr/bin/python3
"""
Generador de preguntas de debate para BrainHub.
Identifica tensiones entre nichos y genera preguntas estructuradas.
"""

from typing import Dict, List, Optional


class GeneradorPreguntas:
    """Genera preguntas de debate desde jerarquía de nichos."""
    
    # Palabras que indican gaps o problemas
    PALABRAS_GAP = [
        'error', 'límite', 'limite', 'riesgo', 'sesgo', 'pendiente',
        'costo', 'vulnerabilidad', 'problema', 'falla', 'fallo'
    ]
    
    # Plantillas de tensión
    PLANTILLAS_TENSION = {
        ('TECNOLOGIA', 'SALUD'): (
            "¿Hasta qué punto el uso de {herramienta} puede reemplazar "
            "la intuición del profesional en {nucleo}?"
        ),
        ('LEGAL', 'TECNOLOGIA'): (
            "Considerando la {contexto}, ¿cuáles son las responsabilidades "
            "normativas del equipo al procesar datos con {herramienta}?"
        ),
        ('FINANZAS', 'TECNOLOGIA'): (
            "¿Cómo justificar la inversión en {herramienta} frente a "
            "las restricciones del marco {contexto}?"
        ),
    }
    
    def __init__(self):
        self.preguntas = []
    
    def _detectar_gaps(self, texto: str) -> List[str]:
        """Detecta palabras de gap en el texto."""
        texto_lower = texto.lower()
        return [p for p in self.PALABRAS_GAP if p in texto_lower]
    
    def generar_por_tension(
        self,
        jerarquia: Dict,
        terminos_clave: List[str]
    ) -> List[Dict]:
        """
        Genera preguntas por intersección crítica entre nichos.
        
        Returns:
            Lista de {'tipo': 'Conceptual/Técnica', 'pregunta': '...'}
        """
        preguntas = []
        nicho_principal = jerarquia.get('nicho_principal', '')
        secundarios = jerarquia.get('secundarios', {})
        
        herramienta = secundarios.get('herramienta')
        contexto = secundarios.get('contexto')
        
        # Tensión Herramienta vs Núcleo
        if herramienta and nicho_principal:
            clave = (herramienta, nicho_principal)
            plantilla = self.PLANTILLAS_TENSION.get(clave)
            
            if plantilla:
                concepto_nucleo = terminos_clave[0] if terminos_clave else 'el diagnóstico'
                concepto_herramienta = terminos_clave[2] if len(terminos_clave) > 2 else herramienta.lower()
                
                pregunta = plantilla.format(
                    herramienta=concepto_herramienta,
                    nucleo=concepto_nucleo,
                    contexto=contexto or 'la normativa'
                )
                
                preguntas.append({
                    'tipo': 'Conceptual / Técnica',
                    'pregunta': pregunta
                })
        
        return preguntas
    
    def generar_por_gaps(
        self,
        texto: str,
        jerarquia: Dict
    ) -> List[Dict]:
        """Genera preguntas por vacíos de información."""
        preguntas = []
        gaps = self._detectar_gaps(texto)
        
        for gap in gaps:
            pregunta = (
                f"El recurso menciona problemas de {gap}. "
                f"¿Qué protocolos alternativos se deberían discutir "
                f"para mitigar este riesgo antes de una implementación real?"
            )
            
            preguntas.append({
                'tipo': 'Ética / Regulatoria',
                'pregunta': pregunta
            })
        
        return preguntas
    
    def generar_por_escalabilidad(
        self,
        jerarquia: Dict,
        terminos_clave: List[str]
    ) -> List[Dict]:
        """Genera preguntas por dilema ético/económico."""
        preguntas = []
        secundarios = jerarquia.get('secundarios', {})
        
        herramienta = secundarios.get('herramienta')
        contexto = secundarios.get('contexto')
        
        if herramienta and contexto:
            pregunta = (
                f"Si tuviéramos que escalar esta solución de {herramienta.lower()} "
                f"a nivel masivo, ¿cómo balancear la inversión requerida "
                f"frente a las restricciones del marco {contexto.lower()}?"
            )
            
            preguntas.append({
                'tipo': 'Práctica / Viabilidad',
                'pregunta': pregunta
            })
        
        return preguntas
    
    def generar(
        self,
        jerarquia: Dict,
        terminos_clave: List[str],
        texto_completo: str = ""
    ) -> Dict:
        """
        Genera banco completo de preguntas.
        
        Returns:
            {'recurso_id': '...', 'preguntas_debate': [...]}
        """
        self.preguntas = []
        
        # 1. Tensión entre nichos
        self.preguntas.extend(
            self.generar_por_tension(jerarquia, terminos_clave)
        )
        
        # 2. Gaps de información
        self.preguntas.extend(
            self.generar_por_gaps(texto_completo, jerarquia)
        )
        
        # 3. Escalabilidad
        self.preguntas.extend(
            self.generar_por_escalabilidad(jerarquia, terminos_clave)
        )
        
        return {
            'recurso_id': jerarquia.get('recurso_id', 'sin_id'),
            'preguntas_debate': self.preguntas
        }


if __name__ == '__main__':
    generador = GeneradorPreguntas()
    
    jerarquia = {
        'recurso_id': 'paper_01',
        'nicho_principal': 'SALUD',
        'secundarios': {
            'herramienta': 'TECNOLOGIA',
            'contexto': 'LEGAL'
        }
    }
    
    terminos = ['diagnóstico', 'paciente', 'machine learning', 'algoritmo']
    
    texto = """
    El sistema presenta una vulnerabilidad en el procesamiento de datos.
    Hay riesgo de sesgo en los resultados del modelo.
    """
    
    resultado = generador.generar(jerarquia, terminos, texto)
    
    print("🎯 PREGUNTAS DE DEBATE")
    print("=" * 50)
    
    for pregunta in resultado['preguntas_debate']:
        print(f"\n   [{pregunta['tipo']}]")
        print(f"   {pregunta['pregunta']}")
