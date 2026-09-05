#!/data/data/com.termux/files/usr/bin/python3
"""
Genera visualización HTML interactiva del grafo.
Usa D3.js para mostrar el grafo en el navegador.
"""

import json
from pathlib import Path

PROJECT_DIR = Path(__file__).parent
GRAFO_JSON = PROJECT_DIR / 'outputs' / 'grafo' / 'grafo_ecosistema.json'
HTML_OUTPUT = PROJECT_DIR / 'outputs' / 'grafo' / 'grafo_interactivo.html'


def generar_html():
    """Genera HTML con visualización interactiva."""
    
    # Cargar grafo
    with open(GRAFO_JSON, 'r', encoding='utf-8') as f:
        grafo = json.load(f)
    
    nodos = grafo['nodos']
    aristas = grafo['aristas']
    
    # Preparar datos para D3
    nodos_json = json.dumps(nodos)
    aristas_json = json.dumps(aristas)
    
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grafo Ecosistema NLP</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        body {{
            margin: 0;
            font-family: -apple-system, sans-serif;
            background: #0f172a;
            color: #e2e8f0;
        }}
        #header {{
            padding: 20px;
            background: #1e293b;
            border-bottom: 1px solid #334155;
        }}
        h1 {{
            margin: 0;
            font-size: 1.5em;
            color: #60a5fa;
        }}
        #stats {{
            padding: 10px 20px;
            font-size: 0.9em;
            color: #94a3b8;
        }}
        #grafo {{
            width: 100%;
            height: calc(100vh - 100px);
        }}
        .nodo {{
            cursor: pointer;
        }}
        .nodo circle {{
            fill: #3b82f6;
            stroke: #60a5fa;
            stroke-width: 2px;
            transition: all 0.3s;
        }}
        .nodo:hover circle {{
            fill: #60a5fa;
            stroke: #93c5fd;
            stroke-width: 3px;
        }}
        .nodo text {{
            fill: #e2e8f0;
            font-size: 11px;
            pointer-events: none;
            text-anchor: middle;
        }}
        .arista {{
            stroke: #475569;
            stroke-opacity: 0.4;
            stroke-width: 1px;
        }}
        .arista:hover {{
            stroke: #60a5fa;
            stroke-opacity: 0.8;
        }}
        .tooltip {{
            position: absolute;
            background: #1e293b;
            border: 1px solid #60a5fa;
            border-radius: 8px;
            padding: 10px;
            pointer-events: none;
            font-size: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }}
    </style>
</head>
<body>
    <div id="header">
        <h1>🕸️ Grafo Ecosistema NLP</h1>
        <div id="stats">
            Nodos: {len(nodos)} | Relaciones: {len(aristas)}
        </div>
    </div>
    <div id="grafo"></div>

    <script>
        const nodos = {nodos_json};
        const aristas = {aristas_json};
        
        // Preparar datos para D3
        const nodes = nodos.map(n => ({{
            id: n.id,
            label: n.label,
            grado: 0
        }}));
        
        const links = aristas.map(a => ({{
            source: a.origen,
            target: a.destino,
            peso: a.peso,
            tipo: a.tipo
        }}));
        
        // Calcular grados
        links.forEach(l => {{
            const source = nodes.find(n => n.id === l.source);
            const target = nodes.find(n => n.id === l.target);
            if (source) source.grado++;
            if (target) target.grado++;
        }});
        
        // Configurar SVG
        const width = document.getElementById('grafo').clientWidth;
        const height = document.getElementById('grafo').clientHeight;
        
        const svg = d3.select('#grafo')
            .append('svg')
            .attr('width', width)
            .attr('height', height);
        
        // Simulación de fuerzas
        const simulation = d3.forceSimulation(nodes)
            .force('link', d3.forceLink(links)
                .id(d => d.id)
                .distance(d => 100 / Math.sqrt(d.peso))
                .strength(0.5))
            .force('charge', d3.forceManyBody()
                .strength(d => -50 - d.grado * 5))
            .force('center', d3.forceCenter(width / 2, height / 2))
            .force('collision', d3.forceCollide().radius(d => 20 + d.grado * 2));
        
        // Dibujar aristas
        const link = svg.append('g')
            .selectAll('line')
            .data(links)
            .enter()
            .append('line')
            .attr('class', 'arista')
            .attr('stroke-width', d => Math.min(d.peso, 5));
        
        // Tooltip
        const tooltip = d3.select('body')
            .append('div')
            .attr('class', 'tooltip')
            .style('opacity', 0);
        
        // Dibujar nodos
        const node = svg.append('g')
            .selectAll('g')
            .data(nodes)
            .enter()
            .append('g')
            .attr('class', 'nodo')
            .call(d3.drag()
                .on('start', dragstarted)
                .on('drag', dragged)
                .on('end', dragended));
        
        node.append('circle')
            .attr('r', d => 8 + d.grado * 0.8)
            .on('mouseover', function(event, d) {{
                tooltip.transition()
                    .duration(200)
                    .style('opacity', 1);
                tooltip.html(`<strong>${{d.label}}</strong><br>Conexiones: ${{d.grado}}`)
                    .style('left', (event.pageX + 10) + 'px')
                    .style('top', (event.pageY - 10) + 'px');
            }})
            .on('mouseout', function() {{
                tooltip.transition()
                    .duration(500)
                    .style('opacity', 0);
            }});
        
        node.append('text')
            .text(d => d.label)
            .attr('dy', -15);
        
        // Actualizar posiciones
        simulation.on('tick', () => {{
            link
                .attr('x1', d => d.source.x)
                .attr('y1', d => d.source.y)
                .attr('x2', d => d.target.x)
                .attr('y2', d => d.target.y);
            
            node.attr('transform', d => `translate(${{d.x}},${{d.y}})`);
        }});
        
        // Funciones de drag
        function dragstarted(event, d) {{
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }}
        
        function dragged(event, d) {{
            d.fx = event.x;
            d.fy = event.y;
        }}
        
        function dragended(event, d) {{
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        }}
    </script>
</body>
</html>"""
    
    HTML_OUTPUT.write_text(html, encoding='utf-8')
    print(f"✅ HTML generado: {HTML_OUTPUT}")
    print(f"   Abrir en navegador para ver el grafo interactivo")


if __name__ == '__main__':
    generar_html()
