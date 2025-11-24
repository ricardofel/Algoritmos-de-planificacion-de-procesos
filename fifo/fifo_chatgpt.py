from dataclasses import dataclass

@dataclass
class Proceso:
    id: str
    llegada: int
    rafaga: int
    inicio: int = 0
    fin: int = 0
    espera: int = 0
    retorno: int = 0


def fifo():

    # PROCESOS QUEMADOS (datos fijos del documento)
    procesos = [
        Proceso(id="P1", llegada=0, rafaga=5),
        Proceso(id="P2", llegada=2, rafaga=3),
        Proceso(id="P3", llegada=4, rafaga=1),
        Proceso(id="P4", llegada=6, rafaga=2),
    ]

    # Ordenar procesos por llegada ascendente
    procesos.sort(key=lambda p: p.llegada)

    # tiempo_actual = 0
    tiempo_actual = 0 # REPRESENTA EL MOMENTO EN EL QUE ESTA LA CPU

    # Planificacion FIFO
    for p in procesos: # SIEMPRE SE ATIENDE AL QUE LLEGA PRIMERO 
        if tiempo_actual < p.llegada:
            tiempo_actual = p.llegada

        # SE CALCULAN LOS TIEMPOS DE CADA PROCESO
        p.inicio = tiempo_actual
        p.espera = p.inicio - p.llegada
        p.fin = p.inicio + p.rafaga
        p.retorno = p.fin - p.llegada

        tiempo_actual = p.fin

    # Calculo de promedios
    N = len(procesos)
    espera_promedio = sum(p.espera for p in procesos) / N
    retorno_promedio = sum(p.retorno for p in procesos) / N

    # RESULTADOS
    print("\n=== Resultados FIFO ===\n")
    print(f"{'ID':<6}{'Llegada':<10}{'Rafaga':<10}{'Inicio':<10}{'Fin':<10}{'Espera':<10}{'Retorno':<10}")
    print("-" * 66)

    for p in procesos:
        print(f"{p.id:<6}{p.llegada:<10}{p.rafaga:<10}{p.inicio:<10}{p.fin:<10}{p.espera:<10}{p.retorno:<10}")

    print("\nTiempo de espera promedio:", espera_promedio)
    print("Tiempo de retorno promedio:", retorno_promedio)

    # Diagrama de Gantt
    print("\nDiagrama de Gantt (FIFO):")
    if procesos:
        linea = ""
        tiempos = f"{procesos[0].inicio:>3}"

        for p in procesos:
            bloque = f"| {p.id} "
            linea += bloque
            tiempos += f"{p.fin:>4}"

        linea += "|"

        print(linea)
        print(tiempos)


if __name__ == "__main__":
    fifo()
