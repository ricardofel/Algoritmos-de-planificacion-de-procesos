import heapq
import time

# ----------------
# CLASE PROCESO
# ----------------

class Proceso:
    """
    Representa un proceso (paciente) con:
    - nombre: Etiqueta del proceso
    - llegada: Tiempo de llegada al sistema
    - duracion: Tiempo total de CPU requerido
    - prioridad: Entre menor el número, mayor prioridad
    - restante: Tiempo que falta por ejecutarse (se inicia igual a duración)
    """
    def __init__(self, nombre, llegada, duracion, prioridad):
        self.nombre = nombre
        self.llegada = llegada
        self.duracion = duracion
        self.prioridad = prioridad
        self.restante = duracion

    def __lt__(self, other):
        """
        Permite que heapq ordene correctamente:
        1 Primero por prioridad (menor es más urgente)
        2 Si empatan, por orden de llegada (FIFO)
        """
        if self.prioridad == other.prioridad:
            return self.llegada < other.llegada
        return self.prioridad < other.prioridad

# -----------------------------------------------------------
# ALGORITMO DE PLANIFICACIÓN POR PRIORIDADES (SIN DESALOJO)
# -----------------------------------------------------------
def planificar_por_prioridades(procesos):
    tiempo = 0
    procesos = sorted(procesos, key=lambda p: p.llegada)

    cola_listos = []  # heap de prioridad
    indice = 0        # para recorrer la lista de procesos por llegada
    actual = None     # proceso que está usando el CPU

    print("\n===== SIMULACIÓN: PLANIFICACION POR PRIORIDADES =====\n")

    while indice < len(procesos) or cola_listos or actual:

        # ---------------------------------------------------------
        # 1. Llegada de procesos
        # ---------------------------------------------------------
        while indice < len(procesos) and procesos[indice].llegada == tiempo:
            p = procesos[indice]
            print(f"[t={tiempo}] Llega {p.nombre} | Prio={p.prioridad} | Duración={p.duracion}")
            heapq.heappush(cola_listos, p)
            indice += 1

        # ---------------------------------------------------------
        # 2. Si el CPU está libre, tomar el proceso de mayor prioridad
        # ---------------------------------------------------------
        if not actual and cola_listos:
            actual = heapq.heappop(cola_listos)
            print(f"[t={tiempo}] >>> Entra al CPU: {actual.nombre} (Prio {actual.prioridad})")

        # ---------------------------------------------------------
        # 3. Ejecutar el proceso actual
        # ---------------------------------------------------------
        if actual:
            actual.restante -= 1
            print(f"[t={tiempo}] Ejecutando {actual.nombre} | Restante: {actual.restante}")

            # Cuando termina
            if actual.restante == 0:
                print(f"[t={tiempo}] ++++++++++++++ {actual.nombre} ha terminado ++++++++++++++")
                actual = None

        # ---------------------------------------------------------
        # 4. Avanzar el tiempo
        # ---------------------------------------------------------
        tiempo += 1
        time.sleep(0.3)  # Solo para visualización más clara en consola

    print("\n===== FIN DE LA SIMULACIÓN =====\n")
# ---------------------
# CREACION DE PROCESOS
# ---------------------
procesos = [
    Proceso("Paciente Fractura",   llegada=0, duracion=6, prioridad=1),
    Proceso("Paciente Gripe",      llegada=1, duracion=3, prioridad=4),
    Proceso("Paciente Corte",      llegada=2, duracion=4, prioridad=2),
    Proceso("Paciente Paro Cardiaco",       llegada=3, duracion=5, prioridad=0),
    Proceso("Paciente Fiebre",     llegada=5, duracion=2, prioridad=5),
]
# ------------------------
# INICIO DE LA SIMULACION
# ------------------------
planificar_por_prioridades(procesos)