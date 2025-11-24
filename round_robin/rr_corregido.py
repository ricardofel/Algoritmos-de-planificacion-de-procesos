# Simulación del Algoritmo Round Robin (RR)
# Lenguaje: Python
# Autor: Grupo de Emilio Peña

def round_robin_final(procesos, quantum):
    # Variables de control de tiempo y colas
    tiempo_actual = 0
    cola_listos = []
    procesos_terminados = []
    secuencia_ejecucion = [] # Para el diagrama de Gantt
    n = len(procesos)
    
    # Hacemos una copia para no dañar los datos originales
    # Agregamos 'bt_restante' para controlar cuánto le falta a cada uno
    for p in procesos:
        p['bt_restante'] = p['bt']

    
    # Bucle principal: Se repite hasta que todos los procesos terminen
    while len(procesos_terminados) < n:
        
        # 1. Verificar llegadas: Metemos a la cola los que ya llegaron (AT <= tiempo)
        # Solo si no están ya en cola ni terminados
        for p in procesos:
            if p['at'] <= tiempo_actual and p not in cola_listos and p not in procesos_terminados:
                cola_listos.append(p)
        
        # Caso: CPU ocioso (nadie ha llegado aún)
        if not cola_listos:
            secuencia_ejecucion.append(("Ocioso", tiempo_actual, tiempo_actual + 1))
            tiempo_actual += 1
            continue

        # 2. Extraer el primer proceso de la cola (FIFO)
        proceso_actual = cola_listos.pop(0)
        
        # 3. Calcular tiempo de ejecución (Quantum vs Lo que le falta)
        tiempo_ejecucion = min(quantum, proceso_actual['bt_restante'])
        
        # Guardamos registro para el Gantt (Quien ejecuta, inicio, fin)
        secuencia_ejecucion.append((proceso_actual['id'], tiempo_actual, tiempo_actual + tiempo_ejecucion))
        
        # Avanzamos el reloj y reducimos la ráfaga
        tiempo_actual += tiempo_ejecucion
        proceso_actual['bt_restante'] -= tiempo_ejecucion
        
        # 4. Verificar si llegaron NUEVOS procesos MIENTRAS este se ejecutaba
        # Esto es CRÍTICO: Los nuevos deben entrar antes de que el actual regrese a la cola
        for p in procesos:
            if p['at'] <= tiempo_actual and p['at'] > (tiempo_actual - tiempo_ejecucion) and p not in cola_listos and p not in procesos_terminados and p != proceso_actual:
                cola_listos.append(p)

        # 5. Decisión: ¿Terminó o regresa a la cola?
        if proceso_actual['bt_restante'] == 0:
            # --- PROCESO TERMINADO ---
            proceso_actual['ct'] = tiempo_actual # Completion Time
            proceso_actual['tat'] = proceso_actual['ct'] - proceso_actual['at'] # Turn Around Time
            proceso_actual['wt'] = proceso_actual['tat'] - proceso_actual['bt'] # Waiting Time
            procesos_terminados.append(proceso_actual)
        else:
            # --- NO TERMINÓ, REGRESA A LA COLA ---
            cola_listos.append(proceso_actual)

    return procesos_terminados, secuencia_ejecucion

# --- DATOS DE PRUEBA (Input) ---
if __name__ == "__main__":
    # Definimos los procesos (ID, Llegada, Ráfaga)
    lista_procesos = [
        {'id': 'P1', 'at': 0, 'bt': 5},
        {'id': 'P2', 'at': 1, 'bt': 3},
        {'id': 'P3', 'at': 2, 'bt': 8},
        {'id': 'P4', 'at': 3, 'bt': 6}
    ]
    Q = 2 # Quantum

    print(f"--- Simulación Round Robin (Quantum = {Q}) ---\n")
    resultados, gantt = round_robin_final(lista_procesos, Q)
    
    # Imprimir Tabla de Resultados
    print(f"{'Proceso':<8} {'AT':<6} {'BT':<6} {'CT':<6} {'TAT':<6} {'WT':<6}")
    print("-" * 40)
    prom_tat = 0
    prom_wt = 0
    for p in sorted(resultados, key=lambda x: x['id']):
        print(f"{p['id']:<8} {p['at']:<6} {p['bt']:<6} {p['ct']:<6} {p['tat']:<6} {p['wt']:<6}")
        prom_tat += p['tat']
        prom_wt += p['wt']
    
    print("-" * 40)
    print(f"Promedio TAT: {prom_tat / len(lista_procesos)}")
    print(f"Promedio WT:  {prom_wt / len(lista_procesos)}")

    # Imprimir Secuencia para Gráfico
    print("\n--- Orden de Ejecución (Para Diagrama de Gantt) ---")
    for paso in gantt:
        print(f"[{paso[1]} - {paso[2]}] -> {paso[0]}")