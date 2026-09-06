#!/data/data/com.termux/files/usr/bin/python3
"""
Adapters por fuente para BrainHub.
Detecta el tipo de fuente y aplica el adapter correcto.
KISS: no reemplaza procesar, lo complementa.
"""

from typing import Optional, Dict


class AdaptersFuente:
    """Detecta y aplica adapters por tipo de fuente."""
    
    ADAPTERS = {
        'youtube': {
            'patron': 'youtu.be|youtube.com',
            'metodo': 'yt-dlp'
        },
        'github': {
            'patron': 'github.com',
            'metodo': 'git clone / raw'
        },
        'pdf': {
            'patron': '.pdf$',
            'metodo': 'pdftotext'
        },
        'texto': {
            'patron': '.txt$|.md$',
            'metodo': 'directo'
        }
    }
    
    def detectar_fuente(self, entrada: str) -> str:
        """
        Detecta el tipo de fuente.
        
        Returns:
            'youtube', 'github', 'pdf', 'texto' o 'desconocido'
        """
        import re
        
        for fuente, config in self.ADAPTERS.items():
            if re.search(config['patron'], entrada, re.IGNORECASE):
                return fuente
        
        return 'desconocido'
    
    def sugerir_procesamiento(self, entrada: str) -> Dict:
        """
        Sugiere cómo procesar la entrada.
        
        Returns:
            {'fuente': 'youtube', 'metodo': 'yt-dlp', 'comando': 'procesar URL'}
        """
        fuente = self.detectar_fuente(entrada)
        
        if fuente == 'youtube':
            return {
                'fuente': fuente,
                'metodo': 'yt-dlp',
                'comando': f'procesar "{entrada}"'
            }
        elif fuente == 'github':
            return {
                'fuente': fuente,
                'metodo': 'git clone',
                'comando': f'git clone "{entrada}" && analizar README.md'
            }
        elif fuente == 'texto':
            return {
                'fuente': fuente,
                'metodo': 'directo',
                'comando': f'analizar "{entrada}"'
            }
        elif fuente == 'pdf':
            return {
                'fuente': fuente,
                'metodo': 'pdftotext',
                'comando': f'pdftotext "{entrada}" && analizar texto.txt'
            }
        else:
            return {
                'fuente': fuente,
                'metodo': 'desconocido',
                'comando': 'revisar manualmente'
            }


if __name__ == '__main__':
    adapters = AdaptersFuente()
    
    tests = [
        'https://youtu.be/abc123',
        'https://github.com/usuario/repo',
        'archivo.pdf',
        'transcripcion.txt',
    ]
    
    print("🔌 DETECCIÓN DE FUENTES")
    for entrada in tests:
        resultado = adapters.sugerir_procesamiento(entrada)
        print(f"\n   {entrada}")
        print(f"   → {resultado['fuente']} ({resultado['metodo']})")
        print(f"   → {resultado['comando']}")
