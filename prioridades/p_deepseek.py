import tkinter as tk
from tkinter import ttk
import heapq
import time
import threading

# ---------------------------------------------------------------
# CLASE PROCESO
# ---------------------------------------------------------------

class Proceso:
    """
    Representa un proceso (paciente) con:
    - nombre
    - tiempo de llegada
    - duración total
    - prioridad (menor número = más urgente)
    """
    def __init__(self, nombre, llegada, duracion, prioridad):
        self.nombre = nombre
        self.llegada = llegada
        self.duracion = duracion
        self.prioridad = prioridad
        self.restante = duracion  # tiempo que falta por ejecutarse

    def __lt__(self, other):
        """
        Para que heapq (cola de prioridad) ordene por prioridad
        y en empate, respete el orden de llegada (FIFO).
        """
        if self.prioridad == other.prioridad:
            return self.llegada < other.llegada
        return self.prioridad < other.prioridad


# ---------------------------------------------------------------
# SIMULACIÓN DEL ALGORITMO DE PRIORIDAD (SIN DESALOJO)
# Y REPRESENTACIÓN GRÁFICA EN TKINTER
# ---------------------------------------------------------------

class PlanificadorGUI:
    def __init__(self, root, procesos):
        self.root = root
        self.root.title("Planificación por Prioridades (Sin Desalojo)")

        self.procesos = sorted(procesos, key=lambda p: p.llegada)
        self.cola_listos = []
        self.indice = 0
        self.tiempo = 0
        self.actual = None
        self.historial = []  # para construir el diagrama de Gantt

        # -------------------------
        # INTERFAZ
        # -------------------------

        # Etiqueta proceso actual
        self.lbl_actual = tk.Label(root, text="Proceso actual: ---", font=("Arial", 14))
        self.lbl_actual.pack(pady=10)

        # Cola de listos
        self.lbl_cola = tk.Label(root, text="Cola de listos:", font=("Arial", 12))
        self.lbl_cola.pack()

        self.lista_cola = tk.Listbox(root, width=40, height=5)
        self.lista_cola.pack()

        # Canvas para el diagrama de Gantt
        self.canvas = tk.Canvas(root, width=600, height=200, bg="white")
        self.canvas.pack(pady=20)

        # Botón iniciar
        self.btn_iniciar = tk.Button(root, text="Iniciar Simulación", command=self.iniciar)
        self.btn_iniciar.pack()

    # ---------------------------------------------------------------
    # INICIAR LA SIMULACIÓN EN UN HILO PARA NO BLOQUEAR LA INTERFAZ
    # ---------------------------------------------------------------
    def iniciar(self):
        self.btn_iniciar.config(state="disabled")
        hilo = threading.Thread(target=self.simular)
        hilo.start()

    # ---------------------------------------------------------------
    # ACTUALIZAR COLA DE LISTOS EN EL LISTBOX
    # ---------------------------------------------------------------
    def actualizar_cola(self):
        self.lista_cola.delete(0, tk.END)
        for p in sorted(self.cola_listos):
            self.lista_cola.insert(tk.END, f"{p.nombre} | Prio {p.prioridad}")

    # ---------------------------------------------------------------
    # DIBUJAR BLOQUE EN EL DIAGRAMA DE GANTT
    # ---------------------------------------------------------------
    def dibujar_gantt(self, proceso, inicio, fin):
        """
        Cada proceso se dibuja como un rectángulo horizontal.
        """
        alto = 30
        pos_y = 20 + (len(self.historial) * 40)

        self.canvas.create_rectangle(inicio*20, pos_y,
                                     fin*20, pos_y + alto,
                                     fill="lightblue")

        self.canvas.create_text((inicio*20 + fin*20)//2,
                                pos_y + alto//2,
                                text=proceso.nombre)

    # ---------------------------------------------------------------
    # SIMULACIÓN DEL ALGORITMO
    # ---------------------------------------------------------------
    def simular(self):
        inicio_bloque = None

        while self.indice < len(self.procesos) or self.cola_listos or self.actual:

            # Procesos que llegan en el tiempo actual
            while self.indice < len(self.procesos) and self.procesos[self.indice].llegada == self.tiempo:
                p = self.procesos[self.indice]
                heapq.heappush(self.cola_listos, p)
                self.indice += 1
                self.actualizar_cola()

            # Si no hay proceso ejecutándose, sacamos el siguiente por prioridad
            if not self.actual and self.cola_listos:
                self.actual = heapq.heappop(self.cola_listos)
                self.actualizar_cola()

                inicio_bloque = self.tiempo
                self.lbl_actual.config(text=f"Proceso actual: {self.actual.nombre}")

            # Procesar el proceso actual
            if self.actual:
                self.actual.restante -= 1

                if self.actual.restante == 0:
                    # Finaliza → dibujamos en Gantt
                    fin_bloque = self.tiempo + 1
                    self.historial.append((self.actual, inicio_bloque, fin_bloque))
                    self.dibujar_gantt(self.actual, inicio_bloque, fin_bloque)

                    # Liberar CPU
                    self.actual = None
                    self.lbl_actual.config(text="Proceso actual: ---")

            # Avanzar el tiempo
            self.tiempo += 1
            time.sleep(0.5)

        self.lbl_actual.config(text="Simulación completada")


# ---------------------------------------------------------------
# EJEMPLO DE PROCESOS (PACIENTES DEL HOSPITAL)
# ---------------------------------------------------------------

procesos = [
    Proceso("Paciente_Fractura", 0, 6, 1),
    Proceso("Paciente_Gripe", 1, 3, 4),
    Proceso("Paciente_Corte", 2, 4, 2),
    Proceso("Paciente_Paro", 3, 5, 0),
    Proceso("Paciente_Fiebre", 5, 2, 5)
]

root = tk.Tk()
app = PlanificadorGUI(root, procesos)
root.mainloop()
