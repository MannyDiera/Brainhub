#!/usr/bin/env python3
"""
Módulo de validación de hablantes V1
"""

import re

def validar_hablante_con_dialogo(hablante, texto, contexto="", nombres_globales=None):
    combinado = texto.lower() + " " + contexto.lower()
    
    if nombres_globales:
        for nombre in nombres_globales:
            if nombre.lower() in combinado:
                patron_dialogo = rf'{re.escape(nombre)}\s*[:\-]'
                if not re.search(patron_dialogo, contexto, re.IGNORECASE):
                    return 'DESCONOCIDO'
    
    return hablante

def filtrar_hablantes_falsos(segmentos, texto_completo):
    patron = r'\b([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)+)\b'
    nombres_en_documento = set(re.findall(patron, texto_completo))
    
    palabras_comunes = {
        'When', 'The', 'And', 'Come', 'Can', 'Ten', 'Just', 'Like',
        'Because', 'But', 'If', 'Then', 'Now', 'Here', 'There'
    }
    nombres_validos = {n for n in nombres_en_documento if n not in palabras_comunes}
    
    for seg in segmentos:
        if seg['hablante'] not in ['DESCONOCIDO', 'NIÑO/A', 'PSICÓLOGO/A', 
                                     'ABOGADO/A', 'JUEZ / AUTORIDAD', 
                                     'POLICÍA / FISCAL', 'TESTIGO (HIJO/A)']:
            seg['hablante'] = validar_hablante_con_dialogo(
                seg['hablante'],
                seg['texto'],
                seg.get('contexto', ''),
                nombres_validos
            )
    
    return segmentos

if __name__ == "__main__":
    texto_test = "Ana Brusco: The minute she doesn't give you your daughter..."
    contexto_test = "Ana Brusco dice que vayas a la policía"
    
    resultado = validar_hablante_con_dialogo(
        'ABOGADA (Ana Brusco)',
        texto_test,
        contexto_test,
        {'Ana Brusco'}
    )
    print(f"Test: {resultado}")
