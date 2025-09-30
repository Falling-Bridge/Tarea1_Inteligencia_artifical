"""Definición de constantes y entidades del sistema."""

# Estados de las celdas del laberinto
LIBRE = 0
MURO = 1
SALIDA_REAL = 2
SALIDA_FALSA = 3
INICIO = 9

# Direcciones de movimiento
MOVIMIENTOS = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # derecha, abajo, izquierda, arriba

class ResultadoBusqueda:
    """Contenedor para resultados de búsqueda."""
    
    def __init__(self, exito=False, longitud_camino=0, nodos_expandidos=0, 
                 tiempo_ejecucion=0.0, camino=None, fitness_final=0, generaciones=0):
        self.exito = exito
        self.longitud_camino = longitud_camino
        self.nodos_expandidos = nodos_expandidos
        self.tiempo_ejecucion = tiempo_ejecucion
        self.camino = camino or []
        self.fitness_final = fitness_final
        self.generaciones = generaciones