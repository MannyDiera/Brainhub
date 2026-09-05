import unicodedata
import re

# Palabras clave para cada nicho (usado por otros módulos)
NICHO_KEYWORDS = {
    'SALUD': [
        'salud', 'epidemiologia', 'hospital', 'paciente', 'medicina',
        'medico', 'clinico', 'enfermedad', 'brote', 'diagnostico',
        'mortalidad', 'morbilidad', 'ligamento', 'cruzado', 'rodilla',
        'lesion', 'cirugia', 'tratamiento'
    ],
    'TECNOLOGIA': [
        'python', 'pytorch', 'machine learning', 'deep learning',
        'software', 'hardware', 'programming', 'code', 'developer',
        'api', 'database', 'server', 'cloud', 'devops'
    ],
    'LEGAL': [
        'judge', 'court', 'custody', 'law', 'attorney', 'legal', 'lawyer',
        'tribunal', 'juez', 'abogado', 'demanda', 'fiscal', 'sentencia'
    ],
    'CIBERSEGURIDAD': [
        'hack', 'security', 'breach', 'malware', 'phishing', 'firewall',
        'encryption', 'vulnerability', 'exploit', 'attack', 'network',
        'hacker', 'seguridad', 'ataque'
    ],
    'FINANZAS': [
        'investment', 'stock', 'market', 'trading', 'portfolio',
        'bitcoin', 'cryptocurrency', 'forex', 'bonds', 'etf'
    ]
}

PALABRAS_SALUD = set(NICHO_KEYWORDS['SALUD'])
PALABRAS_TECNOLOGIA = set(NICHO_KEYWORDS['TECNOLOGIA'])

def normalizar_texto(texto: str) -> str:
    texto = unicodedata.normalize("NFD", texto.lower())
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", texto).strip()

def detectar_nicho(texto: str) -> str:
    texto_normalizado = normalizar_texto(texto)
    if not texto_normalizado:
        return "GENERAL"
    
    # Salud
    if sum(1 for p in PALABRAS_SALUD if p in texto_normalizado) >= 1:
        return "SALUD"
    
    # Tecnologia
    if any(p in texto_normalizado for p in PALABRAS_TECNOLOGIA):
        return "TECNOLOGIA"
    
    return "GENERAL"
