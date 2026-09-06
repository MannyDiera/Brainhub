#!/data/data/com.termux/files/usr/bin/python3
"""
Schemas Pydantic para validar análisis de BrainHub.
Opcional: si Pydantic no está, usa dicts sin validar.
"""

try:
    from pydantic import BaseModel, Field
    PYDANTIC_DISPONIBLE = True
except ImportError:
    PYDANTIC_DISPONIBLE = False


class AnalisisCompleto(BaseModel):
    """Schema para validar análisis completo."""
    video_id: str = Field(default='', description='ID del contenido')
    nicho: str = Field(default='GENERAL')
    terminos_clave: list = Field(default_factory=list)
    sentimiento: float = Field(default=0.0)
    coocurrencias: list = Field(default_factory=list)
    total_segmentos: int = Field(default=0)
    pipeline_version: str = Field(default='6.5')


class TerminoClave(BaseModel):
    """Schema para término clave."""
    termino: str
    frecuencia: int = Field(default=1)


class Coocurrencia(BaseModel):
    """Schema para co-ocurrencia."""
    origen: str
    destino: str
    peso: float = Field(default=1.0)


def validar_analisis(datos: dict) -> dict:
    """
    Valida datos de análisis si Pydantic está disponible.
    Si no, retorna el dict sin validar (KISS).
    """
    if not PYDANTIC_DISPONIBLE:
        return datos
    
    try:
        schema = AnalisisCompleto(**datos)
        return schema.model_dump()
    except Exception as e:
        print(f"⚠️ Validación fallida: {e}")
        return datos


if __name__ == '__main__':
    # Test
    datos = {
        'video_id': 'test_01',
        'nicho': 'TECNOLOGIA',
        'terminos_clave': ['python', 'datos'],
        'sentimiento': 0.05,
        'total_segmentos': 100
    }
    
    if PYDANTIC_DISPONIBLE:
        validado = validar_analisis(datos)
        print(f"✅ Validado: {validado}")
    else:
        print("⚠️ Pydantic no instalado, usando dict sin validar")
        print(f"   Datos: {datos}")
