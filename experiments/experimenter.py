import time
import random
from core.maze import Maze
from agents.search_agent import SearchAgent
from agents.genetic_agent import GeneticAgent
from utils.metrics import exportar_resultados

class Experimentador:
    def __init__(self):
        self.resultados = []
    
    def ejecutar_experimento(self, configuracion):
        """Ejecuta un experimento con la configuración dada."""
        print(f"Ejecutando experimento: {configuracion['nombre']}")
        
        resultados_experimento = {
            'configuracion': configuracion,
            'busqueda': [],
            'genetico': []
        }
        
        semilla_base = configuracion.get('semilla_base')
        
        for i in range(configuracion['repeticiones']):
            print(f"  Repetición {i+1}/{configuracion['repeticiones']}...")
            
            # Determinar semilla para esta repetición
            if semilla_base is not None:
                semilla_actual = semilla_base + i
            else:
                semilla_actual = random.randint(1, 10000)
            
            # Crear laberinto
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
            
            print(f"    Búsqueda: {resultado_busqueda.exito}, Genético: {resultado_genetico.exito}")
        
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
            
            # Estadísticas búsqueda
            resultados_busqueda = exp['busqueda']
            exitos_busqueda = sum(1 for r in resultados_busqueda if r.exito)
            tiempo_busqueda = sum(r.tiempo_ejecucion for r in resultados_busqueda) / len(resultados_busqueda)
            
            # Estadísticas genético
            resultados_genetico = exp['genetico']
            exitos_genetico = sum(1 for r in resultados_genetico if r.exito)
            tiempo_genetico = sum(r.tiempo_ejecucion for r in resultados_genetico) / len(resultados_genetico)
            
            print(f"Búsqueda A*:   {exitos_busqueda}/{config['repeticiones']} exitos "
                  f"({exitos_busqueda/config['repeticiones']*100:.1f}%), "
                  f"Tiempo: {tiempo_busqueda:.4f}s")
            
            print(f"Algoritmo Genético: {exitos_genetico}/{config['repeticiones']} exitos "
                  f"({exitos_genetico/config['repeticiones']*100:.1f}%), "
                  f"Tiempo: {tiempo_genetico:.4f}s")
    
    def exportar_resultados(self, archivo='resultados.csv'):
        """Exporta los resultados a un archivo CSV."""
        exportar_resultados(self.resultados, archivo)