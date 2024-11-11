from manim import *
from constants import *
from utils import extend_3d, Intervalo, convert_svg_to_pdf

config.background_color = WHITE


cmbright = TexTemplate()
cmbright.add_to_preamble(r"\usepackage{cmbright}")
fontsize = 30


ax_time = Axes(x_range=[-5.5,5.5,1],
        y_range=[-1.2,1.2,1],
        x_length=6,
        y_length=CANVAS_HEIGHT/2,
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
)

ax_freq = Axes(x_range=[-1.5,1.5,0.5],
        y_range=[-1.2,1.2,1],
        x_length=6,
        y_length=CANVAS_HEIGHT/2,
        axis_config=dict(
            include_tip=False,
            include_ticks=True,
            include_numbers=True,
            tick_size=0.05,
            font_size=20,
            color=BLACK,
            stroke_width=2,
            decimal_number_config={"num_decimal_places": 1}
        )
)                

def f_shannon(x):
    return (np.sin(2*np.pi*x) - np.sin(np.pi*x))/(np.pi*x)

char_function = lambda x: (
    1 if (
        (-1 <= x <= -0.5) or 
        (0.5 <= x <= 1)
    ) else 0
)

car = ax_freq.plot(
        char_function,
        discontinuities=[-1, -0.5, 0.5, 1],
        color= RED
        )

shannon = ax_time.plot(lambda x : f_shannon(x), color=RED)  

txt_time = Tex(r"$\psi(x) =\dfrac{ \sin(2\pi x) - \sin(\pi x) }{\pi x}$",
                font_size=fontsize,
                tex_template=cmbright
            ).next_to(ax_time, DOWN, buff = 0.7)   

txt_freq = Tex(r"$\hat \psi(x) = {\bf 1}_{ \left [-1, -\frac 12 \right] \, \cup \, \left[ \frac 12, 1 \right] }$",
                font_size=fontsize,
                tex_template=cmbright
            ).next_to(ax_freq, DOWN, buff = 0.7)  

# self.add(ax1, shannon, label)

graf1 = VGroup(ax_time, txt_time, shannon)

graf2 = VGroup(ax_freq, txt_freq, car)

dosaxes = VGroup(graf1, graf2).arrange(buff = 1)

dosaxes.to_svg('pruebo_svg_wavelets_beamer.svg')
convert_svg_to_pdf('pruebo_svg_wavelets_beamer.svg', CANVAS_WIDTH, CANVAS_HEIGHT)



        
            




        

