# 🔍 Tarea 1 - Inteligencia artificial

| Nombre | GitHub | Matrícula |
|--------|--------|-----------|
| Lucas Daniel Morales Oyanedel | [@Falling-Bridge](https://github.com/Falling-Bridge) | 2023441490 |

## Estructura del proyecto

```
├── .gitignore
├── agents
│   ├── base_agent.py
│   ├── genetic_agent.py
│   ├── search_agent.py
├── comparacion_algoritmos.png
├── core
│   ├── entities.py
│   ├── maze.py
├── experiments
│   ├── experimenter.py
├── main.py
├── requirements.txt
├── tree.py
├── utils
│   ├── helpers.py
│   ├── metrics.py
├── visualization
│   ├── plotter.py
```

---

## 📖 Descripción  

Este proyecto enfrenta a dos tipos de agentes dentro de un **laberinto mutante**:  
- Un **agente de búsqueda (A\*)**, que utiliza heurísticas para encontrar rutas óptimas.  
- Un **agente genético**, que explora posibles soluciones mediante evolución poblacional y funciones de *fitness*.  

El laberinto cambia dinámicamente: con cada paso del agente, algunos muros pueden desplazarse ortogonalmente, manteniéndose dentro de los límites. Además, existen múltiples salidas, pero solo una es la verdadera, mientras que las demás son falsas y conducen a callejones sin salida.  

---

## 🎮 Interfaz interactiva  

El programa ofrece un menú de interacción vía teclado con las siguientes opciones:  


```
ESCAPE DEL LABERINTO MUTANTE
============================

Opciones:
1. Demostración básica
2. Experimento personalizado
3. Experimentos predefinidos
4. Experimentos aleatorios
5. Salir

Seleccione una opción:
```
---
## ⚙️ Ejecución del programa  

Para ejecutar este programa

```
python main.py
```
o en su lugar

```
python3 main.py
```

Los gráficos se generan únicamente en los experimentos aleatorios, ya que se consideró que solo los experimentos personalizados y aleatorios aportan resultados relevantes para su visualización.

