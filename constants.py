from manim import config, Dot, Text, SingleStringMathTex, VMobject, Polygram, BLACK
from manim.constants import (
    ORIGIN, UP, DOWN, RIGHT, LEFT, IN, OUT, UL, UR, DL, DR, PI, TAU, DEGREES
)
from manim.typing import Vector3D
import numpy as np

CANVAS_WIDTH: float = config.frame_width
CANVAS_HEIGHT: float = config.frame_height
CANVAS_X_RAD: float = config.frame_x_radius
CANVAS_Y_RAD: float = config.frame_y_radius

Dot.set_default(color=BLACK)
Text.set_default(color=BLACK)
SingleStringMathTex.set_default(color=BLACK)
VMobject.set_default(color=BLACK)
Polygram.set_default(color=BLACK)


