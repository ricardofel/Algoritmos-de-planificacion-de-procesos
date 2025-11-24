import heapq
# Nota sobre heapq:
# heapq siempre devuelve el elemento con el valor numérico más pequeño.
# En este algoritmo, una prioridad más baja (por ejemplo 1) significa
# MAYOR prioridad del proceso. Por eso heapq funciona bien:
# el proceso con mejor prioridad es también el de menor número,
# así que heapq lo extrae primero naturalmente.
import time
import matplotlib.pyplot as plt

# ----------------
# CLASE PROCESO
# ----------------

class Proceso:
    """
    Representa un proceso con:
    - nombre
    - llegada
    - duracion
    - prioridad  (menor número = mayor prioridad)
    - restante   (tiempo pendiente por ejecutar)
    """
    def __init__(self, nombre, llegada, duracion, prioridad):
        self.nombre = nombre
        self.llegada = llegada
        self.duracion = duracion
        self.prioridad = prioridad
        self.restante = duracion

        # Para cálculos finales
        self.tiempo_fin = None

    def __lt__(self, other):
        """
        heapq ordena por prioridad,
        y si empatan usa la hora de llegada (FIFO).
        """
        if self.prioridad == other.prioridad:
            return self.llegada < other.llegada
        return self.prioridad < other.prioridad


# -----------------------------------------------------------
# ALGORITMO DE PLANIFICACIÓN POR PRIORIDADES (NO PREEMPTIVO)
# -----------------------------------------------------------
def planificar_por_prioridades(procesos):
    tiempo = 0
    procesos = sorted(procesos, key=lambda p: p.llegada)

    cola_listos = []
    indice = 0
    actual = None

    # Para gráficos y métricas
    ejecucion_gantt = []     # lista de (proceso, tiempo_inicio, tiempo_fin)
    inicio_actual = None     # para saber cuándo empezó el proceso actual

    print("\n===== SIMULACIÓN: PLANIFICACION POR PRIORIDADES =====\n")

    # CADA VUELTA DE ESTE WHILE SIMULA UN INSTANTE DE TIEMPO T 
    # HASTA QUE:
    # No queden procesos por llegar.
    # No queden procesos en la cola.
    # No haya un proceso ejecutándose.
    while indice < len(procesos) or cola_listos or actual:

        # 1. Llegada de procesos (VA LLEGANDO CADA UNO, LO ANUNCIA Y LO METE EN LA COLA)
        while indice < len(procesos) and procesos[indice].llegada == tiempo:
            p = procesos[indice]
            print(f"[t={tiempo}] LLEGA {p.nombre} | Prio={p.prioridad} | Duración={p.duracion}")
            heapq.heappush(cola_listos, p)
            indice += 1

        # 2. Tomar proceso si CPU libre (TOMA EL PROCESO CON MEJOR PRIORIDAD)
        if not actual and cola_listos:
            actual = heapq.heappop(cola_listos)
            inicio_actual = tiempo
            print(f"[t={tiempo}] >>>>>>>>>> ENTRA AL CPU: {actual.nombre} (Prio {actual.prioridad}) <<<<<<<<<<")

        # 3. Ejecutar
        if actual:
            actual.restante -= 1 # Le quita un instante si ya lo ejecuto
            print(f"[t={tiempo}] Ejecutando {actual.nombre} | Restante: {actual.restante}")

            if actual.restante == 0:
                actual.tiempo_fin = tiempo + 1
                ejecucion_gantt.append((actual.nombre, inicio_actual, tiempo + 1))
                #Si ya terminó, lo marco como terminado y libero la CPU para el siguiente.
                print(f"[t={tiempo}] ++++++++++ {actual.nombre} HA TERMINADO ++++++++++") 
                actual = None

        tiempo += 1
        time.sleep(0.15)  # para animación en consola

    print("\n===== FIN DE LA SIMULACIÓN =====\n")

    mostrar_resultados(procesos, ejecucion_gantt)


# -----------------------------------------------
# FUNCIÓN PARA MOSTRAR TABLA Y GRAFICAR GANTT
# -----------------------------------------------
def mostrar_resultados(procesos, ejecucion):
    print("============ TABLA DE RESULTADOS ============")

    print(f"{'Proceso':20} {'Llegada':8} {'Duración':9} {'Fin':5} {'Espera':7} {'Sistema':8}")

    tiempos_espera = []
    tiempos_sistema = []

    for p in procesos:
        turnaround = p.tiempo_fin - p.llegada
        espera = turnaround - p.duracion

        tiempos_espera.append(espera)
        tiempos_sistema.append(turnaround)

        print(f"{p.nombre:20} {p.llegada:<8} {p.duracion:<9} {p.tiempo_fin:<5} {espera:<7} {turnaround:<8}")

    print("\nTiempo promedio de espera:",
          sum(tiempos_espera) / len(procesos))
    print("Tiempo promedio en el sistema:",
          sum(tiempos_sistema) / len(procesos))

    # --------------------------
    # GRAFICAR GANTT
    # --------------------------
    fig, ax = plt.subplots(figsize=(10, 4))

    for i, (nombre, inicio, fin) in enumerate(ejecucion):
        ax.barh(y=nombre, width=fin - inicio, left=inicio, height=0.4)
        ax.text(inicio + 0.1, i, f"{nombre}", va="center", fontsize=8)

    ax.set_xlabel("Tiempo")
    ax.set_ylabel("Procesos")
    ax.set_title("Diagrama de Gantt - Planificación por Prioridades (No Preemptivo)")
    ax.grid(True, axis="x", linestyle="--", alpha=0.5)

    plt.show()


# ---------------------
# CREACION DE PROCESOS
# ---------------------
procesos = [
    Proceso("Paciente Fractura",   llegada=0, duracion=6, prioridad=1),
    Proceso("Paciente Gripe",      llegada=1, duracion=3, prioridad=4),
    Proceso("Paciente Corte",      llegada=2, duracion=4, prioridad=2),
    Proceso("Paciente Paro Card.", llegada=3, duracion=5, prioridad=0),
    Proceso("Paciente Fiebre",     llegada=5, duracion=2, prioridad=5),
]

# ------------------------
# INICIO DE LA SIMULACION
# ------------------------
planificar_por_prioridades(procesos)
