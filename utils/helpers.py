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

def generar_configuracion_aleatoria(semilla_base=None):
    """Genera una configuración aleatoria completa."""

    random.seed(semilla_base)
    
    tamaño = random.randint(10, 100)
    
    # Parámetros aleatorios
    densidad = round(random.uniform(0.1, 0.5), 2)
    prob_mover_muro = round(random.uniform(0.05, 0.4), 2)
    
    cantidad_salidas_base = math.ceil(tamaño / 10) + 2
    max_salidas_posibles = min(15, 2 * tamaño - 1)
    cantidad_salidas = min(cantidad_salidas_base, max_salidas_posibles)
    
    # Parámetros del algoritmo genético
    longitud_cromosoma = tamaño * 3
    
    return {
        'tamaño': tamaño,
        'densidad_muros': densidad,
        'prob_mover_muro': prob_mover_muro,
        'cantidad_salidas': cantidad_salidas,
        'tamaño_poblacion': 100,
        'longitud_cromosoma': longitud_cromosoma,
        'max_generaciones': 200,
        'repeticiones': 3
    }