import heapq
import time
from .base_agent import BaseAgent
from core.entities import ResultadoBusqueda

class SearchAgent(BaseAgent):
    """
    Agente que utiliza el algoritmo A* para encontrar la salida real del laberinto.
    """
    
    def __init__(self, laberinto):
        super().__init__(laberinto)
        self.posicion_actual = laberinto.inicio
        self.nodos_expandidos = 0
        
    def heuristica(self, posicion):
        """Heurística: distancia Manhattan a la salida real."""
        fila, columna = posicion
        salida_fila, salida_columna = self.laberinto.salida_real
        return abs(fila - salida_fila) + abs(columna - salida_columna)
    
    def a_estrella(self):
        """Implementación del algoritmo A*."""
        inicio = self.laberinto.inicio
        salida = self.laberinto.salida_real
        
        print(f"Buscando camino desde {inicio} hasta {salida}...")
        
        cola = [(0, 0, inicio, [])]
        visitados = set()
        mejor_g = {inicio: 0}
        
        while cola:
            f, g, actual, camino = heapq.heappop(cola)
            self.nodos_expandidos += 1
            
            if self.laberinto.tamaño > 30 and self.nodos_expandidos % 1000 == 0:
                print(f"Nodos expandidos: {self.nodos_expandidos}, Cola: {len(cola)}")
            
            if actual in visitados:
                continue
                
            visitados.add(actual)
            nuevo_camino = camino + [actual]
            
            if actual == salida:
                return nuevo_camino, True
            
            for vecino in self.laberinto.obtener_vecinos(actual):
                if vecino not in visitados:
                    nuevo_g = g + 1
                    if vecino not in mejor_g or nuevo_g < mejor_g[vecino]:
                        mejor_g[vecino] = nuevo_g
                        nuevo_f = nuevo_g + self.heuristica(vecino)
                        heapq.heappush(cola, (nuevo_f, nuevo_g, vecino, nuevo_camino))
        
        return [], False
    
    def ejecutar(self):
        """Ejecuta la búsqueda y devuelve estadísticas."""
        print(f"Ejecutando A* para laberinto {self.laberinto.tamaño}x{self.laberinto.tamaño}")
        inicio_tiempo = time.time()
        
        camino, exito = self.a_estrella()
        tiempo_ejecucion = time.time() - inicio_tiempo
        
        self.resultado = ResultadoBusqueda(
            exito=exito,
            longitud_camino=len(camino) if exito else 0,
            nodos_expandidos=self.nodos_expandidos,
            tiempo_ejecucion=tiempo_ejecucion,
            camino=camino
        )
        
        print(f"Búsqueda A* completada en {tiempo_ejecucion:.2f}s")
        print(f"Nodos expandidos: {self.nodos_expandidos}")
        print(f"Éxito: {exito}")
        
        return self.resultado