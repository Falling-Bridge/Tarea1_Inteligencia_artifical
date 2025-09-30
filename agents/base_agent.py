from abc import ABC, abstractmethod
from core.entities import ResultadoBusqueda

class BaseAgent(ABC):
    """Clase base abstracta para todos los agentes de búsqueda."""
    
    def __init__(self, laberinto):
        self.laberinto = laberinto
        self.resultado = ResultadoBusqueda()

    @abstractmethod
    def ejecutar(self):
        """Ejecuta el algoritmo de búsqueda."""
        pass

    def obtener_resultado(self):
        """Retorna el resultado de la búsqueda."""
        return self.resultado