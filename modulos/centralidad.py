#!/data/data/com.termux/files/usr/bin/python3
"""
Centralidad de intermediación (Betweenness Centrality) para BrainHub.
Mide qué tan estratégico es un nodo como puente entre otros.
"""

from typing import Dict, List, Tuple
from collections import defaultdict, deque
import json


class BetweennessCentrality:
    """Calcula centralidad de intermediación en grafo no dirigido con pesos."""
    
    def __init__(self):
        self.grafo = defaultdict(dict)  # nodo -> {vecino: peso}
        self.nodos = set()
    
    def cargar_desde_json(self, ruta_json: str):
        """Carga grafo desde JSON de BrainHub."""
        with open(ruta_json, 'r', encoding='utf-8') as f:
            datos = json.load(f)
        
        for arista in datos.get('aristas', []):
            origen = arista['origen']
            destino = arista['destino']
            peso = arista.get('peso', 1.0)
            
            self.agregar_relacion(origen, destino, peso)
        
        return self
    
    def agregar_relacion(self, origen: str, destino: str, peso: float):
        """Agrega relación al grafo."""
        self.grafo[origen][destino] = peso
        self.grafo[destino][origen] = peso
        self.nodos.add(origen)
        self.nodos.add(destino)
    
    def _camino_mas_corto(self, origen: str, destino: str) -> List[List[str]]:
        """Encuentra todos los caminos más cortos entre origen y destino."""
        if origen == destino:
            return [[origen]]
        
        visited = {origen}
        queue = deque([(origen, [origen])])
        caminos = []
        distancia_minima = float('inf')
        
        while queue:
            nodo_actual, camino = queue.popleft()
            
            if len(camino) > distancia_minima:
                break
            
            if nodo_actual == destino:
                if len(camino) < distancia_minima:
                    distancia_minima = len(camino)
                    caminos = [camino]
                elif len(camino) == distancia_minima:
                    caminos.append(camino)
                continue
            
            for vecino in self.grafo.get(nodo_actual, {}):
                if vecino not in visited:
                    visited.add(vecino)
                    queue.append((vecino, camino + [vecino]))
        
        return caminos
    
    def calcular(self) -> Dict[str, float]:
        """
        Calcula betweenness centrality para todos los nodos.
        
        Returns:
            Dict con nodo -> centralidad normalizada (0-1)
        """
        betweenness = defaultdict(float)
        nodos_lista = list(self.nodos)
        
        total_pares = 0
        
        for i, origen in enumerate(nodos_lista):
            for destino in nodos_lista[i+1:]:
                caminos = self._camino_mas_corto(origen, destino)
                
                if not caminos:
                    continue
                
                total_caminos = len(caminos)
                total_pares += 1
                
                # Contar cuántos caminos pasan por cada nodo intermedio
                for camino in caminos:
                    nodos_intermedios = camino[1:-1]  # Excluir origen y destino
                    for nodo in set(nodos_intermedios):
                        betweenness[nodo] += 1.0 / total_caminos
        
        # Normalizar por total de pares
        if total_pares > 0:
            for nodo in betweenness:
                betweenness[nodo] /= total_pares
        
        return dict(betweenness)
    
    def top_centrales(self, n: int = 10) -> List[Tuple[str, float]]:
        """Retorna los n nodos más centrales."""
        centralidad = self.calcular()
        ordenados = sorted(centralidad.items(), key=lambda x: x[1], reverse=True)
        return ordenados[:n]
    
    def clasificar_puentes(self, umbral: float = 0.1) -> Dict[str, List[Dict]]:
        """
        Clasifica nodos según su rol en el grafo.
        
        Returns:
            Dict con categorías: 'monopolio', 'puente', 'periferico'
        """
        centralidad = self.calcular()
        
        clasificacion = {
            'monopolio': [],  # > 0.3
            'puente': [],     # 0.1 - 0.3
            'periferico': []  # < 0.1
        }
        
        for nodo, valor in centralidad.items():
            if valor > 0.3:
                clasificacion['monopolio'].append({'nodo': nodo, 'centralidad': round(valor, 3)})
            elif valor > 0.1:
                clasificacion['puente'].append({'nodo': nodo, 'centralidad': round(valor, 3)})
            else:
                clasificacion['periferico'].append({'nodo': nodo, 'centralidad': round(valor, 3)})
        
        for categoria in clasificacion:
            clasificacion[categoria] = sorted(
                clasificacion[categoria], 
                key=lambda x: x['centralidad'], 
                reverse=True
            )
        
        return clasificacion


# Test
if __name__ == '__main__':
    bc = BetweennessCentrality()
    
    # Grafo de ejemplo simple
    bc.agregar_relacion('datos', 'inteligencia', 9.5)
    bc.agregar_relacion('inteligencia', 'artificial', 15.0)
    bc.agregar_relacion('datos', 'salud', 5.0)
    bc.agregar_relacion('salud', 'paciente', 5.2)
    bc.agregar_relacion('datos', 'fabric', 4.8)
    
    centralidad = bc.calcular()
    
    print("📊 Centralidad de intermediación:")
    for nodo, valor in sorted(centralidad.items(), key=lambda x: x[1], reverse=True):
        print(f"   {nodo}: {valor:.3f}")
    
    print("\n🏆 Top centrales:")
    for nodo, valor in bc.top_centrales(3):
        print(f"   {nodo}: {valor:.3f}")
    
    print("\n📋 Clasificación:")
    clasificacion = bc.clasificar_puentes()
    for categoria, nodos in clasificacion.items():
        print(f"   {categoria}: {[n['nodo'] for n in nodos]}")
