from manim import * 
from constants import *
from utils import Intervalo, create_out, setup_custom_axes, save_out, extend_3d, background, convert_svg_to_pdf

out = create_out()

config.background_color = WHITE

# axes para wavelet, más espacio

ax1 = Axes(x_range=[-5.5,5.5,1], y_range=[-1.5,1.5,1],
          axis_config=dict(
            include_tip=False,
            include_ticks=True,
            include_numbers=True,
            tick_size=0.05,
            font_size=20,
            color=BLACK,
            stroke_width=2,
            decimal_number_config={"num_decimal_places": 0}
        )
          # x_axis_config=dict(
          #   unit_size=0.5,
          #   numbers_to_include=[-2,-1, 1, 2],
          #   numbers_with_elongated_ticks=[-2, -1, 1, 2]
          # ),
          # y_axis_config=dict(
          #     line_to_number_buff=0.25
          # )
        )

# axes para función característica, más chatos

ax2 = Axes(x_range=[-2.5,2.5,1], y_range=[-0.5,2,1],
          axis_config=dict(
            include_tip=False,
            include_ticks=True,
            include_numbers=True,
            tick_size=0.05,
            font_size=20,
            color=BLACK,
            stroke_width=2,
            decimal_number_config={"num_decimal_places": 0}
        ))


f1 = ax1.plot(lambda x: (np.sin(2*np.pi*x) - np.sin(np.pi*x))/(np.pi*x), color= RED, stroke_width=2.8)

f2 = ax1.plot(lambda x: (-np.sin(2*np.pi*x) + np.sin((8/3)*np.pi*x) + np.sin(np.pi*x) - np.sin((2/3)*np.pi*x))/(np.pi*x), color= BLUE, stroke_width=2.8)

# x_values = [-5.5, -1, -1, -1/2, -1/2, 1/2, 1/2, 1, 1, 5.5]
# y_values = [0, 0, 1, 1, 0, 0, 1, 1, 0, 0]
# coords = [ax2.c2p(x,y) for x,y in zip(x_values,y_values)]
# plot = VMobject(color=RED).set_points_as_corners(coords)

char_function_1 = lambda x: (
    1 if (
        (-1 <= x <= -0.5) or 
        (0.5 <= x <= 1)
    ) else 0
)

char_function_2 = lambda x: (
    1 if (
        (-4/3 <= x <= -1) or 
        (-1/2 <= x <= -1/3) or 
        (1/3 <= x <= 1/2) or 
        (1 <= x <= 4/3)
    ) else 0
)

car1 = ax1.plot(
    char_function_1,
    discontinuities=[-1, -0.5, 0.5, 1],
    color= RED,
    stroke_width=2.8
    )

car2 = ax1.plot(
    char_function_2,
    discontinuities=[-4/3, -1,  -1/2, -1/3, 1/3, 1/2, 1, 4/3],
    color= RED,
    stroke_width=2.8
    )

# out.add(ax1, f2) 

# out.to_svg('otra_wavelet.svg')
# # convert_svg_to_pdf('caracteristica.svg', 12, 6)
# convert_svg_to_pdf('otra_wavelet.svg', 12, 6)

class Graphs_beamer(Scene):
    def construct(self):

        ax_time = Axes(x_range=[-5.5,5.5,1], y_range=[-1.5,1.5,1],
            axis_config=dict(
            include_tip=False,
            include_ticks=True,
            include_numbers=True,
            tick_size=0.05,
            font_size=20,
            color=BLACK,
            stroke_width=2,
            decimal_number_config={"num_decimal_places": 0}
        )
            # x_axis_config=dict(
            #   unit_size=0.5,
            #   numbers_to_include=[-2,-1, 1, 2],
            #   numbers_with_elongated_ticks=[-2, -1, 1, 2]
            # ),
            # y_axis_config=dict(
            #     line_to_number_buff=0.25
            # )
        )

        ax_freq = Axes(x_range=[-5.5,5.5,1], y_range=[-1.5,1.5,1],
            axis_config=dict(
            include_tip=False,
            include_ticks=True,
            include_numbers=True,
            tick_size=0.05,
            font_size=20,
            color=BLACK,
            stroke_width=2,
            decimal_number_config={"num_decimal_places": 0}
        )
            # x_axis_config=dict(
            #   unit_size=0.5,
            #   numbers_to_include=[-2,-1, 1, 2],
            #   numbers_with_elongated_ticks=[-2, -1, 1, 2]
            # ),
            # y_axis_config=dict(
            #     line_to_number_buff=0.25
            # )
        )

#        shannon_w = ax.plot(lambda x: (np.sin(2*np.pi*x) - np.sin(np.pi*x))/(np.pi*x), color= RED, stroke_width=2.8)

        self.add(
            VGroup(ax_time, ax_freq).arrange()
            )
