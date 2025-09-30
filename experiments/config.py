"""Configuraciones predefinidas para experimentos."""

CONFIGURACIONES_PREDEFINIDAS = [
    {
        'nombre': '10x10_den:0.2_move:0.1',
        'tamaño': 10,
        'densidad_muros': 0.2,
        'cantidad_salidas': 3,
        'prob_mover_muro': 0.1,
        'repeticiones': 5,
        'semilla_base': None,  # Siempre aleatorio
        'tamaño_poblacion': 50,
        'longitud_cromosoma': 30,
        'max_generaciones': 50
    },
    {
        'nombre': '30x30_den:0.25_move:0.1',
        'tamaño': 30,
        'densidad_muros': 0.25,
        'cantidad_salidas': 5,
        'prob_mover_muro': 0.1,
        'repeticiones': 3,
        'semilla_base': None,  # Siempre aleatorio
        'tamaño_poblacion': 100,
        'longitud_cromosoma': 80,
        'max_generaciones': 100
    },
    {
        'nombre': '50x50_den:0.3_move:0.05',
        'tamaño': 50,
        'densidad_muros': 0.3,
        'cantidad_salidas': 8,
        'prob_mover_muro': 0.05,
        'repeticiones': 2,
        'semilla_base': None,  # Siempre aleatorio
        'tamaño_poblacion': 150,
        'longitud_cromosoma': 120,
        'max_generaciones': 150
    }
]

# Configuración para experimentos aleatorios
CONFIG_RANDOM = {
    'tamaño_min': 10,
    'tamaño_max': 100,
    'tamaño_step': 10,  # Múltiplos de 10
    'densidad_min': 0.1,
    'densidad_max': 0.5,
    'wall_move_prob_min': 0.1,
    'wall_move_prob_max': 0.5,
    'tamaño_poblacion': 100,
    'max_generaciones': 200,
    'repeticiones_por_config': 3,  # Cuántas veces repetir cada configuración aleatoria
    'total_experimentos': 10  # Cuántas configuraciones aleatorias diferentes generar
}