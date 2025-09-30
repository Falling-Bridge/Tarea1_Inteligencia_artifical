import matplotlib.pyplot as plt
import numpy as np

class Plotter:
    """Clase para generar gráficos de resultados."""
    
    @staticmethod
    def graficar_resultados(resultados):
        """Genera gráficos comparativos."""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # Usar nombres directamente sin formateo especial
        nombres = [exp['configuracion']['nombre'] for exp in resultados]
        
        # Tasa de éxito
        exitos_busqueda = [sum(1 for r in exp['busqueda'] if r.exito) / len(exp['busqueda']) 
                          for exp in resultados]
        exitos_genetico = [sum(1 for r in exp['genetico'] if r.exito) / len(exp['genetico']) 
                          for exp in resultados]
        
        x = np.arange(len(nombres))
        ax1.bar(x - 0.2, exitos_busqueda, 0.4, label='Búsqueda A*', alpha=0.7, color='skyblue')
        ax1.bar(x + 0.2, exitos_genetico, 0.4, label='Algoritmo Genético', alpha=0.7, color='lightcoral')
        ax1.set_xlabel('Configuración del Experimento')
        ax1.set_ylabel('Tasa de Éxito')
        ax1.set_title('Comparación de Tasa de Éxito')
        ax1.set_xticks(x)
        ax1.set_xticklabels(nombres, rotation=45, ha='right', fontsize=8)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Tiempo de ejecución
        tiempo_busqueda = [np.mean([r.tiempo_ejecucion for r in exp['busqueda']]) 
                          for exp in resultados]
        tiempo_genetico = [np.mean([r.tiempo_ejecucion for r in exp['genetico']]) 
                          for exp in resultados]
        
        ax2.bar(x - 0.2, tiempo_busqueda, 0.4, label='Búsqueda A*', alpha=0.7, color='skyblue')
        ax2.bar(x + 0.2, tiempo_genetico, 0.4, label='Algoritmo Genético', alpha=0.7, color='lightcoral')
        ax2.set_xlabel('Configuración del Experimento')
        ax2.set_ylabel('Tiempo (segundos)')
        ax2.set_title('Comparación de Tiempo de Ejecución')
        ax2.set_xticks(x)
        ax2.set_xticklabels(nombres, rotation=45, ha='right', fontsize=8)
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Longitud del camino (solo para éxitos)
        long_busqueda = []
        long_genetico = []
        
        for exp in resultados:
            # Para búsqueda A*
            caminos_exitosos_busqueda = [r.longitud_camino for r in exp['busqueda'] if r.exito]
            long_busqueda.append(np.mean(caminos_exitosos_busqueda) if caminos_exitosos_busqueda else 0)
            
            # Para algoritmo genético
            caminos_exitosos_genetico = [r.longitud_camino for r in exp['genetico'] if r.exito]
            long_genetico.append(np.mean(caminos_exitosos_genetico) if caminos_exitosos_genetico else 0)
        
        ax3.bar(x - 0.2, long_busqueda, 0.4, label='Búsqueda A*', alpha=0.7, color='skyblue')
        ax3.bar(x + 0.2, long_genetico, 0.4, label='Algoritmo Genético', alpha=0.7, color='lightcoral')
        ax3.set_xlabel('Configuración del Experimento')
        ax3.set_ylabel('Longitud del Camino')
        ax3.set_title('Comparación de Longitud del Camino (solo éxitos)')
        ax3.set_xticks(x)
        ax3.set_xticklabels(nombres, rotation=45, ha='right', fontsize=8)
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Eficiencia (éxito/tiempo)
        eficiencia_busqueda = [e/t if t > 0 else 0 for e, t in zip(exitos_busqueda, tiempo_busqueda)]
        eficiencia_genetico = [e/t if t > 0 else 0 for e, t in zip(exitos_genetico, tiempo_genetico)]
        
        ax4.bar(x - 0.2, eficiencia_busqueda, 0.4, label='Búsqueda A*', alpha=0.7, color='skyblue')
        ax4.bar(x + 0.2, eficiencia_genetico, 0.4, label='Algoritmo Genético', alpha=0.7, color='lightcoral')
        ax4.set_xlabel('Configuración del Experimento')
        ax4.set_ylabel('Eficiencia (Éxito/Tiempo)')
        ax4.set_title('Comparación de Eficiencia')
        ax4.set_xticks(x)
        ax4.set_xticklabels(nombres, rotation=45, ha='right', fontsize=8)
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('comparacion_algoritmos.png', dpi=300, bbox_inches='tight')
        plt.show()