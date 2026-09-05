#!/data/data/com.termux/files/usr/bin/python3
"""
Fuzzy matching para detección de nicho con tolerancia a errores.
"""

from difflib import SequenceMatcher


def fuzzy_match(termino: str, diccionario: dict, umbral: float = 0.6) -> str:
    """
    Encuentra la mejor coincidencia difusa.
    
    Args:
        termino: Término a buscar
        diccionario: {termino_correcto: categoria}
        umbral: Mínimo ratio de similitud (0-1)
    
    Returns:
        Categoría si hay match, 'GENERAL' si no
    """
    mejor_ratio = 0
    mejor_termino = None
    
    for termino_correcto in diccionario:
        ratio = SequenceMatcher(None, termino.lower(), termino_correcto.lower()).ratio()
        if ratio > mejor_ratio:
            mejor_ratio = ratio
            mejor_termino = termino_correcto
    
    if mejor_ratio >= umbral and mejor_termino:
        return diccionario[mejor_termino]
    
    return 'GENERAL'


# Diccionario de nichos con términos
DICCIONARIO_NICHOS = {
    'machine learning': 'TECNOLOGIA',
    'deep learning': 'TECNOLOGIA',
    'inteligencia artificial': 'TECNOLOGIA',
    'historia clinica': 'SALUD',
    'diagnostico': 'SALUD',
    'tratamiento': 'SALUD',
    'expediente': 'LEGAL',
    'juzgado': 'LEGAL',
    'sentencia': 'LEGAL',
    'vulnerabilidad': 'CIBERSEGURIDAD',
    'hacker': 'CIBERSEGURIDAD',
    'phishing': 'CIBERSEGURIDAD',
    'inversion': 'FINANZAS',
    'acciones': 'FINANZAS',
    'mercado': 'FINANZAS'
}


def detectar_nicho_fuzzy(texto: str) -> str:
    """Detecta nicho con tolerancia a errores."""
    texto_lower = texto.lower()
    
    votos = {}
    
    # Buscar palabras individuales
    for palabra in texto_lower.split():
        categoria = fuzzy_match(palabra, DICCIONARIO_NICHOS)
        if categoria != 'GENERAL':
            votos[categoria] = votos.get(categoria, 0) + 1
    
    # Buscar bigramas (dos palabras)
    palabras = texto_lower.split()
    for i in range(len(palabras) - 1):
        bigrama = palabras[i] + ' ' + palabras[i+1]
        categoria = fuzzy_match(bigrama, DICCIONARIO_NICHOS)
        if categoria != 'GENERAL':
            votos[categoria] = votos.get(categoria, 0) + 2  # Bigrama pesa más
    
    if votos:
        return max(votos, key=votos.get)
    
    return 'GENERAL'


if __name__ == '__main__':
    # Test con errores de transcripción
    tests = [
        "machin lerning y deep lerning",
        "historia clinica del paciente",
        "vulnerabilidad en el sistem",
        "inversion en el mercdo"
    ]
    
    for texto in tests:
        nicho = detectar_nicho_fuzzy(texto)
        print(f"   '{texto}' → {nicho}")
