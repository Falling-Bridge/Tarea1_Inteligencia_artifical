import time
import numpy as np
import random
from core.maze import Maze
from agents.search_agent import SearchAgent
from agents.genetic_agent import GeneticAgent
from utils.metrics import exportar_resultados

class Experimentador:

    def __init__(self, result_collector=None):
        self.resultados = []
    
    def ejecutar_experimento(self, configuracion):
        """Ejecuta un experimento con la configuración dada."""
        print(f"Ejecutando experimento: {configuracion['nombre']}")
        
        resultados_experimento = {
            'configuracion': configuracion,
            'busqueda': [],
            'genetico': []
        }
        
        # Determinar si usar semilla fija o aleatoria
        semilla_base = configuracion.get('semilla_base')
        usar_semillas_fijas = semilla_base is not None
        
        if usar_semillas_fijas:
            print(f"Usando semilla base: {semilla_base} (reproducible)")
        else:
            print("Usando semillas aleatorias para cada repetición")
        
        for i in range(configuracion['repeticiones']):
            print(f"  Repetición {i+1}/{configuracion['repeticiones']}...")
            
            # Determinar la semilla para esta repetición
            if usar_semillas_fijas:
                semilla_actual = semilla_base + i
            else:
                semilla_actual = random.randint(1, 10000)
            
            laberinto = Maze(
                tamaño=configuracion['tamaño'],
                densidad_muros=configuracion['densidad_muros'],
                cantidad_salidas=configuracion['cantidad_salidas'],
                probabilidad_mover_muro=configuracion['prob_mover_muro'],
                semilla=semilla_actual
            )
            
            # Ejecutar algoritmo de búsqueda
            agente_busqueda = SearchAgent(laberinto)
            resultado_busqueda = agente_busqueda.ejecutar()
            resultados_experimento['busqueda'].append(resultado_busqueda)
            
            # Ejecutar algoritmo genético
            agente_genetico = GeneticAgent(
                laberinto,
                tamaño_poblacion=configuracion['tamaño_poblacion'],
                longitud_cromosoma=configuracion['longitud_cromosoma'],
                max_generaciones=configuracion['max_generaciones']
            )
            resultado_genetico = agente_genetico.ejecutar()
            resultados_experimento['genetico'].append(resultado_genetico)
            
            print(f"    Búsqueda - {resultado_busqueda.exito}, Genético - {resultado_genetico.exito}")
            
            if usar_semillas_fijas:
                print(f"    Semilla: {semilla_actual}")
            else:
                print(f"    Semilla aleatoria: {semilla_actual}")
        
        self.resultados.append(resultados_experimento)
        return resultados_experimento
    
    def generar_reporte(self):
        """Genera un reporte comparativo de todos los experimentos."""
        print("\n" + "="*60)
        print("REPORTE COMPARATIVO DE ALGORITMOS")
        print("="*60)
        
        for exp in self.resultados:
            config = exp['configuracion']
            print(f"\nExperimento: {config['nombre']}")
            print(f"Configuración: Tamaño={config['tamaño']}, "
                  f"Densidad={config['densidad_muros']}, "
                  f"Movimiento={config['prob_mover_muro']}")
            
            # Estadísticas búsqueda
            resultados_busqueda = exp['busqueda']
            exitos_busqueda = sum(1 for r in resultados_busqueda if r.exito)
            tiempo_busqueda = np.mean([r.tiempo_ejecucion for r in resultados_busqueda])
            caminos_exitosos_busqueda = [r.longitud_camino for r in resultados_busqueda if r.exito]
            longitud_busqueda = np.mean(caminos_exitosos_busqueda) if caminos_exitosos_busqueda else 0
            
            # Estadísticas genético
            resultados_genetico = exp['genetico']
            exitos_genetico = sum(1 for r in resultados_genetico if r.exito)
            tiempo_genetico = np.mean([r.tiempo_ejecucion for r in resultados_genetico])
            caminos_exitosos_genetico = [r.longitud_camino for r in resultados_genetico if r.exito]
            longitud_genetico = np.mean(caminos_exitosos_genetico) if caminos_exitosos_genetico else 0
            
            print(f"Búsqueda A*:   {exitos_busqueda}/{config['repeticiones']} exitos "
                  f"({exitos_busqueda/config['repeticiones']*100:.1f}%), "
                  f"Tiempo: {tiempo_busqueda:.4f}s, "
                  f"Longitud: {longitud_busqueda:.2f}")
            print(f"Algoritmo Genético: {exitos_genetico}/{config['repeticiones']} exitos "
                  f"({exitos_genetico/config['repeticiones']*100:.1f}%), "
                  f"Tiempo: {tiempo_genetico:.4f}s, "
                  f"Longitud: {longitud_genetico:.2f}")
        
    
    def exportar_resultados(self, archivo='resultados.csv'):
        """Exporta los resultados a un archivo CSV."""
        print("Exportando resultados tradicionales...")
        exportar_resultados(self.resultados, archivo)