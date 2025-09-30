import random
import time
from .base_agent import BaseAgent
from core.entities import ResultadoBusqueda, MOVIMIENTOS

class GeneticAgent(BaseAgent):
    """
    Agente que utiliza un algoritmo genético para encontrar la salida del laberinto.
    """
    
    def __init__(self, laberinto, tamaño_poblacion=100, longitud_cromosoma=50, 
                 prob_mutacion=0.1, prob_cruce=0.8, max_generaciones=100):
        super().__init__(laberinto)
        self.tamaño_poblacion = tamaño_poblacion
        self.longitud_cromosoma = longitud_cromosoma
        self.prob_mutacion = prob_mutacion
        self.prob_cruce = prob_cruce
        self.max_generaciones = max_generaciones
        self.movimientos = MOVIMIENTOS
        
        if laberinto.tamaño > 50:
            self.longitud_cromosoma = max(longitud_cromosoma, laberinto.tamaño * 3)
            self.tamaño_poblacion = max(tamaño_poblacion, 200)
    
    def generar_cromosoma(self):
        """Genera un cromosoma aleatorio (secuencia de movimientos)."""
        return [random.randint(0, 3) for _ in range(self.longitud_cromosoma)]
    
    def calcular_fitness(self, cromosoma):
        """Calcula el fitness de un cromosoma."""
        posicion = self.laberinto.inicio
        pasos_validos = 0
        distancia_minima = float('inf')
        visitados = set([posicion])
        
        for movimiento in cromosoma:
            df, dc = self.movimientos[movimiento]
            nueva_pos = (posicion[0] + df, posicion[1] + dc)
            
            if self.laberinto.es_libre(nueva_pos):
                posicion = nueva_pos
                pasos_validos += 1
                visitados.add(posicion)
                
                distancia = abs(posicion[0] - self.laberinto.salida_real[0]) + \
                           abs(posicion[1] - self.laberinto.salida_real[1])
                distancia_minima = min(distancia_minima, distancia)
                
                if self.laberinto.es_salida_real(posicion):
                    return 10000 + (self.longitud_cromosoma - pasos_validos)
                elif self.laberinto.es_salida(posicion):
                    return 5000 + (self.longitud_cromosoma - pasos_validos)
            else:
                pasos_validos -= 0.5
        
        fitness_exploracion = len(visitados) * 2
        fitness = (self.longitud_cromosoma - distancia_minima) * 5 + pasos_validos + fitness_exploracion
        return max(fitness, 1)
    
    def seleccion_ruleta(self, poblacion, fitnesses):
        """Selección por ruleta."""
        total_fitness = sum(fitnesses)
        if total_fitness == 0:
            return random.choice(poblacion)
        
        punto = random.uniform(0, total_fitness)
        acumulado = 0
        
        for i, fitness in enumerate(fitnesses):
            acumulado += fitness
            if acumulado >= punto:
                return poblacion[i]
        
        return poblacion[-1]
    
    def cruce(self, padre1, padre2):
        """Cruce de un punto."""
        if random.random() < self.prob_cruce:
            punto = random.randint(1, self.longitud_cromosoma - 1)
            hijo1 = padre1[:punto] + padre2[punto:]
            hijo2 = padre2[:punto] + padre1[punto:]
            return hijo1, hijo2
        else:
            return padre1.copy(), padre2.copy()
    
    def mutacion(self, cromosoma):
        """Mutación de un gen aleatorio."""
        cromosoma_mutado = cromosoma.copy()
        for i in range(len(cromosoma_mutado)):
            if random.random() < self.prob_mutacion:
                cromosoma_mutado[i] = random.randint(0, 3)
        return cromosoma_mutado
    
    def ejecutar(self):
        """Ejecuta el algoritmo genético completo."""
        inicio_tiempo = time.time()
        
        poblacion = [self.generar_cromosoma() for _ in range(self.tamaño_poblacion)]
        mejor_fitness_historico = 0
        mejor_cromosoma = None
        generacion_mejor = 0
        
        print(f"Ejecutando algoritmo genético para laberinto {self.laberinto.tamaño}x{self.laberinto.tamaño}")
        print(f"Población: {self.tamaño_poblacion}, Cromosoma: {self.longitud_cromosoma}, Generaciones: {self.max_generaciones}")
        
        for generacion in range(self.max_generaciones):
            fitnesses = [self.calcular_fitness(ind) for ind in poblacion]
            
            max_fitness = max(fitnesses)
            if max_fitness > mejor_fitness_historico:
                mejor_fitness_historico = max_fitness
                mejor_cromosoma = poblacion[fitnesses.index(max_fitness)]
                generacion_mejor = generacion
            
            if generacion % 10 == 0:
                avg_fitness = sum(fitnesses) / len(fitnesses)
                print(f"Generación {generacion}: Mejor fitness = {mejor_fitness_historico:.1f}, Promedio = {avg_fitness:.1f}")
            
            if mejor_fitness_historico >= 10000:
                print(f"¡Solución encontrada en la generación {generacion}!")
                break
            
            nueva_poblacion = []
            
            if mejor_cromosoma:
                nueva_poblacion.append(mejor_cromosoma)
            
            while len(nueva_poblacion) < self.tamaño_poblacion:
                padre1 = self.seleccion_ruleta(poblacion, fitnesses)
                padre2 = self.seleccion_ruleta(poblacion, fitnesses)
                
                hijo1, hijo2 = self.cruce(padre1, padre2)
                hijo1 = self.mutacion(hijo1)
                hijo2 = self.mutacion(hijo2)
                
                nueva_poblacion.extend([hijo1, hijo2])
            
            poblacion = nueva_poblacion[:self.tamaño_poblacion]
        
        tiempo_ejecucion = time.time() - inicio_tiempo
        
        # Reconstruir el camino del mejor cromosoma
        camino = [self.laberinto.inicio]
        posicion = self.laberinto.inicio
        
        if mejor_cromosoma:
            for movimiento in mejor_cromosoma:
                df, dc = self.movimientos[movimiento]
                nueva_pos = (posicion[0] + df, posicion[1] + dc)
                if self.laberinto.es_libre(nueva_pos):
                    posicion = nueva_pos
                    camino.append(posicion)
                    
                    if self.laberinto.es_salida_real(posicion):
                        break
        
        self.resultado = ResultadoBusqueda(
            exito=mejor_fitness_historico >= 10000,
            longitud_camino=len(camino),
            fitness_final=mejor_fitness_historico,
            generaciones=min(generacion + 1, self.max_generaciones),
            tiempo_ejecucion=tiempo_ejecucion,
            camino=camino
        )
        
        print(f"Algoritmo genético completado en {tiempo_ejecucion:.2f}s")
        print(f"Mejor fitness: {mejor_fitness_historico:.1f} (encontrado en generación {generacion_mejor})")
        
        return self.resultado