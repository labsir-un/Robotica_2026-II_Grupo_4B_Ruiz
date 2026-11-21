# -*- coding: utf-8 -*-
"""
Genera plano_planta.svg (vista superior de la celda del Motoman MH6, LabSIR).
Origen = base del robot. +X hacia el torno (dirección del brazo en S = 0°),
+Y hacia el alimentador de barras. Unidades del dibujo: mm.

Datos tomados de la estación RoboDK (RobodkBasico-2_1_1.rdk):
  - Base del robot sobre pedestal a 450 mm del piso.
  - Frame_from_Target1 en (823.2, -34.5, -21.1) mm respecto a la base.
  - Alcance horizontal MH6 = 1422 mm, eje S = ±170°.
Los elementos dibujados con borde punteado tienen posición/tamaño aproximado.
"""
import math

S = 0.2                    # px por mm
X0, Y0 = -2300, 1700       # esquina superior izquierda del lienzo en mm
W, H = 5900 * S, 3900 * S  # tamaño del lienzo en px
MARGEN_INF = 110           # px extra para la leyenda


def px(x, y):
    return (x - X0) * S, (Y0 - y) * S


def rect(x, y, w, h, fill, stroke="#333", dash=False, rx=4):
    (a, b) = px(x, y + h)
    d = ' stroke-dasharray="8 5"' if dash else ""
    return (f'<rect x="{a:.1f}" y="{b:.1f}" width="{w*S:.1f}" height="{h*S:.1f}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="1.5"{d}/>')


def text(x, y, s, size=12, anchor="middle", weight="normal", color="#222"):
    a, b = px(x, y)
    lines = s.split("\n")
    out = [f'<text x="{a:.1f}" y="{b:.1f}" font-size="{size}" text-anchor="{anchor}" '
           f'font-weight="{weight}" fill="{color}">']
    for i, ln in enumerate(lines):
        dy = 0 if i == 0 else size * 1.2
        out.append(f'<tspan x="{a:.1f}" dy="{dy:.1f}">{ln}</tspan>')
    out.append("</text>")
    return "".join(out)


def line(x1, y1, x2, y2, color="#333", w=1.5, dash=None, marker=False):
    a, b = px(x1, y1)
    c, d = px(x2, y2)
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    mk = ' marker-end="url(#flecha)"' if marker else ""
    return f'<line x1="{a:.1f}" y1="{b:.1f}" x2="{c:.1f}" y2="{d:.1f}" stroke="{color}" stroke-width="{w}"{ds}{mk}/>'


el = []
el.append(f'<rect width="{W}" height="{H + MARGEN_INF}" fill="white"/>')

# Cuadrícula cada 500 mm
for gx in range(-2000, 3501, 500):
    el.append(line(gx, -2200, gx, 1700, "#eee", 1))
for gy in range(-2000, 1701, 500):
    el.append(line(-2300, gy, 3600, gy, "#eee", 1))

# Zona de alcance (S = ±170°): sector circular de 340°
R = 1422
a0, a1 = math.radians(-170), math.radians(170)
p0 = px(R * math.cos(a0), R * math.sin(a0))
p1 = px(R * math.cos(a1), R * math.sin(a1))
c = px(0, 0)
el.append(f'<path d="M {c[0]:.1f} {c[1]:.1f} L {p0[0]:.1f} {p0[1]:.1f} '
          f'A {R*S:.1f} {R*S:.1f} 0 1 0 {p1[0]:.1f} {p1[1]:.1f} Z" '
          f'fill="#fdecea" fill-opacity="0.55" stroke="#c0392b" stroke-width="1.5" stroke-dasharray="10 6"/>')
el.append(text(1150, -1400, "Volumen de trabajo MH6\nR = 1422 mm, S = ±170°", 12, anchor="start", color="#c0392b"))

# Alimentador de barras SN542 (detrás del robot) y torno CNC
el.append(rect(-2100, 550, 3300, 420, "#d9d9d9", dash=True))
el.append(text(-450, 720, "Alimentador de barras SN542", 13, weight="bold"))
el.append(rect(1200, -500, 2000, 1500, "#f3ead3", dash=True))
el.append(text(2200, 300, "Torno CNC\nJinn Fa JSL-32AB", 14, weight="bold"))
el.append(text(2200, -300, "(frente / puerta)", 11, color="#555"))

# Unidad hidráulica del torno
el.append(rect(1250, 1050, 600, 450, "#e5e5e5", dash=True))
el.append(text(1550, 1250, "Unidad hidráulica", 11))

# Pedestal y robot
el.append(rect(-330, -380, 660, 760, "#2f5fb3", stroke="#1d3d75", rx=6))
el.append(f'<circle cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="{230*S:.1f}" fill="#bfbfbf" stroke="#555" stroke-width="1.5"/>')
el.append(text(0, 30, "MH6", 12, weight="bold"))
el.append(text(0, -310, "Pedestal h = 450 mm", 10, color="white"))

# Ejes de la base del robot
el.append(line(0, 0, 450, 0, "#c0392b", 2.5, marker=True))
el.append(line(0, 0, 0, 450, "#27ae60", 2.5, marker=True))
el.append(text(520, -20, "X", 13, weight="bold", color="#c0392b"))
el.append(text(-40, 480, "Y", 13, weight="bold", color="#27ae60"))

# Superficie de dibujo (CAJA2) y frame de trabajo
fx, fy = 823.2, -34.5
el.append(rect(fx - 230, fy - 300, 460, 460, "#9e9e9e", stroke="#424242", dash=True))
el.append(f'<circle cx="{px(fx, fy)[0]:.1f}" cy="{px(fx, fy)[1]:.1f}" r="4" fill="#f1c40f" stroke="#333"/>')
el.append(text(700, fy - 460, "Superficie de dibujo (CAJA2)\nFrame_from_Target1\n(823, −34) mm", 11, weight="bold"))
# Espiral pequeña indicativa (r = 10 e^{b θ})
b = math.log(14) / (6 * math.pi)
pts = []
for i in range(301):
    th = 6 * math.pi * i / 300
    r = 10 * math.exp(b * th)
    pts.append(px(fx + r * math.cos(th), fy - r * math.sin(th)))
el.append('<polyline fill="none" stroke="#f1c40f" stroke-width="1.6" points="' +
          " ".join(f"{a:.1f},{bb:.1f}" for a, bb in pts) + '"/>')

# Soporte con placa de madera y mesa metálica
el.append(rect(-900, -150, 120, 450, "#c8a26b", dash=True))
el.append(text(-1180, 100, "Soporte con\nplaca de madera", 11, anchor="middle"))
el.append(rect(-1150, -1000, 650, 400, "#e0e0e0", dash=True))
el.append(text(-825, -820, "Soporte metálico", 11))

# Controlador, PC y pendant
el.append(rect(-2150, -500, 450, 500, "#4d4d4d", stroke="#222", dash=True))
el.append(text(-1925, -230, "DX100", 13, weight="bold", color="white"))
el.append(rect(-2150, -1600, 600, 400, "#dff0d8", dash=True))
el.append(text(-1850, -1420, "PC + RoboDK", 13, weight="bold"))
el.append(text(-1850, -1530, "(Run on robot)", 10, color="#555"))
el.append(rect(-300, -1640, 260, 170, "#fafafa", dash=True))
el.append(text(-170, -1590, "Pendant", 10))

# Conexiones
el.append(line(-1850, -1200, -1925, -500, "#2980b9", 2, "6 4"))
el.append(text(-1830, -800, "Ethernet (HSE)\n192.168.1.20", 10, anchor="start", color="#2980b9"))
el.append(line(-1700, -250, -330, -100, "#7f8c8d", 2, "2 4"))
el.append(text(-1250, -110, "cables motor/encoder", 10, color="#7f8c8d"))
q = [px(-1700, -450), px(-1350, -1150), px(-300, -1555)]
el.append('<polyline fill="none" stroke="#8e44ad" stroke-width="1.5" stroke-dasharray="2 4" points="' + " ".join(f"{a:.1f},{bb:.1f}" for a, bb in q) + '"/>')
el.append(text(-900, -1450, "cable pendant", 10, color="#8e44ad"))

# Zona del operador
el.append(rect(-1400, -2100, 1700, 350, "#fff8dc", stroke="#b7950b", dash=True))
el.append(text(-550, -1990, "Zona del operador (fuera del volumen de trabajo)", 11, color="#7d6608"))

# Escala gráfica
sx, sy = 2300, -1900
el.append(line(sx, sy, sx + 1000, sy, "#000", 3))
for k in (0, 500, 1000):
    el.append(line(sx + k, sy - 40, sx + k, sy + 40, "#000", 2))
el.append(text(sx + 500, sy + 90, "1000 mm", 12))

# Título y leyenda
el.append(f'<text x="{W/2:.0f}" y="24" font-size="17" font-weight="bold" text-anchor="middle">'
          'Plano de planta – Celda Motoman MH6 (LabSIR, UNAL) – vista superior</text>')
ly = H + 25
el.append(f'<text x="15" y="{ly:.0f}" font-size="12" fill="#333">'
          'Origen en la base del robot. +X: dirección del brazo con S = 0° (hacia el torno); +Y: hacia el alimentador de barras.</text>')
el.append(f'<text x="15" y="{ly+20:.0f}" font-size="12" fill="#333">'
          'Línea continua: posición tomada de la estación RoboDK. Línea punteada: posición/tamaño aproximado según fotografías.</text>')
el.append(f'<text x="15" y="{ly+40:.0f}" font-size="12" fill="#333">'
          'Pedestal del robot: 450 mm de altura. Frame de trabajo: Frame_from_Target1 (estación RoboDK).</text>')

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H + MARGEN_INF:.0f}" '
       f'viewBox="0 0 {W:.0f} {H + MARGEN_INF:.0f}" font-family="DejaVu Sans, Arial, sans-serif">'
       '<defs><marker id="flecha" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto">'
       '<path d="M0,0 L12,6 L0,12 z" fill="#333"/></marker></defs>'
       + "".join(el) + "</svg>")

with open("plano_planta.svg", "w", encoding="utf-8") as f:
    f.write(svg)
print("plano_planta.svg generado")
