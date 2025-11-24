def round_robin(processes, quantum):
    n = len(processes)
    remaining_bt = [p[2] for p in processes]  # Burst Time restante
    t = 0  # tiempo actual
    finish_time = [0] * n
    
    # Cola de procesos (se agregan cuando llegan)
    queue = []
    visited = [False] * n
    completed = 0
    
    while completed < n:
        # Agregar procesos que llegan en el tiempo t
        for i in range(n):
            if processes[i][1] <= t and not visited[i]:
                queue.append(i)
                visited[i] = True
        
        if not queue:  
            t += 1
            continue
        
        # Obtener siguiente proceso en la cola
        idx = queue.pop(0)

        # Ejecutar el proceso
        exec_time = min(quantum, remaining_bt[idx])
        remaining_bt[idx] -= exec_time
        t += exec_time

        # Agregar procesos nuevos que llegaron durante la ejecución
        for i in range(n):
            if processes[i][1] <= t and not visited[i]:
                queue.append(i)
                visited[i] = True

        # Si el proceso no terminó, vuelve a la cola
        if remaining_bt[idx] > 0:
            queue.append(idx)
        else:
            finish_time[idx] = t
            completed += 1

    # Calcular tiempos
    turnaround = [finish_time[i] - processes[i][1] for i in range(n)]
    waiting = [turnaround[i] - processes[i][2] for i in range(n)]

    avg_turnaround = sum(turnaround) / n
    avg_waiting = sum(waiting) / n

    return waiting, turnaround, avg_waiting, avg_turnaround


# ------------------------------------------
# PROGRAMA PRINCIPAL
# ------------------------------------------

processes = []
n = int(input("Número de procesos: "))
quantum = int(input("Quantum: "))

for i in range(n):
    pid = input(f"\nID del Proceso {i+1}: ")
    arrival = int(input("Tiempo de llegada: "))
    burst = int(input("Tiempo de ráfaga: "))
    processes.append((pid, arrival, burst))

waiting, turnaround, avg_waiting, avg_turnaround = round_robin(processes, quantum)

print("\n--- RESULTADOS ---")
for i, p in enumerate(processes):
    print(f"Proceso {p[0]} | TE: {waiting[i]} | TR: {turnaround[i]}")

print(f"\nTiempo de Espera Promedio: {avg_waiting:.2f}")
print(f"Tiempo de Retorno Promedio: {avg_turnaround:.2f}")
