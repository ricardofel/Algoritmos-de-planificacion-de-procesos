from collections import deque

class Proceso:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0

def calcular_round_robin(procesos, quantum):
    tiempo_actual = 0
    cola_listos = deque()
    procesos_completados = 0
    n = len(procesos)
    
    # Ordenamos por tiempo de llegada para simular correctamente la entrada
    procesos.sort(key=lambda x: x.arrival_time)
    
    # Índice para rastrear qué procesos del pool original ya han entrado a la cola
    indice_proceso = 0
    
    # Bucle principal de simulación
    while procesos_completados < n:
        # 1. Agregar procesos que han llegado hasta el tiempo actual a la cola
        while indice_proceso < n and procesos[indice_proceso].arrival_time <= tiempo_actual:
            cola_listos.append(procesos[indice_proceso])
            indice_proceso += 1
            
        # 2. Si la cola está vacía pero faltan procesos, saltar el tiempo (CPU Ociosa)
        if not cola_listos:
            if indice_proceso < n:
                tiempo_actual = procesos[indice_proceso].arrival_time
            continue

        # 3. Tomar el proceso al frente de la cola
        proceso_actual = cola_listos.popleft()
        
        # 4. Determinar tiempo de ejecución (Ráfaga restante o Quantum)
        tiempo_ejecucion = min(proceso_actual.remaining_time, quantum)
        
        # Simular paso del tiempo
        tiempo_actual += tiempo_ejecucion
        proceso_actual.remaining_time -= tiempo_ejecucion
        
        # 5. MUY IMPORTANTE: Verificar si llegaron nuevos procesos MIENTRAS este se ejecutaba
        while indice_proceso < n and procesos[indice_proceso].arrival_time <= tiempo_actual:
            cola_listos.append(procesos[indice_proceso])
            indice_proceso += 1
            
        # 6. Verificar si el proceso terminó o debe volver a la cola
        if proceso_actual.remaining_time == 0:
            # Proceso terminado
            procesos_completados += 1
            proceso_actual.completion_time = tiempo_actual
            # Cálculos finales
            proceso_actual.turnaround_time = proceso_actual.completion_time - proceso_actual.arrival_time
            proceso_actual.waiting_time = proceso_actual.turnaround_time - proceso_actual.burst_time
        else:
            # Proceso no terminado, regresa al final de la cola
            cola_listos.append(proceso_actual)

    return procesos

def main():
    print("--- Simulador Round Robin ---")
    try:
        quantum = int(input("Ingrese el valor del Quantum: "))
        n = int(input("Ingrese el número de procesos: "))
        lista_procesos = []

        print("\nIngrese los datos de los procesos:")
        for i in range(n):
            print(f"--- Proceso {i+1} ---")
            pid = input("  ID del proceso (ej. P1): ")
            at = int(input("  Tiempo de Llegada (AT): "))
            bt = int(input("  Ráfaga de CPU (BT): "))
            lista_procesos.append(Proceso(pid, at, bt))

        # Ejecutar algoritmo
        resultado = calcular_round_robin(lista_procesos, quantum)

        # Mostrar resultados
        print("\n" + "="*65)
        print(f"{'ID':<10} {'Llegada':<10} {'Ráfaga':<10} {'Retorno (TAT)':<15} {'Espera (WT)':<15}")
        print("-" * 65)

        total_tat = 0
        total_wt = 0

        # Ordenamos por ID o por orden de finalización para mostrar
        resultado.sort(key=lambda x: x.pid)

        for p in resultado:
            print(f"{p.pid:<10} {p.arrival_time:<10} {p.burst_time:<10} {p.turnaround_time:<15} {p.waiting_time:<15}")
            total_tat += p.turnaround_time
            total_wt += p.waiting_time

        avg_tat = total_tat / n
        avg_wt = total_wt / n

        print("="*65)
        print(f"Promedio Tiempo de Retorno (TAT): {avg_tat:.2f}")
        print(f"Promedio Tiempo de Espera (WT):   {avg_wt:.2f}")

    except ValueError:
        print("Error: Por favor ingrese números enteros válidos para los tiempos.")

if __name__ == "__main__":
    main()