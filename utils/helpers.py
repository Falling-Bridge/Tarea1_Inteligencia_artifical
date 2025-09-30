import random
import time
import csv
import math

def medir_tiempo(func):
    """Decorador para medir el tiempo de ejecución de una función."""
    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = func(*args, **kwargs)
        fin = time.time()
        print(f"Tiempo de ejecución de {func.__name__}: {fin - inicio:.4f} segundos")
        return resultado
    return wrapper

def generar_semilla_aleatoria():
    """Genera una semilla aleatoria para reproducibilidad."""
    return random.randint(1, 10000)

def validar_parametros_laberinto(tamaño, densidad_muros, cantidad_salidas, prob_mover_muro):
    """Valida que los parámetros del laberinto sean correctos."""
    assert tamaño > 0, "El tamaño debe ser mayor a 0"
    assert 0 <= densidad_muros <= 1, "La densidad de muros debe estar entre 0 y 1"
    assert cantidad_salidas > 0, "Debe haber al menos una salida"
    assert 0 <= prob_mover_muro <= 1, "La probabilidad de mover muro debe estar entre 0 y 1"
    
    max_salidas_posibles = 2 * tamaño - 1
    assert cantidad_salidas <= max_salidas_posibles, f"Máximo {max_salidas_posibles} salidas para tamaño {tamaño}"

def calcular_distancia_manhattan(p1, p2):
    """Calcula la distancia Manhattan entre dos puntos."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def obtener_entero(mensaje, min_val=1, max_val=1000, default=None, mostrar_rango=True):
    """Obtiene un número entero del usuario con validación."""
    rango_texto = f" ({min_val}-{max_val})" if mostrar_rango else ""
    
    while True:
        try:
            if default is not None:
                entrada = input(f"{mensaje}{rango_texto} [{default}]: ").strip()
                if entrada == "":
                    return default
            else:
                entrada = input(f"{mensaje}{rango_texto}: ").strip()
            
            valor = int(entrada)
            if min_val <= valor <= max_val:
                return valor
            else:
                print(f"Error: El valor debe estar entre {min_val} y {max_val}")
        except ValueError:
            print("Error: Por favor ingrese un número entero válido")
        except KeyboardInterrupt:
            print("\n\nSaliendo del programa...")
            exit()

def obtener_float(mensaje, min_val=0.0, max_val=1.0, default=None, mostrar_rango=True):
    """Obtiene un número decimal del usuario con validación."""
    rango_texto = f" ({min_val}-{max_val})" if mostrar_rango else ""
    
    while True:
        try:
            if default is not None:
                entrada = input(f"{mensaje}{rango_texto} [{default}]: ").strip()
                if entrada == "":
                    return default
            else:
                entrada = input(f"{mensaje}{rango_texto}: ").strip()
            
            valor = float(entrada)
            if min_val <= valor <= max_val:
                return valor
            else:
                print(f"Error: El valor debe estar entre {min_val} y {max_val}")
        except ValueError:
            print("Error: Por favor ingrese un número decimal válido")
        except KeyboardInterrupt:
            print("\n\nSaliendo del programa...")
            exit()

def clear_screen():
    """Limpia la pantalla de la consola."""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def obtener_semilla_configuracion():
    """Pregunta al usuario si quiere semilla fija o aleatoria."""
    print("\n--- Configuración de Semilla ---")
    print("1. Semilla aleatoria (cada ejecución es diferente)")
    print("2. Semilla fija (reproducible)")
    
    opcion = input("Seleccione opción [1]: ").strip()
    
    if opcion == "2":
        return obtener_entero("Ingrese semilla fija", 1, 10000, 42)
    else:
        return None  # None indica semilla aleatoria

def generar_configuracion_aleatoria(config_random, semilla_base=None):
    """Genera una configuración aleatoria según los parámetros dados."""
    # Usar semilla si se proporciona
    if semilla_base is not None:
        random.seed(semilla_base)
    
    # Tamaño en múltiplos de 10 entre tamaño_min y tamaño_max
    tamaño_opciones = list(range(
        config_random['tamaño_min'], 
        config_random['tamaño_max'] + 1, 
        config_random['tamaño_step']
    ))
    tamaño = random.choice(tamaño_opciones)
    
    # Densidad entre densidad_min y densidad_max
    densidad = round(random.uniform(
        config_random['densidad_min'], 
        config_random['densidad_max']
    ), 2)
    
    # Probabilidad de mover muro entre wall_move_prob_min y wall_move_prob_max
    prob_mover_muro = round(random.uniform(
        config_random['wall_move_prob_min'], 
        config_random['wall_move_prob_max']
    ), 2)
    
    # Calcular cantidad de salidas: size/10 + 1 (mínimo 2, máximo según límites del laberinto)
    cantidad_salidas_base = max(2, math.ceil(tamaño / 10) + 1)
    max_salidas_posibles = min(15, 2 * tamaño - 1)  # Máximo 15 salidas o menos por restricciones
    cantidad_salidas = min(cantidad_salidas_base, max_salidas_posibles)
    
    # Longitud del cromosoma basada en el tamaño
    longitud_cromosoma = tamaño * 3
    
    return {
        'tamaño': tamaño,
        'densidad_muros': densidad,
        'prob_mover_muro': prob_mover_muro,
        'cantidad_salidas': cantidad_salidas,
        'tamaño_poblacion': config_random['tamaño_poblacion'],
        'longitud_cromosoma': longitud_cromosoma,
        'max_generaciones': config_random['max_generaciones'],
        'repeticiones': config_random['repeticiones_por_config']
    }