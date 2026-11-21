# -*- coding: utf-8 -*-
"""
Convierte las posiciones Home1/Home2 leídas en el pendant del DX100 (pulsos)
a grados articulares.

Relación pulsos/grado tomada de los parámetros del robot "Motoman MH6"
guardados en la estación RobodkBasico-2_1_1.rdk:
    S = 1435.350, L = 1300.317, U = 1376.711,
    R =  568.889, B =  823.908, T =  425.558
"""

EJES = ["S", "L", "U", "R", "B", "T"]
PULSOS_POR_GRADO = [1435.350, 1300.317, 1376.711, 568.889, 823.908, 425.558]

HOMES = {
    "Home1 - WORK HOME POSITION": [0, -115290, -111622, 1, 42647, 1392],
    "Home2 - SECOND HOME POS":    [0, 2037, 2359, 0, -121, 1392],
}


def pulsos_a_grados(pulsos):
    return [p / k for p, k in zip(pulsos, PULSOS_POR_GRADO)]


if __name__ == "__main__":
    print("| Posición | " + " | ".join(f"{e} [°]" for e in EJES) + " |")
    print("|---|" + "---|" * len(EJES))
    for nombre, pulsos in HOMES.items():
        grados = pulsos_a_grados(pulsos)
        print(f"| {nombre} | " + " | ".join(f"{g:.2f}" for g in grados) + " |")
