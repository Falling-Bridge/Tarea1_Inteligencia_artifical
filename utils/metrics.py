import csv

def exportar_resultados(resultados, archivo='resultados.csv'):
    with open(archivo, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Experimento', 'Algoritmo', 'Exitos', 'Tasa_Exito', 
                        'Tiempo_Promedio', 'Longitud_Promedio'])
        
        for exp in resultados:
            config = exp['configuracion']
            nombre_exp = config['nombre']
            
            # Datos para búsqueda
            resultados_busqueda = exp['busqueda']
            exitos_busqueda = sum(1 for r in resultados_busqueda if r.exito)
            tasa_busqueda = exitos_busqueda / len(resultados_busqueda)
            tiempo_busqueda = sum(r.tiempo_ejecucion for r in resultados_busqueda) / len(resultados_busqueda)
            long_busqueda = sum(r.longitud_camino for r in resultados_busqueda if r.exito) / exitos_busqueda if exitos_busqueda > 0 else 0
            
            writer.writerow([nombre_exp, 'Busqueda_A*', exitos_busqueda, tasa_busqueda, 
                           tiempo_busqueda, long_busqueda])
            
            # Datos para genético
            resultados_genetico = exp['genetico']
            exitos_genetico = sum(1 for r in resultados_genetico if r.exito)
            tasa_genetico = exitos_genetico / len(resultados_genetico)
            tiempo_genetico = sum(r.tiempo_ejecucion for r in resultados_genetico) / len(resultados_genetico)
            long_genetico = sum(r.longitud_camino for r in resultados_genetico if r.exito) / exitos_genetico if exitos_genetico > 0 else 0
            
            writer.writerow([nombre_exp, 'Algoritmo_Genetico', exitos_genetico, tasa_genetico, 
                           tiempo_genetico, long_genetico])
    
    print(f"Resultados exportados a {archivo}")