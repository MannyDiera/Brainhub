#!/data/data/com.termux/files/usr/bin/python3
"""
Módulo de consolidación automática para DuckDB CLI.
Versión final con parser corregido para Termux.
"""

import json
import os
import sys
import subprocess
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

# Directorios del proyecto
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
DATA_DIR = PROJECT_DIR / 'data'
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Configuración
TERMUX_HOME = os.environ.get('HOME', '/data/data/com.termux/files/home')
DEFAULT_DB_PATH = DATA_DIR / 'nlp_ecosystem.duckdb'

class ConsolidarAuto:
    """Consolidación usando DuckDB CLI."""
    
    def __init__(self, db_path: str = None):
        """Inicializa usando CLI."""
        if db_path is None:
            db_path = DEFAULT_DB_PATH
        
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.duckdb_cli = 'duckdb'
        self.simple_schema = False
        
        # Verificar versión silenciosamente
        try:
            result = subprocess.run([self.duckdb_cli, '--version'],
                                  capture_output=True, text=True, timeout=5)
            if result.returncode != 0:
                print("❌ DuckDB CLI no funciona")
                sys.exit(1)
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)
        
        # Crear esquema
        self._initialize_schema()
    
    def _execute_sql(self, sql: str, timeout: int = 30) -> tuple:
        """Ejecuta SQL usando el CLI."""
        try:
            result = subprocess.run(
                [self.duckdb_cli, str(self.db_path)],
                input=sql,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return False, "", "Timeout"
        except Exception as e:
            return False, "", str(e)
    
    def _initialize_schema(self):
        """Crea el esquema base."""
        # Primero intentar con secuencias
        schema_sql = """
CREATE TABLE IF NOT EXISTS contenidos (
    content_id VARCHAR PRIMARY KEY,
    titulo VARCHAR,
    source_type VARCHAR,
    nicho VARCHAR,
    url VARCHAR,
    processed_at TIMESTAMP,
    pipeline_version VARCHAR,
    content_hash VARCHAR,
    metadata TEXT
);

CREATE SEQUENCE IF NOT EXISTS seq_entidades_id START 1;
CREATE TABLE IF NOT EXISTS entidades (
    id INTEGER DEFAULT nextval('seq_entidades_id') PRIMARY KEY,
    content_id VARCHAR,
    nombre VARCHAR,
    tipo VARCHAR,
    frecuencia INTEGER,
    grounding TEXT,
    metadata TEXT
);

CREATE SEQUENCE IF NOT EXISTS seq_relaciones_id START 1;
CREATE TABLE IF NOT EXISTS relaciones (
    id INTEGER DEFAULT nextval('seq_relaciones_id') PRIMARY KEY,
    content_id VARCHAR,
    entidad_origen VARCHAR,
    entidad_destino VARCHAR,
    tipo_relacion VARCHAR,
    peso FLOAT
);

CREATE INDEX IF NOT EXISTS idx_contenidos_nicho ON contenidos(nicho);
CREATE INDEX IF NOT EXISTS idx_contenidos_processed ON contenidos(processed_at);
"""
        
        success, output, error = self._execute_sql(schema_sql)
        if not success:
            # Si falla, intentar esquema simple sin IDs
            self.simple_schema = True
            schema_simple = """
CREATE TABLE IF NOT EXISTS contenidos (
    content_id VARCHAR PRIMARY KEY,
    titulo VARCHAR,
    source_type VARCHAR,
    nicho VARCHAR,
    url VARCHAR,
    processed_at TIMESTAMP,
    pipeline_version VARCHAR,
    content_hash VARCHAR,
    metadata TEXT
);

CREATE TABLE IF NOT EXISTS entidades (
    content_id VARCHAR,
    nombre VARCHAR,
    tipo VARCHAR,
    frecuencia INTEGER,
    grounding TEXT,
    metadata TEXT
);

CREATE TABLE IF NOT EXISTS relaciones (
    content_id VARCHAR,
    entidad_origen VARCHAR,
    entidad_destino VARCHAR,
    tipo_relacion VARCHAR,
    peso FLOAT
);
"""
            success, output, error = self._execute_sql(schema_simple)
            if not success:
                print(f"❌ Error fatal en esquema: {error}")
    
    def consolidar_contenido(self, content_data: Dict[str, Any]) -> bool:
        """Consolida un contenido procesado."""
        if 'content_id' not in content_data:
            print("❌ Falta content_id")
            return False
        
        try:
            content_id = content_data.get('content_id', '')
            titulo = self._escape_sql(content_data.get('titulo', 'Sin título'))
            source_type = content_data.get('source_type', 'desconocido')
            nicho = content_data.get('nicho', 'GENERAL')
            url = content_data.get('url', '')
            processed_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            pipeline_version = content_data.get('pipeline_version', '6.4')
            content_hash = content_data.get('content_hash', '')
            metadata = self._escape_sql(json.dumps(content_data.get('metadata', {}), ensure_ascii=False))
            
            sql_parts = []
            
            # Insertar contenido principal
            sql_parts.append(f"""
INSERT OR REPLACE INTO contenidos VALUES (
    '{content_id}', '{titulo}', '{source_type}', '{nicho}', '{url}',
    '{processed_at}', '{pipeline_version}', '{content_hash}', '{metadata}'
);""")
            
            # Eliminar y reinsertar entidades
            sql_parts.append(f"DELETE FROM entidades WHERE content_id = '{content_id}';")
            if 'entidades' in content_data:
                for entidad in content_data['entidades']:
                    nombre = self._escape_sql(entidad.get('nombre', ''))
                    tipo = entidad.get('tipo', 'desconocido')
                    frecuencia = entidad.get('frecuencia', 1)
                    grounding = self._escape_sql(entidad.get('grounding', ''))
                    ent_metadata = self._escape_sql(json.dumps(entidad.get('metadata', {}), ensure_ascii=False))
                    
                    if self.simple_schema:
                        sql_parts.append(f"""
INSERT INTO entidades (content_id, nombre, tipo, frecuencia, grounding, metadata)
VALUES ('{content_id}', '{nombre}', '{tipo}', {frecuencia}, '{grounding}', '{ent_metadata}');""")
                    else:
                        sql_parts.append(f"""
INSERT INTO entidades (content_id, nombre, tipo, frecuencia, grounding, metadata)
VALUES ('{content_id}', '{nombre}', '{tipo}', {frecuencia}, '{grounding}', '{ent_metadata}');""")
            
            # Eliminar y reinsertar relaciones
            sql_parts.append(f"DELETE FROM relaciones WHERE content_id = '{content_id}';")
            if 'relaciones' in content_data:
                for relacion in content_data['relaciones']:
                    origen = self._escape_sql(relacion.get('origen', ''))
                    destino = self._escape_sql(relacion.get('destino', ''))
                    tipo_rel = relacion.get('tipo', 'relacionado_con')
                    peso = relacion.get('peso', 1.0)
                    
                    if self.simple_schema:
                        sql_parts.append(f"""
INSERT INTO relaciones (content_id, entidad_origen, entidad_destino, tipo_relacion, peso)
VALUES ('{content_id}', '{origen}', '{destino}', '{tipo_rel}', {peso});""")
                    else:
                        sql_parts.append(f"""
INSERT INTO relaciones (content_id, entidad_origen, entidad_destino, tipo_relacion, peso)
VALUES ('{content_id}', '{origen}', '{destino}', '{tipo_rel}', {peso});""")
            
            # Ejecutar todo
            full_sql = "\n".join(sql_parts)
            success, output, error = self._execute_sql(full_sql)
            
            if success:
                return True
            else:
                print(f"❌ Error: {error}")
                return False
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def _escape_sql(self, text: str) -> str:
        """Escapa texto para SQL."""
        if text is None:
            return ''
        return str(text).replace("'", "''")
    
    def obtener_estadisticas(self) -> Dict[str, Any]:
        """Obtiene estadísticas usando modo CSV para mejor parsing."""
        stats = {}
        
        for tabla in ['contenidos', 'entidades', 'relaciones']:
            # Usar modo CSV para facilitar el parsing
            sql = f"SELECT COUNT(*) FROM {tabla};"
            success, output, error = self._execute_sql(sql)
            
            if success:
                # Buscar el último número en la salida
                numbers = re.findall(r'│\s*(\d+)\s*│', output)
                if numbers:
                    stats[f'total_{tabla}'] = int(numbers[0])
                else:
                    # Buscar cualquier número
                    all_numbers = re.findall(r'\d+', output)
                    if all_numbers:
                        # El count real suele ser el número después de los headers
                        stats[f'total_{tabla}'] = int(all_numbers[-1])
                    else:
                        stats[f'total_{tabla}'] = 0
            else:
                stats[f'total_{tabla}'] = 0
        
        return stats
    
    def consultar(self, sql: str) -> List:
        """Ejecuta una consulta SQL y retorna resultados limpios."""
        success, output, error = self._execute_sql(sql + "\n")
        if success:
            return self._parse_output_clean(output)
        else:
            print(f"❌ Error: {error}")
            return []
    
    def _parse_output_clean(self, output: str) -> List:
        """Parsea la salida del CLI de forma limpia."""
        lines = output.strip().split('\n')
        results = []
        headers = []
        
        for i, line in enumerate(lines):
            if '│' in line and '┌' not in line and '└' not in line and '├' not in line:
                parts = [p.strip() for p in line.split('│')]
                data = [p for p in parts if p and p != '│']
                
                if data:
                    # Primera línea con datos = headers
                    if not headers:
                        headers = data
                    else:
                        # Datos reales
                        results.append(data)
        
        return results
    
    def close(self):
        """No necesita cerrar nada para CLI."""
        pass

def integrar_con_analizar(content_data: Dict[str, Any]) -> bool:
    """Integra con el pipeline existente."""
    consolidar = ConsolidarAuto()
    try:
        success = consolidar.consolidar_contenido(content_data)
        if success:
            print(f"✅ {content_data.get('content_id')} consolidado en DuckDB")
        return success
    finally:
        consolidar.close()

if __name__ == "__main__":
    print("🚀 Test de DuckDB CLI")
    
    test_data = {
        'content_id': 'test_123',
        'titulo': 'Test DuckDB',
        'source_type': 'test',
        'nicho': 'TECNOLOGIA',
        'url': 'https://youtube.com/test',
        'entidades': [
            {'nombre': 'Python', 'tipo': 'lenguaje', 'frecuencia': 5},
            {'nombre': 'DuckDB', 'tipo': 'base_datos', 'frecuencia': 3}
        ],
        'relaciones': [
            {'origen': 'Python', 'destino': 'DuckDB', 'tipo': 'usa', 'peso': 0.8}
        ]
    }
    
    success = integrar_con_analizar(test_data)
    
    if success:
        consolidar = ConsolidarAuto()
        stats = consolidar.obtener_estadisticas()
        print(f"\n📊 Estadísticas reales:")
        for key, value in stats.items():
            print(f"   {key}: {value}")
        
        print("\n🔍 Verificación:")
        result = consolidar.consultar("SELECT content_id, titulo FROM contenidos")
        print(f"Contenidos: {result}")
        
        consolidar.close()
        print("\n✅ Test exitoso")
    else:
        print("\n❌ Test fallido")
