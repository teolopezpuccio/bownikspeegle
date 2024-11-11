from manim import *
from constants import *
from itertools import product
import numpy as np
import os
import re

class Intervalo(Polygon):
    def __init__(
        self,
        x1: float = 0,
        x2: float = 1.0,
        y1: float = 0,
        y2: float = 1.0,
        color: ParsableManimColor = BLACK,
        **kwargs,
    ):
        super().__init__([x2, y2, 0], [x1, y2, 0], [x1, y1, 0], [x2 , y1, 0], color=color, stroke_opacity=0 , fill_opacity=1, **kwargs)

def create_out(width=CANVAS_WIDTH, height=CANVAS_HEIGHT, stroke=False): # crea el vmobject base solo con el fondo
    out = VGroup()
    out += Rectangle(fill_color=WHITE, # el fondo blanco
                stroke_color=BLACK,
                stroke_opacity=stroke,
                width=width,
                height=height,
                fill_opacity=1)
    return out

def save_out(filename, out, pdf_out: bool = True, cropping: bool = True):
    out.to_svg(f"{filename}.svg", crop=cropping) # exporta out a svg...
    if pdf_out:
        os.system(f"rsvg-convert -f pdf -o {filename}.pdf {filename}.svg") # ...y corre en la terminal el código que convierte el svg a pdf

def setup_axes(out):
    width, height = out.get_width(), out.get_height()
    out += Axes(                        # los ejes
        x_range=(-64/9 * width / CANVAS_WIDTH, 64/9 * width / CANVAS_WIDTH, 1),
        y_range=(-4.0 * height / CANVAS_HEIGHT, 4.0 * height / CANVAS_HEIGHT, 1),
        x_length=None,
        y_length=None,
        axis_config=dict(
            include_ticks=True,
            include_tip=False,
            include_numbers=True,
            tick_size=0.05,
            font_size=20,
            color=BLACK,
            stroke_width=2,
            decimal_number_config={"num_decimal_places": 0}
        ),
        x_axis_config=dict(
            numbers_to_include=range(-int(width/2), int(width/2)+1, 1)
        ),
        y_axis_config=dict(
            numbers_to_include=range(-int(height/2), int(height/2)+1, 1),
            line_to_number_buff=0.3
        )
    )

def setup_custom_axes(out, width, height, font_size=20, tick_size=0.05, ticks=True):
    out += Axes(                        # los ejes
        x_range=(-64/9 * width / CANVAS_WIDTH, 64/9 * width / CANVAS_WIDTH, 1),
        y_range=(-4.0 * height / CANVAS_HEIGHT, 4.0 * height / CANVAS_HEIGHT, 1),
        x_length=None,
        y_length=None,
        axis_config=dict(
            include_ticks=ticks,
            include_tip=False,
            include_numbers=True,
            tick_size=tick_size,
            font_size=font_size,
            color=BLACK,
            stroke_width=2,
            decimal_number_config={"num_decimal_places": 0}
        ),
        x_axis_config=dict(
            numbers_to_include=range(-int(width/2), int(width/2)+1, 1)
        ),
        y_axis_config=dict(
            numbers_to_include=range(-int(height/2), int(height/2)+1, 1),
            line_to_number_buff=0.3
        )
    )

def extend_3d(m: np.array):
    extended = np.eye(3)
    extended[:2, :2] = m
    return extended

def translate_Z(vm, m, n):
    return vm.shift(m*RIGHT, n*UP)

def fill_range(vm, x_range, y_range):
    displaced_vms = []
    for i,j in product(x_range, y_range):
        displaced_vms.append(
            translate_Z(vm.copy(), i, j)
        )
    return displaced_vms

def fill_range_R1(vm, x_range):
    displaced_vms = []
    for i in x_range:
        displaced_vms.append(
            translate_Z(vm.copy(), i, 0)
        )
    return displaced_vms

def setup_integer_lattice(out, x_range, y_range, r=0.05):
    dot = Dot(radius=r).set_fill(color=BLACK, opacity=1).set_stroke(opacity=1)
    for i in x_range:
        for j in y_range:
            out.add(translate_Z(dot.copy(), i, j))

background = Rectangle(width=CANVAS_WIDTH, height=CANVAS_HEIGHT)


# conversor a SVG y PDF hecho por Berna que cropea


# estas se van a constants
# (podés escribirlas en función de SLIDE_WIDTH y SLIDE_HEIGHT)
X_MANIM_TO_PX = 1920/(8 * 16/9)
Y_MANIM_TO_PX = 1080/8



def convert_svg_to_pdf(filename, new_width, new_height):
    with open(filename, 'r') as f:
        svg = f.readlines()

    width_pattern = r'width="(\d+)"'
    height_pattern = r'height="(\d+)"'
    viewbox_pattern = r'viewBox="([\d\s]+)"'

    width = float(re.search(width_pattern, svg[1]).group(1))
    height = float(re.search(height_pattern, svg[1]).group(1))

    new_width, new_height = new_width*X_MANIM_TO_PX, new_height*Y_MANIM_TO_PX
    new_x, new_y = (width-new_width)/2, (height-new_height)/2

    svg[1] = re.sub(width_pattern, f'width="{new_width}"', svg[1])
    svg[1] = re.sub(height_pattern, f'height="{new_height}"', svg[1])
    svg[1] = re.sub(
        viewbox_pattern,
        f'viewBox="{new_x} {new_y} {new_width} {new_height}"',
        svg[1]
    )

    with open(f"new_{filename}", 'w') as f:
        f.writelines(svg)

    output_filename = f"{filename.replace('.svg','.pdf')}"
    os.system(
        f"rsvg-convert -f pdf -o {output_filename} new_{filename}"
    )