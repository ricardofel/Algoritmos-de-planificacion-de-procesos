def round_robin_scheduler():
    print("="*60)
    print(" SIMULADOR DE PLANIFICACIÓN ROUND ROBIN")
    print("="*60)
    
    # Solicitar quantum
    quantum = int(input("\nIngrese el valor del Quantum: "))
    
    # Solicitar número de procesos
    n = int(input("Ingrese el número de procesos: "))
    
    # Listas para almacenar datos
    pid = []
    tiempo_llegada = []
    tiempo_rafaga = []
    tiempo_rafaga_restante = []
    tiempo_finalizacion = []
    tiempo_retorno = []
    tiempo_espera = []
    
    # Ingresar datos de los procesos
    print("\n" + "-"*60)
    for i in range(n):
        print(f"\nProceso {i+1}:")
        pid.append(i+1)
        llegada = int(input("  Tiempo de llegada: "))
        tiempo_llegada.append(llegada)
        rafaga = int(input("  Tiempo de ráfaga: "))
        tiempo_rafaga.append(rafaga)
        tiempo_rafaga_restante.append(rafaga)
        tiempo_finalizacion.append(0)
        tiempo_retorno.append(0)
        tiempo_espera.append(0)
    
    # Simulación del algoritmo Round Robin
    print("\n" + "="*60)
    print(" EJECUCIÓN DEL ALGORITMO")
    print("="*60 + "\n")
    
    tiempo_actual = 0
    cola = []
    procesos_listos = [False] * n
    completados = 0
    
    # Agregar primer proceso que llega
    for i in range(n):
        if tiempo_llegada[i] == 0:
            cola.append(i)
            procesos_listos[i] = True
    
    while completados < n:
        if len(cola) == 0:
            # Avanzar tiempo si no hay procesos en cola
            tiempo_actual += 1
            for i in range(n):
                if tiempo_llegada[i] <= tiempo_actual and not procesos_listos[i] and tiempo_rafaga_restante[i] > 0:
                    cola.append(i)
                    procesos_listos[i] = True
            continue
        
        # Tomar proceso de la cola
        indice = cola.pop(0)
        
        # Ejecutar proceso
        if tiempo_rafaga_restante[indice] > quantum:
            print(f"[Tiempo {tiempo_actual}] Ejecutando P{pid[indice]} por {quantum} unidades")
            tiempo_actual += quantum
            tiempo_rafaga_restante[indice] -= quantum
        else:
            print(f"[Tiempo {tiempo_actual}] Ejecutando P{pid[indice]} por {tiempo_rafaga_restante[indice]} unidades")
            tiempo_actual += tiempo_rafaga_restante[indice]
            tiempo_rafaga_restante[indice] = 0
            
            # Proceso completado
            tiempo_finalizacion[indice] = tiempo_actual
            tiempo_retorno[indice] = tiempo_finalizacion[indice] - tiempo_llegada[indice]
            tiempo_espera[indice] = tiempo_retorno[indice] - tiempo_rafaga[indice]
            completados += 1
            print(f"[Tiempo {tiempo_actual}] Proceso P{pid[indice]} COMPLETADO\n")
        
        # Agregar procesos que llegaron durante la ejecución
        for i in range(n):
            if tiempo_llegada[i] <= tiempo_actual and not procesos_listos[i] and tiempo_rafaga_restante[i] > 0:
                cola.append(i)
                procesos_listos[i] = True
        
        # Si el proceso no terminó, volver a agregarlo a la cola
        if tiempo_rafaga_restante[indice] > 0:
            cola.append(indice)
    
    # Mostrar resultados
    print("\n" + "="*60)
    print(" RESULTADOS DE LA PLANIFICACIÓN")
    print("="*60)
    print(f"\n{'PID':<6} {'Llegada':<10} {'Ráfaga':<10} {'Final':<10} {'Retorno':<10} {'Espera':<10}")
    print("-"*60)
    
    suma_espera = 0
    suma_retorno = 0
    
    for i in range(n):
        print(f"P{pid[i]:<5} {tiempo_llegada[i]:<10} {tiempo_rafaga[i]:<10} {tiempo_finalizacion[i]:<10} {tiempo_retorno[i]:<10} {tiempo_espera[i]:<10}")
        suma_espera += tiempo_espera[i]
        suma_retorno += tiempo_retorno[i]
    
    print("-"*60)
    
    # Calcular promedios
    espera_promedio = suma_espera / n
    retorno_promedio = suma_retorno / n
    
    print(f"\nTIEMPO DE ESPERA PROMEDIO:    {espera_promedio:.2f} unidades")
    print(f"TIEMPO DE RETORNO PROMEDIO:   {retorno_promedio:.2f} unidades")
    print("="*60)

# Ejecutar el programa
if __name__ == "__main__":
    round_robin_scheduler()