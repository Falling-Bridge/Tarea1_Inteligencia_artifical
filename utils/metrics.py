import csv

def exportar_resultados(resultados, archivo='resultados.csv'):
    """Exporta los resultados a un archivo CSV."""
    with open(archivo, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Experimento', 'Algoritmo', 'Exitos', 'Tasa_Exito', 
                        'Tiempo_Promedio', 'Longitud_Promedio'])
        
        for exp in resultados:
            config = exp['configuracion']
            nombre_exp = config['nombre']
            
            # Datos para búsqueda
            exitos_busqueda = sum(1 for r in exp['busqueda'] if r['exito'])
            tasa_busqueda = exitos_busqueda / len(exp['busqueda'])
            tiempo_busqueda = sum(r['tiempo_ejecucion'] for r in exp['busqueda']) / len(exp['busqueda'])
            long_busqueda = sum(r['longitud_camino'] for r in exp['busqueda'] if r['exito'] or r['longitud_camino'] > 0) / len(exp['busqueda'])
            
            writer.writerow([nombre_exp, 'Busqueda_A*', exitos_busqueda, tasa_busqueda, 
                           tiempo_busqueda, long_busqueda])
            
            # Datos para genético
            exitos_genetico = sum(1 for r in exp['genetico'] if r['exito'])
            tasa_genetico = exitos_genetico / len(exp['genetico'])
            tiempo_genetico = sum(r['tiempo_ejecucion'] for r in exp['genetico']) / len(exp['genetico'])
            long_genetico = sum(r['longitud_camino'] for r in exp['genetico'] if r['exito'] or r['longitud_camino'] > 0) / len(exp['genetico'])
            
            writer.writerow([nombre_exp, 'Algoritmo_Genetico', exitos_genetico, tasa_genetico, 
                           tiempo_genetico, long_genetico])
    
    print(f"Resultados exportados a {archivo}")