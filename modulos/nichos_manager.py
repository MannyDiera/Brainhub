#!/data/data/com.termux/files/usr/bin/python3
"""
Gestor de diccionario de nichos desde JSON.
Similar a stopwords_manager.py y diccionario_clinico.py.
"""

import json
import os
from typing import Dict, List, Set


class NichosManager:
    """Gestiona el diccionario de nichos desde JSON."""
    
    DEFAULT_JSON_PATH = os.path.expanduser('~/proyectos/nlp/diccionario_nichos.json')
    
    def __init__(self, json_path: str = None):
        self.json_path = json_path or self.DEFAULT_JSON_PATH
        self._data = None
        self._load()
    
    def _load(self):
        """Carga diccionario de nichos desde JSON."""
        if not os.path.exists(self.json_path):
            print(f"⚠️ Diccionario no encontrado: {self.json_path}")
            self._data = {}
            return
        
        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                self._data = json.load(f)
            print(f"✅ Diccionario de nichos cargado: {len(self._data)} nichos")
        except json.JSONDecodeError as e:
            print(f"❌ Error al parsear JSON: {e}")
            self._data = {}
    
    def reload(self):
        """Recarga el diccionario."""
        self._load()
    
    def get_terminos(self, nicho: str) -> List[str]:
        """Retorna términos de un nicho."""
        if nicho in self._data:
            return self._data[nicho].get('terminos', [])
        return []
    
    def get_todos_nichos(self) -> List[str]:
        """Retorna todos los nichos disponibles."""
        return list(self._data.keys())
    
    def get_todos_terminos(self) -> Dict[str, List[str]]:
        """Retorna diccionario {nicho: [terminos]}."""
        return {
            nicho: self.get_terminos(nicho)
            for nicho in self.get_todos_nichos()
        }


if __name__ == '__main__':
    manager = NichosManager()
    
    print(f"\n📋 Nichos: {manager.get_todos_nichos()}")
    
    for nicho in manager.get_todos_nichos():
        terminos = manager.get_terminos(nicho)
        print(f"\n   {nicho} ({len(terminos)} términos):")
        print(f"      {', '.join(terminos[:5])}...")
