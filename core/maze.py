import random
from .entities import LIBRE, MURO, SALIDA_REAL, SALIDA_FALSA, INICIO

class Maze:
    """
    Clase que representa un laberinto N x N con paredes móviles y múltiples salidas.
    """
    
    def __init__(self, tamaño, densidad_muros=0.2, cantidad_salidas=3, 
                 probabilidad_mover_muro=0.1, semilla=None):
        self.tamaño = tamaño
        self.densidad_muros = densidad_muros
        self.cantidad_salidas = cantidad_salidas
        self.probabilidad_mover_muro = probabilidad_mover_muro
        self.semilla = semilla

        self._validar_parametros()

        if semilla is not None:
            random.seed(semilla)

        self.grilla = self._generar_grilla()
        self.inicio = (0, 0)
        self.salidas = self._generar_salidas()

    def _validar_parametros(self):
        """Valida que los parámetros del laberinto sean correctos."""
        if self.tamaño < 10 or self.tamaño > 1000:
            raise ValueError("El tamaño debe estar entre 10 y 1000")
        
        if self.cantidad_salidas < 2 or self.cantidad_salidas > 100:
            raise ValueError("La cantidad de salidas debe estar entre 2 y 100")
        
        max_salidas_posibles = 2 * self.tamaño - 1
        if self.cantidad_salidas > max_salidas_posibles:
            raise ValueError(f"No se pueden tener más de {max_salidas_posibles} salidas")
        
        if not 0 <= self.densidad_muros <= 1:
            raise ValueError("La densidad de muros debe estar entre 0 y 1")
        
        if not 0 <= self.probabilidad_mover_muro <= 1:
            raise ValueError("La probabilidad de mover muro debe estar entre 0 y 1")

    def _generar_grilla(self):
        """Genera el laberinto inicial con muros aleatorios."""
        grilla = []
        for fila in range(self.tamaño):
            fila_actual = []
            for columna in range(self.tamaño):
                if (fila, columna) == (0, 0):
                    fila_actual.append(LIBRE)
                else:
                    fila_actual.append(MURO if random.random() < self.densidad_muros else LIBRE)
            grilla.append(fila_actual)
        return grilla

    def _generar_salidas(self):
        """Genera múltiples salidas, una real al azar."""
        posibles_salidas = [(fila, self.tamaño - 1) for fila in range(self.tamaño)] + \
                           [(self.tamaño - 1, columna) for columna in range(self.tamaño)]
        
        posibles_salidas = [pos for pos in posibles_salidas if pos != (0,0)]
        cantidad_salidas = min(self.cantidad_salidas, len(posibles_salidas))
        
        salidas_seleccionadas = random.sample(posibles_salidas, cantidad_salidas)
        self.salida_real = random.choice(salidas_seleccionadas)
        return salidas_seleccionadas

    def mover_muros(self):
        """Mueve algunos muros según la probabilidad definida."""
        for fila in range(self.tamaño):
            for columna in range(self.tamaño):
                if self.grilla[fila][columna] == MURO and random.random() < self.probabilidad_mover_muro:
                    nueva_fila = random.randint(0, self.tamaño-1)
                    nueva_columna = random.randint(0, self.tamaño-1)
                    if self.grilla[nueva_fila][nueva_columna] == LIBRE:
                        self.grilla[nueva_fila][nueva_columna] = MURO
                        self.grilla[fila][columna] = LIBRE

    def es_valida(self, posicion):
        """Verifica si una posición está dentro del laberinto."""
        fila, columna = posicion
        return 0 <= fila < self.tamaño and 0 <= columna < self.tamaño

    def es_libre(self, posicion):
        """Verifica si una posición está libre (no es muro)."""
        fila, columna = posicion
        return self.es_valida(posicion) and self.grilla[fila][columna] != MURO

    def es_salida(self, posicion):
        """Verifica si una posición es una salida."""
        return posicion in self.salidas

    def es_salida_real(self, posicion):
        """Verifica si una posición es la salida real."""
        return posicion == self.salida_real

    def obtener_vecinos(self, posicion):
        """Obtiene las posiciones vecinas válidas y libres."""
        from .entities import MOVIMIENTOS
        
        fila, columna = posicion
        vecinos = []
        
        for df, dc in MOVIMIENTOS:
            nueva_pos = (fila + df, columna + dc)
            if self.es_libre(nueva_pos):
                vecinos.append(nueva_pos)
        
        return vecinos

    def mostrar(self):
        """Muestra el laberinto en consola."""
        from .entities import SALIDA_FALSA, SALIDA_REAL, INICIO
        
        if self.tamaño > 20:
            print(f"Laberinto {self.tamaño}x{self.tamaño} (demasiado grande para mostrar)")
            print(f"Salida real: {self.salida_real}")
            print(f"Total de salidas: {len(self.salidas)}")
            return

        grilla_copia = [fila.copy() for fila in self.grilla]
        for fila_salida, columna_salida in self.salidas:
            valor = SALIDA_FALSA if (fila_salida, columna_salida) != self.salida_real else SALIDA_REAL
            grilla_copia[fila_salida][columna_salida] = valor
        grilla_copia[self.inicio[0]][self.inicio[1]] = INICIO

        nombres = {
            LIBRE: "/",
            MURO: "#",
            SALIDA_REAL: "&",
            SALIDA_FALSA: "?",
            INICIO: "0"
        }

        print(f"Laberinto {self.tamaño}x{self.tamaño} - Salida real: {self.salida_real}")
        for fila in grilla_copia:
            print(" ".join(nombres[c] for c in fila))
        print()