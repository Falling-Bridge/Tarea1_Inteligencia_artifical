from core.maze import Maze
from agents.search_agent import SearchAgent
from agents.genetic_agent import GeneticAgent
from experiments.experimenter import Experimentador
from utils.helpers import (clear_screen, obtener_entero, obtener_float, 
                          obtener_semilla_configuracion, generar_configuracion_aleatoria)
import random
import math

# Configuraciones predefinidas
CONFIGURACIONES_PREDEFINIDAS = [
    {
        'nombre': 'Pequeño_BajaDensidad',
        'tamaño': 15,
        'densidad_muros': 0.1,
        'cantidad_salidas': math.ceil(15/10) + 2,  # 2 + 2 = 4
        'prob_mover_muro': 0.05,
        'tamaño_poblacion': 50,
        'longitud_cromosoma': 45,
        'max_generaciones': 50,
        'repeticiones': 3
    },
    {
        'nombre': 'Medio_MediaDensidad',
        'tamaño': 30,
        'densidad_muros': 0.2,
        'cantidad_salidas': math.ceil(30/10) + 2,  # 3 + 2 = 5
        'prob_mover_muro': 0.1,
        'tamaño_poblacion': 100,
        'longitud_cromosoma': 90,
        'max_generaciones': 100,
        'repeticiones': 3
    },
    {
        'nombre': 'Grande_AltaDensidad',
        'tamaño': 50,
        'densidad_muros': 0.3,
        'cantidad_salidas': math.ceil(50/10) + 2,  # 5 + 2 = 7
        'prob_mover_muro': 0.15,
        'tamaño_poblacion': 150,
        'longitud_cromosoma': 150,
        'max_generaciones': 150,
        'repeticiones': 3
    }
]

def configuracion_personalizada():
    """Permite al usuario configurar todos los parámetros del laberinto."""
    print("\n" + "="*50)
    print("CONFIGURACIÓN PERSONALIZADA DEL LABERINTO")
    print("="*50)
    
    config = {}
    
    # Parámetros del laberinto
    config['tamaño'] = obtener_entero(
        "Tamaño del laberinto (N x N)", 
        min_val=10, 
        max_val=1000
    )
    
    max_salidas_posibles = min(100, 2 * config['tamaño'] - 1)
    config['cantidad_salidas'] = obtener_entero(
        f"Cantidad de salidas", 
        min_val=2, 
        max_val=max_salidas_posibles, 
        default=min(5, max_salidas_posibles)
    )
    
    config['densidad_muros'] = obtener_float(
        "Densidad de muros", 
        min_val=0.1, 
        max_val=0.5
    )
    
    config['prob_mover_muro'] = obtener_float(
        "Probabilidad de mover muros", 
        min_val=0.1, 
        max_val=0.4
    )
    
    print("\n--- Parámetros del Algoritmo Genético ---")
    config['tamaño_poblacion'] = obtener_entero(
        "Tamaño de la población", 
        min_val=100, 
        max_val=1000,
        default=200
    )
    
    config['longitud_cromosoma'] = obtener_entero(
        "Longitud del cromosoma", 
        min_val=10, 
        max_val=500, 
        default=50
    )
    
    config['max_generaciones'] = obtener_entero(
        "Máximo de generaciones", 
        min_val=10, 
        max_val=1000, 
        default=100
    )
    
    config['repeticiones'] = obtener_entero(
        "Número de repeticiones del experimento", 
        min_val=1, 
        max_val=100
    )
    
    # Configuración de semilla
    config['semilla_base'] = obtener_semilla_configuracion()
    
    return config

def demostracion_basica():
    """Demostración básica del funcionamiento del laberinto y agentes."""
    clear_screen()
    print("=== DEMOSTRACIÓN BÁSICA ===")
    
    tamaño = obtener_entero("Tamaño del laberinto para demostración", 10, 100, 15)
    salidas = obtener_entero("Cantidad de salidas", 2, min(100, 2*tamaño-1), 3)
    
    # Preguntar por semilla en demostración
    semilla = obtener_semilla_configuracion()
    if semilla is None:
        semilla = random.randint(1, 10000)
    
    laberinto = Maze(
        tamaño=tamaño,
        densidad_muros=0.2,
        cantidad_salidas=salidas,
        probabilidad_mover_muro=0.1,
        semilla=semilla
    )
    
    print(f"\nLaberinto {tamaño}x{tamaño} con {salidas} salidas:")
    print(f"Semilla: {semilla}")
    laberinto.mostrar()
    
    print("=== ALGORITMO DE BÚSQUEDA A* ===")
    agente_busqueda = SearchAgent(laberinto)
    resultado_busqueda = agente_busqueda.ejecutar()
    
    print(f"Éxito: {resultado_busqueda.exito}")
    print(f"Longitud del camino: {resultado_busqueda.longitud_camino}")
    print(f"Nodos expandidos: {resultado_busqueda.nodos_expandidos}")
    print(f"Tiempo de ejecución: {resultado_busqueda.tiempo_ejecucion:.4f}s")
    
    print("\n=== ALGORITMO GENÉTICO ===")
    agente_genetico = GeneticAgent(
        laberinto,
        tamaño_poblacion=50,
        longitud_cromosoma=min(50, tamaño * 3),
        max_generaciones=100
    )
    resultado_genetico = agente_genetico.ejecutar()
    
    print(f"Éxito: {resultado_genetico.exito}")
    print(f"Longitud del camino: {resultado_genetico.longitud_camino}")
    print(f"Fitness final: {resultado_genetico.fitness_final}")
    print(f"Generaciones: {resultado_genetico.generaciones}")
    print(f"Tiempo de ejecución: {resultado_genetico.tiempo_ejecucion:.4f}s")
    
    input("\nPresione Enter para continuar...")

def ejecutar_experimento_personalizado():
    """Ejecuta un experimento con configuración personalizada."""
    clear_screen()
    
    config = configuracion_personalizada()
    
    print(f"\nResumen de configuración:")
    print(f"  Tamaño del laberinto: {config['tamaño']}x{config['tamaño']}")
    print(f"  Cantidad de salidas: {config['cantidad_salidas']}")
    print(f"  Densidad de muros: {config['densidad_muros']}")
    print(f"  Probabilidad de mover muros: {config['prob_mover_muro']}")
    print(f"  Tamaño de población: {config['tamaño_poblacion']}")
    print(f"  Longitud de cromosoma: {config['longitud_cromosoma']}")
    print(f"  Máximo de generaciones: {config['max_generaciones']}")
    print(f"  Repeticiones: {config['repeticiones']}")
    if config['semilla_base'] is None:
        print(f"  Semilla: Aleatoria (diferente en cada ejecución)")
    else:
        print(f"  Semilla: Fija ({config['semilla_base']})")
    
    confirmar = input("\n¿Ejecutar experimento con esta configuración? (s/n): ").strip().lower()
    
    if confirmar in ['s', 'si', 'sí', 'y', 'yes']:
        experimentador = Experimentador()
        
        # Crear nombre simplificado
        nombre_experimento = f"{config['tamaño']}x{config['tamaño']}_den:{config['densidad_muros']:.1f}_move:{config['prob_mover_muro']:.1f}"
        
        config_experimento = {
            'nombre': nombre_experimento,
            'tamaño': config['tamaño'],
            'densidad_muros': config['densidad_muros'],
            'cantidad_salidas': config['cantidad_salidas'],
            'prob_mover_muro': config['prob_mover_muro'],
            'repeticiones': config['repeticiones'],
            'semilla_base': config['semilla_base'],
            'tamaño_poblacion': config['tamaño_poblacion'],
            'longitud_cromosoma': config['longitud_cromosoma'],
            'max_generaciones': config['max_generaciones']
        }
        
        print(f"\nEjecutando experimento: {nombre_experimento}")
        experimentador.ejecutar_experimento(config_experimento)
        experimentador.generar_reporte()
        
        from visualization.plotter import Plotter
        Plotter.graficar_resultados(experimentador.resultados)
        
        # Preguntar si exportar resultados
        exportar = input("\n¿Exportar resultados a CSV? (s/n): ").strip().lower()
        if exportar in ['s', 'si', 'sí', 'y', 'yes']:
            nombre_archivo = input("Nombre del archivo [resultados.csv]: ").strip()
            if not nombre_archivo:
                nombre_archivo = 'resultados.csv'
            experimentador.exportar_resultados(nombre_archivo)
        
        input("\nPresione Enter para continuar...")
    else:
        print("Experimento cancelado.")
        input("Presione Enter para continuar...")

def ejecutar_experimentos_predefinidos():
    """Ejecuta un conjunto de experimentos predefinidos."""
    clear_screen()
    print("=== EXPERIMENTOS PREDEFINIDOS ===")
    
    experimentador = Experimentador()
    
    print("Ejecutando experimentos predefinidos...")
    
    for config in CONFIGURACIONES_PREDEFINIDAS:
        # Preguntar por semilla para experimentos predefinidos
        semilla = obtener_semilla_configuracion()
        config['semilla_base'] = semilla
        
        experimentador.ejecutar_experimento(config)
    
    experimentador.generar_reporte()
    
    from visualization.plotter import Plotter
    Plotter.graficar_resultados(experimentador.resultados)
    
    # Exportar resultados
    exportar = input("\n¿Exportar resultados a CSV? (s/n): ").strip().lower()
    if exportar in ['s', 'si', 'sí', 'y', 'yes']:
        nombre_archivo = input("Nombre del archivo [resultados_predefinidos.csv]: ").strip()
        if not nombre_archivo:
            nombre_archivo = 'resultados_predefinidos.csv'
        experimentador.exportar_resultados(nombre_archivo)
        print(f"Resultados exportados a {nombre_archivo}")
    
    input("\nPresione Enter para continuar...")

def ejecutar_experimentos_aleatorios():
    """Ejecuta experimentos con parámetros aleatorios."""
    clear_screen()
    print("=== EXPERIMENTOS ALEATORIOS ===")
    print("Se generarán configuraciones aleatorias de laberintos y algoritmos.")
    print("\nParámetros aleatorios:")
    print(f"  - Tamaño: 10-100 (cualquier entero)")
    print(f"  - Cantidad de salidas: ceil(tamaño/10) + 2")
    print(f"  - Densidad de muros: 0.1-0.5")
    print(f"  - Prob. mover muros: 0.1-0.4")
    print(f"  - Población: 100")
    print(f"  - Generaciones: 200")
    print(f"  - Cromosoma: tamaño_laberinto * 3")
    
    total_experimentos = obtener_entero("Número de configuraciones aleatorias", 1, 20, 5)
    repeticiones = obtener_entero("Repeticiones por configuración", 1, 10, 3)
    
    print(f"\nSe ejecutarán {total_experimentos} configuraciones diferentes")
    print(f"con {repeticiones} repeticiones cada una.")
    
    confirmar = input("\n¿Ejecutar experimentos aleatorios? (s/n): ").strip().lower()
    
    if confirmar not in ['s', 'si', 'sí', 'y', 'yes']:
        print("Experimentos aleatorios cancelados.")
        input("Presione Enter para continuar...")
        return
    
    # Preguntar por semilla para la generación de configuraciones
    semilla_configs = obtener_semilla_configuracion()
    
    experimentador = Experimentador()
    
    print(f"\nGenerando {total_experimentos} configuraciones aleatorias...")
    
    for i in range(total_experimentos):
        config = generar_configuracion_aleatoria()
        config['repeticiones'] = repeticiones
        
        nombre_experimento = f"{config['tamaño']}x{config['tamaño']}-{config['densidad_muros']}-{config['prob_mover_muro']}"
        
        config_experimento = {
            'nombre': nombre_experimento,
            'tamaño': config['tamaño'],
            'densidad_muros': config['densidad_muros'],
            'cantidad_salidas': config['cantidad_salidas'],
            'prob_mover_muro': config['prob_mover_muro'],
            'repeticiones': config['repeticiones'],
            'semilla_base': semilla_configs,
            'tamaño_poblacion': config['tamaño_poblacion'],
            'longitud_cromosoma': config['longitud_cromosoma'],
            'max_generaciones': config['max_generaciones']
        }
        
        print(f"\n--- Configuración {i+1}/{total_experimentos} ---")
        print(f"  Tamaño: {config['tamaño']}x{config['tamaño']}")
        print(f"  Densidad: {config['densidad_muros']}")
        print(f"  Prob. mover muros: {config['prob_mover_muro']}")
        print(f"  Salidas: {config['cantidad_salidas']} (ceil({config['tamaño']}/10) + 2 = {math.ceil(config['tamaño']/10) + 2})")
        
        experimentador.ejecutar_experimento(config_experimento)
    
    print(f"\n{'='*60}")
    print("EXPERIMENTOS ALEATORIOS COMPLETADOS")
    print(f"{'='*60}")
    
    experimentador.generar_reporte()
    
    from visualization.plotter import Plotter
    Plotter.graficar_resultados(experimentador.resultados)
    
    # Exportar resultados
    exportar = input("\n¿Exportar resultados a CSV? (s/n): ").strip().lower()
    if exportar in ['s', 'si', 'sí', 'y', 'yes']:
        nombre_archivo = input("Nombre del archivo [resultados_aleatorios.csv]: ").strip()
        if not nombre_archivo:
            nombre_archivo = 'resultados_aleatorios.csv'
        experimentador.exportar_resultados(nombre_archivo)
        print(f"Resultados exportados a {nombre_archivo}")
    
    input("\nPresione Enter para continuar...")

def main():
    """Función principal."""
    while True:
        clear_screen()
        print("ESCAPE DEL LABERINTO MUTANTE")
        print("============================\n")
        
        print("Opciones:")
        print("1. Demostración básica")
        print("2. Experimento personalizado")
        print("3. Experimentos predefinidos")
        print("4. Experimentos aleatorios")
        print("5. Salir")
        
        opcion = input("\nSeleccione una opción: ").strip()
        
        if opcion == "1":
            demostracion_basica()
        elif opcion == "2":
            ejecutar_experimento_personalizado()
        elif opcion == "3":
            ejecutar_experimentos_predefinidos()
        elif opcion == "4":
            ejecutar_experimentos_aleatorios()
        elif opcion == "5":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intente nuevamente.")
            input("Presione Enter para continuar...")

if __name__ == "__main__":
    main()