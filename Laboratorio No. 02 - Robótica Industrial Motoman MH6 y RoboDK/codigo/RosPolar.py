from robodk.robolink import *    # API para comunicarte con RoboDK
from robodk.robomath import *    # Funciones matemáticas
import math

#------------------------------------------------
# 1) Conexión a RoboDK e inicialización
#------------------------------------------------
RDK = Robolink()

# Elegir un robot (si hay varios, aparece un popup)
robot = RDK.ItemUserPick("Selecciona un robot", ITEM_TYPE_ROBOT)
if not robot.Valid():
    raise Exception("No se ha seleccionado un robot válido.")

# Conectar al robot físico
#if not robot.Connect():
 #   raise Exception("No se pudo conectar al robot. Verifica que esté en modo remoto y que la configuración sea correcta.")

 #Confirmar conexión
if not robot.ConnectedState():
    raise Exception("El robot no está conectado correctamente. Revisa la conexión.")

print("Robot conectado correctamente.")

#------------------------------------------------
# 2) Cargar el Frame (ya existente) donde quieres dibujar
#    Ajusta el nombre si tu Frame se llama diferente
#------------------------------------------------
frame_name = "Frame_from_Target1"
frame = RDK.Item(frame_name, ITEM_TYPE_FRAME)
if not frame.Valid():
    raise Exception(f'No se encontró el Frame "{frame_name}" en la estación.')

# Asignamos este frame al robot
robot.setPoseFrame(frame)
# Usamos la herramienta activa
robot.setPoseTool(robot.PoseTool())

# Ajustes de velocidad y blending
robot.setSpeed(300)   # mm/s - Ajusta según necesites
robot.setRounding(5)  # blending (radio de curvatura)

target_home = "home1"
home = RDK.Item(target_home, ITEM_TYPE_TARGET)
robot.MoveJ(home)

#------------------------------------------------
# 3) Parámetros de la figura (Espiral Logaritmico)
#------------------------------------------------
r_inicial = 10            # mm
r_final = 140             # mm
vueltas = 3
num_points = 500
z_surface = 0          # plano del frame
z_safe = 50             # altura de aproximación

#------------------------------------------------
# 4)Calcula b para acabar exactamente en r_final
#------------------------------------------------
theta_final = 2 * math.pi * vueltas
b = math.log(r_final / r_inicial) / theta_final
#------------------------------------------------

#------------------------------------------------
# 5) Movimiento al centro en altura segura
#------------------------------------------------
# El centro de la rosa (r=0) corresponde a x=0, y=0
robot.MoveJ(transl(0, 0, z_surface - z_safe))

# Bajamos a la "superficie" (Z=0)
robot.MoveL(transl(0, 0, z_surface))

#------------------------------------------------
# 6) Dibujar el Espiral Logaritmico
#------------------------------------------------
# Recorremos theta de 0 a 2*pi (una vuelta completa)

for i in range(num_points + 1):
    
    theta = theta_final * i / num_points
    r = r_inicial * math.exp(b * theta)

    x = r * math.cos(theta)
    y = r * math.sin(theta)

    robot.MoveL(transl(x, y, z_surface))

# Al terminar, subimos de nuevo para no chocar
robot.MoveL(transl(x, y, z_surface + z_safe))

import csv

z_dibujo = 0
z_levantar = -5  

offset_x = 60
offset_y = 0
trazo = []

with open(r"C:\Users\guzma\OneDrive\Escritorio\Juan_Carlos.csv",
          newline="", encoding="utf-8") as archivo:

    for fila in csv.reader(archivo):
        if fila:
            trazo.append([
    float(fila[0]) + offset_x,
    float(fila[1]) + offset_y,
    float(fila[2])
])
        elif trazo:
            # Ir al inicio de una letra o contorno sin dibujar
            x, y, z = trazo[0]
            robot.MoveJ(transl(x, y, z_levantar))
            robot.MoveL(transl(x, y, z_dibujo))

            # Dibujar el contorno
            for x, y, z in trazo[1:]:
                robot.MoveL(transl(x, y, z_dibujo))

            robot.MoveL(transl(x, y, z_levantar))
            trazo = []

target_home = "home1"
home = RDK.Item(target_home, ITEM_TYPE_TARGET)
robot.MoveJ(home)


print(f"¡Figura (Espiral Logaritmico) completada en el frame '{frame_name}'!")