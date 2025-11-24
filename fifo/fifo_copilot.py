# Simulacion del algoritmo FIFO con tabla y diagrama de Gantt

# Lista de procesos: (nombre, llegada, rafaga)
procesos = [
    ("P1", 0, 5),
    ("P2", 2, 3),
    ("P3", 4, 1),
    ("P4", 6, 2)
]

# Inicializacion
tiempo_actual = 0
tabla = []
gantt = []

for nombre, llegada, rafaga in procesos:
    if tiempo_actual < llegada:
        tiempo_actual = llegada

    inicio = tiempo_actual
    fin = inicio + rafaga
    espera = inicio - llegada
    retorno = fin - llegada

    tabla.append((nombre, llegada, rafaga, inicio, fin, espera, retorno))
    gantt.append((nombre, inicio, fin))

    tiempo_actual = fin

# Mostrar tabla
print("\nTabla de ejecucion FIFO:")
print("Proceso | Llegada | Rafaga | Inicio | Fin | Espera | Retorno")
for fila in tabla:
    print("{:<7} | {:<7} | {:<6} | {:<6} | {:<3} | {:<6} | {:<7}".format(*fila))

# Calcular promedios
prom_espera = sum(f[5] for f in tabla) / len(tabla)
prom_retorno = sum(f[6] for f in tabla) / len(tabla)

print(f"\nTiempo de espera promedio: {prom_espera:.2f} unidades de tiempo")
print(f"Tiempo de retorno promedio: {prom_retorno:.2f} unidades de tiempo")

# Mostrar diagrama de Gantt
print("\nDiagrama de Gantt:")
for nombre, inicio, fin in gantt:
    print(f"| {nombre} ", end="")
print("|")

for nombre, inicio, fin in gantt:
    print(f"{inicio:<6}", end="")
print(f"{gantt[-1][2]:<6}")
