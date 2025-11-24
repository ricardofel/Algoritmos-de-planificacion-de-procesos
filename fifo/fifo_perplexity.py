import matplotlib.pyplot as plt

# Definir los procesos con sus tiempos de llegada y ráfaga
procesos = [
    {'nombre': 'P1', 'llegada': 0, 'rafaga': 5},
    {'nombre': 'P2', 'llegada': 2, 'rafaga': 3},
    {'nombre': 'P3', 'llegada': 4, 'rafaga': 1},
    {'nombre': 'P4', 'llegada': 6, 'rafaga': 2}
]

# FIFO (First In First Out) - planificación por orden de llegada
tiempo_actual = 0
resultados = []

for p in procesos:
    inicio = max(tiempo_actual, p['llegada'])
    fin = inicio + p['rafaga']
    espera = inicio - p['llegada']
    retorno = fin - p['llegada']
    resultados.append({
        'Proceso': p['nombre'],
        'Llegada': p['llegada'],
        'Rafaga': p['rafaga'],
        'Inicio': inicio,
        'Fin': fin,
        'Espera': espera,
        'Retorno': retorno
    })
    tiempo_actual = fin

# Mostrar resultados
for r in resultados:
    print(r)

# Datos para el diagrama de Gantt
procesos_nombres = [r['Proceso'] for r in resultados]
inicio = [r['Inicio'] for r in resultados]
duracion = [r['Fin'] - r['Inicio'] for r in resultados]

# Crear diagrama de Gantt
fig, ax = plt.subplots(figsize=(8, 3))

for i, proc in enumerate(procesos_nombres):
    ax.barh(proc, duracion[i], left=inicio[i], height=0.5, color='skyblue')
    ax.text(inicio[i] + duracion[i] / 2, i, proc, va='center', ha='center', color='black')

ax.set_xlabel('Tiempo')
ax.set_ylabel('Procesos')
ax.set_xticks(range(0, max(inicio) + max(duracion) + 1))
ax.set_title('Diagrama de Gantt para FIFO')

plt.tight_layout()
plt.show()
