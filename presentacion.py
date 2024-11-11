from manim import *
from constants import *
from utils import extend_3d, Intervalo

config.background_color = WHITE

def make_axes(opacity=1):
    return Axes(
        x_range=[-7.111111111111111, 7.111111111111111, 1],
        y_range=[-4, 4, 1],
        x_length=2*7.111111111111111,
        y_length=8,
        tips=False,
        axis_config=dict(
            tick_size=0.08
        )
    ).set_opacity(opacity)

def make_numberplane(gridlines_opacity=0.6):
    return NumberPlane(
        x_range=[-9, 9, 1],
        y_range=[-6, 6, 1],
        background_line_style={
            "stroke_color": TEAL,
            "stroke_width": 1,
            "stroke_opacity": gridlines_opacity
        },
        axis_config=dict(
        color=TEAL,
        )
    )

def make_matrix_for_dilations(a, b, c, d):
    M = np.array([
        [a, b],
        [c, d]
        ])
    M = extend_3d(M)
    return M

def arcpolygon1():
    a = [0.8, 0.7, 0]
    b = [-0.6, 0.75, 0]
    c = [-0.1, -0.4, 0]
    d = [0.8, -0.9, 0]
    e = [0.5, 0.08, 0]
    ap1 = ArcPolygon(a, b, c, d, e,
                        radius=2.5,
                        color=RED,
                        fill_opacity=0.4,
                        ).set_stroke(width=0)
    return ap1

C1 = Polygon([1, 0, 0],
             [0,1, 0],
             [-1, 0, 1],
             [0, -1, 0])

C2 = Polygon([1/2, 1/2, 0],
            [-1/2, 1/2, 0],
            [-1/2, -1/2, 0],
            [1/2, -1/2, 0],)       

diamante = Difference(C1, C2).set_fill(color=RED, opacity=1).set_stroke(opacity=1, width=2)

def make_lattice(n=9, m=8, lattice_matrix = np.eye(3)):
    x_range_lattice = range(-n,n)
    y_range_lattice = range(-m,m)
    vg = VGroup()
    vg = VGroup(*[Dot(color=TEAL, radius=0.05).shift(lattice_matrix @ (i * LEFT + j * UP)) 
                        for i in x_range_lattice for j in y_range_lattice])
    return vg

def create_fila(mobject, n, M = np.eye(3)):
    lst = []
    for i in range(-n,n+1):
        lst.append(mobject.copy().shift(M @ (i*RIGHT)))
    return VGroup(*lst)

def create_speegle(cnst=2, iter=8): 
    b = []

    for i in range(0,iter):
        b += [
            Intervalo(0.5/(cnst**(i+1)), 0.5/(cnst**i), 0, 0.5).shift(i*UP/2),
            Intervalo(-0.5/(cnst**i), -0.5/(cnst**(i+1)), 0, 0.5).shift(i*UP/2),
            Intervalo(0.5/(cnst**(i+1)), 0.5/(cnst**i), -0, -0.5).shift(i*DOWN/2),
            Intervalo(-0.5/(cnst**i), -0.5/(cnst**(i+1)), -0, -0.5).shift(i*DOWN/2),    
        ]
        
    b = (Union(*b)
        .set_color(RED)
        .set_fill(opacity=1)
        .set_stroke(opacity=0)
        )
    
    return b

sp = create_speegle(2)

class Translations_by_lattice(Scene):
    def construct(self):

        intermediate_matrix = make_matrix_for_dilations(2, -2.3, 0.7, 1.1)
        matrix = make_matrix_for_dilations(1, 1/3, 1/2, 3/2)

        numberplane = make_numberplane()

        axes = make_axes(opacity=0.4)

        integer_lattice = make_lattice()

        intermediate_positions = [intermediate_matrix @ (dot.get_center()) for dot in integer_lattice]
        new_positions = [matrix @ (dot.get_center()) for dot in integer_lattice]


        # ejemplos de tiles

        ap1 = arcpolygon1() # el más general, empaca 2-redundantemente

        circulito = Circle(radius=0.3, color=RED, fill_opacity=0.6).stretch_to_fit_width(1.3).set_stroke(opacity=0) # el que empaca

        cubre = ( RoundedRectangle(corner_radius=0.25, height=1.2, width=1.4)
            .set_fill(color=RED, opacity=0.4)
            .set_stroke(opacity=0)
            .rotate(0.1*PI)
            .apply_matrix(matrix)
        )

        c = Square(1).set_fill(color=RED, opacity=0.4).set_stroke(opacity=1, width=2, color=RED)
        c.points[1] += 0.3*UP
        c.points[2] += 0.6*DOWN + 0.2*RIGHT
        c.points[6] += 0.3*LEFT
        c.points[5] += 0.3*RIGHT

        c.points[10] += 0.3*UP
        c.points[9] += 0.6*DOWN + 0.2*RIGHT
        c.points[13] += 0.3*LEFT
        c.points[14] += 0.3*RIGHT
        c.apply_matrix(matrix)
        tesela_rara = c # el que tesela 
                    
        def mover_horizontal_por_lattice(mobject, n, t1, t2, M = np.eye(3), pausa_inicial = False):
            for i in range(1,n):
                if i==1:
                    self.play(mobject
                            .copy()
                            .animate.shift(M @ RIGHT) , run_time=t1
                            )
                    if pausa_inicial == True:
                        self.wait()
                    self.play(mobject
                            .copy()
                            .animate.shift(M @ LEFT) , run_time=t2
                            )
                else:
                    self.play(mobject.copy().shift(M @ ((i-1)*RIGHT))
                            .animate.shift(M @ RIGHT) ,  run_time=t2*(0.6**i)
                            )
                    self.play(mobject.copy().shift(M @ ((i-1)*LEFT))
                            .animate.shift(M @ LEFT) ,  run_time=t2*(0.6**i)
                            )

        fila_ap1 = create_fila(ap1, 9, matrix)
        fila_tesela_rara = create_fila(tesela_rara, 9, matrix)

        def mover_vertical_por_lattice(mobject, n, t2, M = np.eye(3)):
            for i in range(1,n):
                    if i==1:
                        self.play(mobject
                                .copy()
                                .animate.shift(M @ UP) , run_time=t2
                                )
                        self.play(mobject
                                .copy()
                                .animate.shift(M @ DOWN) , run_time=t2
                                )
                    else:
                        self.play(mobject.copy().shift(M @ ((i-1)*UP))
                                .animate.shift(M @ UP) ,  run_time=t2*(0.6**i)
                                )
                        self.play(mobject.copy().shift(M @ ((i-1)*DOWN))
                                .animate.shift(M @ DOWN) ,  run_time=t2*(0.6**i)
                                )
        
        def translations(mobject, n, m, M = np.eye(3)):
            vg = VGroup(*[mobject.copy().shift(M @ (i*LEFT + j*UP)) for i in range(-n, n+1) for j in range(-m, m+1) ])
            return vg


        cmbright = TexTemplate()
        cmbright.add_to_preamble(r"\usepackage{cmbright}")
        fontsize = 30

        gamma = Tex(r'llamamos a $\Gamma$ ', r' una ``lattice" en $\mathbb R ^n$', font_size=fontsize, tex_template=cmbright).to_edge(LEFT, buff=1).shift(0.25*DOWN)
        zn = Tex(r'$\mathbb Z ^n$ ', font_size=fontsize, tex_template=cmbright).to_edge(LEFT, buff=1).shift(0.25*UP)
        rzn = Tex(r'$\Gamma = R \mathbb Z ^n$ con $R$ una matriz inversible', font_size=fontsize, tex_template=cmbright).to_edge(LEFT, buff=1).shift(0.25*UP)

        self.next_section('plano_con_ejes')
        self.add(numberplane)
        self.play(Create(axes), run_time=1)

        self.next_section('integer_lattice')
        self.play(FadeIn(integer_lattice, zn))

        self.next_section('lattice_general_1')
        self.play(FadeOut(zn))
        animations = [dot.animate.move_to(new_position) for dot, new_position in zip(integer_lattice, intermediate_positions)]
        self.play(ApplyMatrix(intermediate_matrix, numberplane), *animations, run_time=1)
        self.play(FadeOut(axes, numberplane))
        self.play(FadeIn(rzn))
        self.wait()

        self.next_section('lattice_general_2')
        self.play(FadeIn(axes, numberplane))
        animations = [dot.animate.move_to(new_position) for dot, new_position in zip(integer_lattice, new_positions)]
        self.play(ApplyMatrix(matrix @ np.linalg.inv(intermediate_matrix), numberplane), *animations, run_time=1)
        self.play(FadeOut(axes), FadeOut(numberplane))
        self.play(FadeIn(gamma))

        self.next_section('chau_lattice_general')  
        self.play(FadeOut(gamma, rzn))

        self.next_section('circulito')
        txt_W = MathTex(r'W', font_size=fontsize, tex_template=cmbright, color=RED).to_edge(LEFT, buff=1)
        txt_Wtrans = MathTex(r'\{ W + \gamma : \gamma \in \Gamma \}', font_size=fontsize, tex_template=cmbright).to_edge(LEFT, buff=1).shift(0.25*UP)
        txt_empaca = Tex(r'Decimos que $W$ \textit{empaca por traslaciones}', font_size=fontsize, tex_template=cmbright).to_edge(LEFT, buff=1).shift(0.25*UP)
        txt_empaca_def = Tex(r"si $\sum_{\gamma\in \Gamma} {\bf 1}_{W+\gamma} (x)  \leq 1$ para casi todo $x\in \mathbb R^n$", font_size=fontsize, tex_template=cmbright).to_edge(LEFT, buff=1).shift(0.25*UP)
        self.play(FadeIn(circulito, txt_W.next_to(circulito)), run_time=0.5)

        self.next_section('conjunto_que_empaca')
        mover_horizontal_por_lattice(circulito, 10, 1, 0.5, matrix, pausa_inicial=True)
        mover_vertical_por_lattice(create_fila(circulito, 9, matrix), 7, 0.3, matrix)
        self.play(FadeOut(txt_W), run_time=0.5)
        self.play(FadeIn(txt_Wtrans), run_time=0.5)
        self.next_section('chau_txt_traslaciones')
        self.play(FadeOut(txt_Wtrans), run_time=0.5)
        self.play(FadeIn(txt_empaca), run_time=0.5)
        self.play(FadeIn(txt_empaca_def.next_to(txt_empaca, DOWN)), run_time=0.5)

        self.next_section('chau_conjunto_que_empaca')        
        self.wait()
        self.play(
            *[FadeOut(mob)for mob in self.mobjects] , run_time=0.5
        )

        self.next_section('conjunto_general')

        txt_empaca_R = Tex(r'Decimos que $W$ \textit{empaca $M$-redundantemente por traslaciones}', font_size=fontsize, tex_template=cmbright).to_edge(LEFT, buff=1).shift(0.25*UP)
        txt_empaca_R_def = Tex(r"si $\sum_{\gamma\in \Gamma} {\bf 1}_{W+\gamma} (x)  \leq M$ para casi todo $x\in \mathbb R^n$", font_size=fontsize, tex_template=cmbright).to_edge(LEFT, buff=1).shift(0.25*UP)
        self.play(FadeIn(integer_lattice, ap1))
        self.next_section('traslaciones_conjunto_general')
        mover_horizontal_por_lattice(ap1, 9, 0.5, 0.5, matrix)
        mover_vertical_por_lattice(create_fila(ap1, 9, matrix), 7, 0.2, matrix)
        self.play(FadeIn(txt_empaca_R), run_time=0.5)
        self.play(FadeIn(txt_empaca_R_def.next_to(txt_empaca, DOWN)), run_time=0.5)

        self.next_section('chau_traslaciones_conjunto_general')        
        self.wait()
        self.play(
            *[FadeOut(mob)for mob in self.mobjects]
        )

        self.next_section('conjunto_que_cubre')
        txt_cubre = Tex(r'Decimos que $W$ \textit{cubre por traslaciones}', font_size=fontsize, tex_template=cmbright).to_edge(LEFT, buff=1).shift(0.25*UP)
        txt_cubre_def = Tex(r"si $\sum_{\gamma\in \Gamma} {\bf 1}_{W+\gamma} (x)  \geq 1$ para casi todo $x\in \mathbb R^n$", font_size=fontsize, tex_template=cmbright).to_edge(LEFT, buff=1).shift(0.25*UP)
        self.play(FadeIn(integer_lattice), FadeIn(cubre))
        mover_horizontal_por_lattice(cubre, 10, 0.3, 0.3, matrix)
        mover_vertical_por_lattice(create_fila(cubre, 9, matrix), 7, 0.2, matrix)
        self.play(FadeIn(txt_cubre), run_time=0.5)
        self.play(FadeIn(txt_cubre_def.next_to(txt_empaca, DOWN)), run_time=0.5)
        self.next_section('chau_conjunto_que_cubre')        
        self.wait()
        self.play(
            *[FadeOut(mob)for mob in self.mobjects]
        )

        self.next_section('tesela_rara')
        self.play(FadeIn(integer_lattice), FadeIn(tesela_rara))

        self.next_section('conjunto_que_tesela')
        txt_tesela = Tex(r'Decimos que $W$ \textit{tesela por traslaciones}', font_size=fontsize, tex_template=cmbright).to_edge(LEFT, buff=1).shift(0.25*UP)
        txt_tesela_def = Tex(r"si $\sum_{\gamma\in \Gamma} {\bf 1}_{W+\gamma} (x) = 1$ para casi todo $x\in \mathbb R^n$", font_size=fontsize, tex_template=cmbright).to_edge(LEFT, buff=1).shift(0.25*UP)
        mover_horizontal_por_lattice(tesela_rara, 10, 0.3, 0.3, matrix)
        mover_vertical_por_lattice(create_fila(tesela_rara, 9, matrix), 7, 0.2, matrix)
        self.play(FadeIn(txt_tesela), run_time=0.5)
        self.play(FadeIn(txt_tesela_def.next_to(txt_empaca, DOWN)), run_time=0.5)
        self.wait()

        self.next_section('chau_conjunto_que_tesela')        
        self.wait()
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )


class Dilations_by_a(Scene):
    def construct(self):
        cmbright = TexTemplate()
        cmbright.add_to_preamble(r"\usepackage{cmbright}")
        fontsize = 30

        matrix = make_matrix_for_dilations(1, 1/3, -1/2, 3/2)
        numberplane = make_numberplane()
        axes = make_axes(opacity=0.4)

        sq = RoundedRectangle(corner_radius=0.1, width=1.5, height=1.5, fill_opacity=0.1, stroke_opacity=0.7, color=RED)
        txt_matrix= Tex(r'$A$ una matriz inversible de $n\times n$', font_size=fontsize, tex_template=cmbright).to_edge(LEFT, buff=1).shift(0.25*UP)
        txt_dilations= MathTex(r'\{ A\,^j (W) : j \in \mathbb Z \}', font_size=fontsize, tex_template=cmbright).to_edge(LEFT, buff=1).shift(0.25*UP)
        txt_W= MathTex(r'W', font_size=fontsize, tex_template=cmbright, color=RED).next_to(sq, LEFT+UP, buff=0.1)

        txt_dilation_tiling= Tex(r'Decimos que $W$ \textit{tesela por dilataciones de A}', font_size=fontsize, tex_template=cmbright).to_edge(LEFT, buff=1).shift(0.25*UP)
        txt_dilation_tiling_def= Tex(r'si $\sum_{j \in \mathbb Z} {\bf 1}_{A^{\,j}(W)}(x) = 1$ para casi todo $x \in \mathbb R^n$', font_size=fontsize, tex_template=cmbright).next_to(txt_dilation_tiling, DOWN)


        self.next_section('plano')
        self.add(numberplane)
        self.play(Create(axes), run_time=1)
        self.play(FadeIn(txt_matrix))
        self.next_section('dilatacion')        
        self.play(ApplyMatrix(matrix, numberplane), run_time=1)

        self.next_section('conjunto')
        self.play(FadeOut(numberplane, txt_matrix))
        numberplane = numberplane.apply_matrix(np.linalg.inv(matrix))
        self.play(FadeIn(sq, txt_W))
        self.wait(1)

        self.next_section('conjunto_dilataciones')
        self.play(FadeOut(txt_W))

        sq_dilates=[sq]
        for i in range(1,5):
            self.play(FadeIn(numberplane) , run_time=0.3)
            if i==1:
                s =  sq.copy().apply_matrix(np.linalg.matrix_power(matrix, i-1))
                self.play(ApplyMatrix(matrix, s), ApplyMatrix(matrix, numberplane) , run_time=0.3)
                self.wait()
                self.play(FadeOut(numberplane) , run_time=0.3)
                sq_dilates.append(s)
                numberplane = numberplane.apply_matrix(np.linalg.inv(matrix))
            else:
                s =  sq.copy().apply_matrix(np.linalg.matrix_power(matrix, i-1))
                self.play(ApplyMatrix(matrix, s), ApplyMatrix(matrix, numberplane) , run_time=0.3)
                self.play(FadeOut(numberplane) , run_time=0.3)
                sq_dilates.append(s)
                numberplane = numberplane.apply_matrix(np.linalg.inv(matrix))
        self.wait()
        self.next_section('dilataciones_inversas')
        for i in range(1,5):
            s =  sq.copy().apply_matrix(np.linalg.matrix_power(matrix, -(i-1)))
            self.play(ApplyMatrix(np.linalg.inv(matrix), s), ApplyMatrix(np.linalg.inv(matrix), numberplane) , run_time=0.3)
            self.play(FadeOut(numberplane) , run_time=0.3)
            sq_dilates.append(s)
            numberplane = numberplane.apply_matrix(matrix)
        self.play(FadeIn(txt_dilations))
        self.wait()
        self.next_section('chau_conjunto_dilataciones')
        self.play(FadeOut(*sq_dilates))
        
        numberplane = make_numberplane()
        self.next_section('conjunto_que_tesela')
        matrix2 = make_matrix_for_dilations(1.5, 1/3, -0.75, 3/2)
        matrix2inv = np.linalg.inv(matrix2)
        c = Circle(radius=1, fill_opacity=0.2, stroke_opacity=0.5, color=RED)
        c2 = c.copy().apply_matrix(np.linalg.inv(matrix2))
        dt = Difference(c, c2, fill_opacity=0.2, stroke_opacity=0.5, color=RED)

        self.play(FadeIn(dt))
        sq_dilates=[dt]

        self.next_section('accion_conjunto_que_tesela')
        accel = 0.8
        for i in range(1,7):
            self.play(FadeIn(numberplane) , run_time=0.3*(accel**i))
            s =  dt.copy().apply_matrix(np.linalg.matrix_power(matrix2, i-1))
            self.play(ApplyMatrix(matrix2, s), ApplyMatrix(matrix2, numberplane) , run_time=0.3*(accel**i))
            self.play(FadeOut(numberplane) , run_time=0.3*(accel**i))
            sq_dilates.append(s)
            numberplane = numberplane.apply_matrix(np.linalg.inv(matrix2))
        for i in range(1,6):
            self.play(FadeIn(numberplane) , run_time=0.3*(accel**i))
            s =  dt.copy().apply_matrix(np.linalg.matrix_power(matrix2, -(i-1)))
            self.play(ApplyMatrix(matrix2inv, s), ApplyMatrix(matrix2inv, numberplane) , run_time=0.3*(accel**i))
            self.play(FadeOut(numberplane) , run_time=0.3*(accel**i))
            sq_dilates.append(s)
            numberplane = numberplane.apply_matrix(matrix2)
        self.wait()
        self.next_section('def_conjunto_que_tesela')
        self.play(FadeOut(txt_dilations))
        self.play(FadeIn(txt_dilation_tiling))
        self.play(FadeIn(txt_dilation_tiling_def))
        self.wait()
        self.next_section('chau_conjunto_que_tesela')
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )

class Wavelet_graphs(Scene):
    def construct(self):
        cmbright = TexTemplate()
        cmbright.add_to_preamble(r"\usepackage{cmbright}")
        fontsize = 35


        ax1 = Axes(x_range=[-9,9,1],
                y_range=[-2.5,2.5,1],
                x_length=CANVAS_WIDTH,
                y_length=CANVAS_HEIGHT,
                axis_config=dict(
                    include_tip=False,
                    include_ticks=True,
                    include_numbers=True,
                    tick_size=0.05,
                    font_size=fontsize,
                    color=BLACK,
                    stroke_width=2,
                    decimal_number_config={"num_decimal_places": 0}
                )
        )        

        a = ValueTracker(1)

        k = ValueTracker(0)

        def f_shannon(x):
            return (np.sin(2*np.pi*x) - np.sin(np.pi*x))/(np.pi*x)


        shannon = ax1.plot(lambda x : f_shannon(x), color=RED, x_range=[-9,9,0.05])

        shannon.add_updater(
            lambda mob: mob.become(
                ax1.plot(
                lambda x : a.get_value()**(-1/2) * f_shannon((x - k.get_value()) / a.get_value()),
                color = RED,
                x_range=[-9,9,0.05]
            )) 
        )

        a_number = DecimalNumber(
            a.get_value(),
            color=RED,
            num_decimal_places=1,
            show_ellipsis=False
            )
        
        k_number = DecimalNumber(
            a.get_value(),
            color=RED,
            num_decimal_places=1,
            show_ellipsis=False
            )
        
        a_number.add_updater(
            lambda mob : mob.set_value(a.get_value())
        )

        k_number.add_updater(
            lambda mob : mob.set_value(k.get_value())
        )

        label_dilation = always_redraw(
            lambda : ax1.get_graph_label(
                shannon,
                MathTex(
                        r"\mathfrak D_a \psi(x), \ a=" + str(round(a.get_value(), 2)),
                        font_size=fontsize,
                        tex_template=cmbright
                        ),
                direction=np.array([0,1,0])
            )
        )

        label_translation = always_redraw(
            lambda : ax1.get_graph_label(
                shannon,
                MathTex(
                        r"\mathfrak T_k \psi(x), \ k=" + str(round(k.get_value(), 2)),
                        font_size=fontsize,
                        tex_template=cmbright
                        ),
                direction=np.array([0,1,0])
            )
        )

        label = always_redraw(
            lambda : ax1.get_graph_label(
                shannon,
                MathTex(
                        r"\mathfrak T_k \mathfrak D_a \psi(x) \\ \ a="
                            + str(round(a.get_value(), 2))
                            + r"\\ \ k="
                            + str(round(k.get_value(), 2)),
                        font_size=fontsize,
                        tex_template=cmbright
                ),
                direction=np.array([0,1,0])
        )).set_color(RED_E)

        # self.add(ax1, shannon, label)

        self.next_section('mostrar_wavelet')
        self.play(Create(ax1))
        self.play(Write(shannon), run_time=1.5)
        self.play(FadeIn(label), run_time=0.3)
        self.wait(0.5)
        
        self.next_section('dilatar_wavelet')
        self.play(a.animate.set_value(3), rate_func=smoothstep, run_time=2)
        self.wait()
        self.play(a.animate.set_value(0.3), rate_func=smoothstep, run_time=2)
        self.wait(1)

        self.next_section('trasladar_wavelet')
        self.play(k.animate.set_value(4), rate_func=smoothstep)
        self.wait(0.5)

        self.next_section('seguir_y_terminar')
        self.play(a.animate.set_value(1), rate_func=smoothstep, run_time=2)
        self.wait(0.5)
        self.play(k.animate.set_value(-5), rate_func=there_and_back, run_time=4)
        self.play(a.animate.set_value(1), k.animate.set_value(1), rate_func=smoothstep)

class WS(Scene):
    
    def construct(self):

        cmbright = TexTemplate()
        cmbright.add_to_preamble(r"\usepackage{cmbright}")
        fontsize = 30

        plane = make_numberplane()

        A = make_matrix_for_dilations(1, 1, 1, -1)
        A_inv = np.linalg.inv(A)

        txt = MathTex(r"A=\begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}, \quad \Gamma = \mathbb Z^2", tex_template=cmbright, font_size=fontsize).to_corner(UL)

        def next_esp(mob):
            dir = None
            x = mob.get_x()
            y = mob.get_y()
            if (y <= x < -y + 1) or (x == 0 == y):
                dir = RIGHT
            if (-x + 1 <= y < x):
                dir = UP
            if (-y < x <= y):
                dir = LEFT
            if (x < y <= -x):
                dir = DOWN
            return dir

        self.next_section('mostrar_plano')
        self.add(plane, txt)
        self.wait()

        self.next_section('mostrar_diamante')
        self.play(FadeIn(diamante))
        self.wait()

        colors = {0: RED, 1: BLUE, 2: PURPLE, 3: GOLD, 4: GREEN}

        diam = diamante.copy()

        self.next_section('dilataciones_diamante')
        trasladados1 = [diam] # se agranda y rota por separado
        trasladados2 = [diam]
        rt = .8
        for j in range(7):
            c1 = trasladados1[-1].copy().set_fill(color=colors[(j+1)%len(colors)])
            c2 = trasladados2[-1].copy().set_fill(color=colors[(j+1)%len(colors)])
            self.play(ScaleInPlace(c1, np.sqrt(2)), ScaleInPlace(c2, np.sqrt(1/2)), run_time=rt, rate_func=smoothstep)
            self.play(Rotate(c1, angle=PI/4), Rotate(c2, angle=-PI/4), run_time=rt, rate_func=smoothstep)
            trasladados1.append(c1)
            trasladados2.append(c2)
            rt = rt * .8
            txt.set_z_index(c1.z_index + 1)
        self.wait()

        self.next_section('chau_dilataciones_diamante')        
        self.play(FadeOut(*trasladados1, *trasladados2))
        self.wait()


        # t = ValueTracker(0)

        # def mob_roto_homotecia(mob, angle, scale, t): # t va a ir de 0 a 1
        #     return always_redraw(
        #         lambda: mob.copy()
        #             .rotate(t.get_value() * angle)
        #             .scale(
        #                 (1-t.get_value()) + t.get_value() * scale
        #                 )
        #     )

        # self.next_section('dilataciones_diamante')

        # trasladados1 = [diam]  # HAY TERRIBLE BUGCITO EN LOS ALWAYS_REDRAW. NO PERMITEN CAMBIAR EL COLOR EN CADA FRAME, SE PONEN NEGROS
        # trasladados2 = [diam]
        # rt = 0.9
        # for j in range(4):
        #     t_aux = ValueTracker(0)
        #     col=(j+1)%len(colors)
        #     c1 = mob_roto_homotecia(trasladados1[-1], PI/4, np.sqrt(2), t_aux, col)
        #     c2 = mob_roto_homotecia(trasladados2[-1], PI/4, np.sqrt(1/2), t_aux, col)
        #     self.add(
        #         c1,
        #         c2
        #         )
        #     self.play(t_aux.animate.set_value(1), run_time = rt)
        #     trasladados1.append(c1)
        #     trasladados2.append(c2)
        #     rt = rt * .6
        # self.wait()
        # self.play(FadeOut(*trasladados1))


        # el que ya funcionó

        self.next_section('traslaciones_diamante')
        c = diam
        trasladados = [c]
        for n in range(250): # traslada los diamantes en espiral
            x = int(c.get_x())
            y = int(c.get_y())
            idx = x + 2*y
            c = c.copy().set_fill(color=colors[idx%len(colors)])
            trasladados.append(c)
            if n<30:
                self.play(c.animate.shift(next_esp(c)), run_time=0.9*(0.9)**n)
            else:
                c.shift(next_esp(c))
            txt.set_z_index(c.z_index + 1)
        ultimos = trasladados[30:]
        self.play(FadeIn(*ultimos))
        self.wait(2)
        
        # self.next_section('chau_traslaciones_diamante')
        # self.play(FadeOut(*trasladados))



class Speegle(Scene):
    
    def construct(self):

        colors = {0: RED, 1: BLUE, 2: PURPLE_A, 3: GOLD, 4: GREEN}

        cmbright = TexTemplate()
        cmbright.add_to_preamble(r"\usepackage{cmbright}")
        fontsize = 30

        plane = make_numberplane()

        A = make_matrix_for_dilations(2, 0, 0, 1)
        A_inv = np.linalg.inv(A)

        txt = MathTex(r"A=\begin{pmatrix} 2 & 0 \\ 0 & 1 \end{pmatrix}, \quad \Gamma = \mathbb Z^2", tex_template=cmbright, font_size=fontsize).to_corner(UL)

        self.next_section('mostrar_plano')
        self.add(plane, txt)
        self.wait()

        self.next_section('mostrar_speegle')
        self.add(sp)
        self.wait()

        self.next_section('dilatar_speegle')
        dilatados = [sp.copy()]
        dil_iters = 11
        
        def idx(i):
            return (i+1) % 5

        for i in range(dil_iters):
            s = dilatados[-1].set_color(colors[idx(i)])
            self.add(s)
            self.play(ApplyMatrix(A, s), run_time=1.5*0.9**i)
            dilatados.append(s.copy())
            txt.set_z_index(s.z_index + 1)
        self.wait()

        self.next_section('chau_dilatar_speegle')


        self.play(FadeOut(*dilatados))

        self.next_section('trasladar_speegle')

        trasladados_hor1 = [sp.copy()]
        trasladados_hor2 = [sp.copy()]

        for i in range(7):
            s1 = trasladados_hor1[-1].set_color(colors[idx(i)])
            s2 = trasladados_hor2[-1].set_color(colors[idx(i)])
            self.add(s1, s2)
            self.play(s1.animate.shift(RIGHT), run_time=0.6**i)
            self.play(s2.animate.shift(LEFT), run_time=0.6**i)
            trasladados_hor1.append(s1.copy())
            trasladados_hor2.append(s2.copy())

        self.wait()

        fila_lst =  trasladados_hor1 + trasladados_hor2 + [sp.copy()]
        fila = VGroup(*fila_lst)
        filas_up = [fila.copy()]
        filas_down = [fila.copy()]

        def cambiar_colores(lst, j):
            i = j
            for m in lst:
                m.set_color(colors[i%5])
                i += 1

        for i in range(6):
            fila_up = filas_up[-1].copy()
            fila_down = filas_down[-1].copy()

            cambiar_colores(fila_up, i)
            cambiar_colores(fila_down, i)

            self.play(fila_up.animate.shift(UP), run_time=0.8**i)
            self.play(fila_down.animate.shift(DOWN), run_time=0.8**i)

            filas_up.append(fila_up)
            filas_down.append(fila_down)


        
class Tesela_recta(Scene):
    def construct(self):
        cols = {0: RED, 1: BLUE, 2: GOLD, 3: GREEN}

        nl = NumberLine(
            x_range=[-8.5,8.5,1],
            include_numbers=True,
            font_size=20,
            tick_size=0.15
        )

        cjto = Union(
            Intervalo(-1, -1/2, -0.1 ,0.1),
            Intervalo(1/2, 1, -0.1 ,0.1)
        ).set_fill(color=RED, opacity=1).set_stroke(opacity=0)

        dilatados = [cjto]

        self.next_section('mostrar_cjto')
        self.add(nl, cjto)
        self.wait()

        self.next_section('dilatar_cjto')
        for i in range(3):
            def idx(i): return i%4
            c = dilatados[-1].copy().set_color(cols[idx(i+1)])
            self.play(c.animate.stretch_to_fit_width(2**(i+2)), run_time=1)
            dilatados.append(c)

        contraidos = [cjto]

        for i in range(4):
            def idx(i): return i%4
            c = contraidos[-1].copy().set_color(cols[idx(-i-1)])
            self.play(c.animate.stretch_to_fit_width(2**(-(i))), run_time=1)
            contraidos.append(c)

        del dilatados[0]
        del contraidos[0]

        self.next_section('trasladar_cjto')
        self.play(FadeOut(*dilatados, *contraidos))

        derecha = [cjto]
        izquierda = [cjto]
        for i in range(7):
            def idx(i): return i%4
            c1 = derecha[-1].copy().set_color(cols[idx(i+1)])
            c2 = izquierda[-1].copy().set_color(cols[idx(-i-1)])
            self.play(c1.animate.shift(RIGHT), run_time=0.6**i)
            self.play(c2.animate.shift(LEFT), run_time=0.6**i)
            derecha.append(c1)
            izquierda.append(c2)
        self.wait()

class Chiste(Scene):
    def construct(self):
        cmbright = TexTemplate()
        cmbright.add_to_preamble(r"\usepackage{cmbright}")
        fontsize = 30

        plane = make_numberplane()

        txt = MathTex(r"A=\begin{pmatrix} 3 & 0 \\ 0 & \frac12 \end{pmatrix}, \quad \Gamma = \mathbb Z^2", tex_template=cmbright, font_size=fontsize).to_corner(UL)

        self.add(plane, txt)



class Final(Scene):
    def construct(self):
        colors = {0: RED, 1: BLUE, 2: PURPLE, 3: GOLD, 4: GREEN}

        cmbright = TexTemplate()
        cmbright.add_to_preamble(r"\usepackage{cmbright}")
        fontsize = 30

        gracias = Tex(r'¡Gracias!', tex_template=cmbright, font_size=fontsize)
        self.play(Rotate(gracias, PI/10))
        gracias.move_to([0,0,0])

        plane = make_numberplane()
        c = gracias
        A = make_matrix_for_dilations(2, 0.7, 0, 2)
        self.play(FadeIn(plane))
                # dilates = [c]

        def next_esp(mob):
            dir = None
            x = mob.get_x()
            y = mob.get_y()
            if (y <= x < -y + 1) or (x == 0 == y):
                dir = RIGHT
            if (-x + 1 <= y < x):
                dir = UP
            if (-y < x <= y):
                dir = LEFT
            if (x < y <= -x):
                dir = DOWN
            return dir
        
        trasladados = []
        
        for n in range(50): # traslada los diamantes en espiral
            x = int(c.get_x())
            y = int(c.get_y())
            idx = x + 2*y
            c = c.copy().set_fill(color=colors[idx%len(colors)])
            trasladados.append(c)
            self.play(c.animate.shift(next_esp(c)), run_time=0.9*(0.6)**n)

        self.play(FadeOut(*trasladados))

        dilates = [gracias]
        self.play(Rotate(gracias, -PI/10))
        c = gracias
        accel = 0.8
        for i in range(1,7):
            if i != 1:
                self.play(FadeIn(plane) , run_time=0.3*(accel**i))
            s =  c.copy().apply_matrix(np.linalg.matrix_power(A, i-1)).set_color(colors[i%5]).set_z_index(-i+1)
            self.add(s)
            self.play(ApplyMatrix(A, s), ApplyMatrix(A, plane) , run_time=0.3*(accel**i))
            self.play(FadeOut(plane) , run_time=0.3*(accel**i))
            dilates.append(s)
            plane = plane.apply_matrix(np.linalg.inv(A))


class Shear(Scene):
    def construct(self):

        cmbright = TexTemplate()
        cmbright.add_to_preamble(r"\usepackage{cmbright}")
        fontsize = 30

        plane = make_numberplane()
        axes = make_axes(opacity=0.3)

        A = make_matrix_for_dilations(1, 1, 0, 1)
        A_inv = np.linalg.inv(A)

        txt = MathTex(
            r"A=\begin{pmatrix} 1 & 1 \\ 0 & 1 \end{pmatrix}", tex_template=cmbright, font_size=fontsize
                      ).to_corner(UL).shift(DOWN)

        cono=Union(
        Polygon([0,0,0], [0, 5, 0], [5, 5, 0]),
        Polygon([0,0,0], [0, -5, 0], [-5, -5, 0]),
        color=RED,
        fill_opacity=1,
        stroke_width=0
        )
        # cono=Intervalo(0, 1, 0, 1)

        self.next_section('mostrar_plano')
        self.add(plane, axes, txt)
        self.wait()
        
        self.next_section('mostrar_accion')
        self.play(ApplyMatrix(A, plane), run_time=0.7)
        self.wait()

        self.next_section('mostrar_cono')
        self.play(ApplyMatrix(A_inv, plane), run_time=0.3)
        self.play(FadeIn(cono))
        self.wait()

        colors = {0: RED, 1: BLUE, 2: PURPLE, 3: GOLD, 4: GREEN}

        diam = diamante.copy()

        self.next_section('dilataciones_cono')
        rt = .7
        dilatados = [cono]
        for j in range(10):
            c = dilatados[-1].copy().set_fill(color=colors[(j+1)%5])
            self.add(c)
            self.play(ApplyMatrix(A, c), ApplyMatrix(A, plane), run_time=rt**j)
            dilatados.append(c.copy())
            self.play(FadeOut(plane), run_time=rt**(j+2))
            plane.apply_matrix(A_inv)
            self.play(FadeIn(plane), run_time=rt**(j+2))
        self.remove(plane)
        self.wait(0.2)
            
        self.next_section('contracciones_cono')

        dilatados = [cono]
        rt = .5
        self.add(plane)
        for j in range(10):
            c = dilatados[-1].copy().set_fill(color=colors[(j+1)%5])
            self.add(c)
            self.play(ApplyMatrix(A_inv, c), ApplyMatrix(A_inv, plane), run_time=rt**j)
            dilatados.append(c.copy())
            self.remove(plane)
            plane.apply_matrix(A)
            self.add(plane)
            txt.set_z_index(j+1)
        self.remove(plane)
        self.wait(0.2)

class Expansiva(Scene):
    def construct(self):
        cmbright = TexTemplate()
        cmbright.add_to_preamble(r"\usepackage{cmbright}")
        fontsize = 30
        numberplane = make_numberplane()
        axes = make_axes(opacity=0.4)

        txt1 = Tex(
            r'Como $A$ es expansiva', font_size=fontsize, tex_template=cmbright
            )
        txt2 = Tex(
            r'existe un conjunto acotado', font_size=fontsize, tex_template=cmbright
            )
        txt3 = Tex(
            r'que tesela por dilataciones de $A$.', font_size=fontsize, tex_template=cmbright
            )
        txt_hipexp = VGroup(txt1, txt2, txt3)
        txt_hipexp.arrange(DOWN, center=False, aligned_edge=LEFT).to_corner(UL).shift(2*DOWN)

        txt4 = Tex(
            r'Para toda lattice $\Gamma$, existe un conjunto', font_size=fontsize, tex_template=cmbright
            )
        txt5 = Tex(
            r' que tesela por traslaciones de $\Gamma$', font_size=fontsize, tex_template=cmbright
            )
        txt6 = Tex(
            r'y contiene un entorno del origen.', font_size=fontsize, tex_template=cmbright
            )
        txt_hipg = VGroup(txt4, txt5, txt6)
        txt_hipg.arrange(DOWN, center=False, aligned_edge=LEFT).to_corner(UL).shift(2*DOWN)


        txt7 = Tex(
            r'$\exists k$ suf. grande tal que $A^{-k}$', font_size=fontsize, tex_template=cmbright
            )
        txt8 = Tex(
            r'contrae a un conjunto dentro del otro.', font_size=fontsize, tex_template=cmbright
            )
        txt_contrae = VGroup(txt7, txt8)
        txt_contrae.arrange(DOWN, center=False, aligned_edge=LEFT).to_corner(UL).shift(2*DOWN)

        txt7 = Tex(
            r'Este conjunto tesela por dilataciones de $A$', font_size=fontsize, tex_template=cmbright
            )
        txt8 = Tex(
            r'y empaca por traslaciones de $\Gamma$.', font_size=fontsize, tex_template=cmbright
            )
        txt_cumple = VGroup(txt7, txt8)
        txt_cumple.arrange(DOWN, center=False, aligned_edge=LEFT).to_corner(UL).shift(2*DOWN)

        txt_fin = Tex(
            r'¡Entonces existe un $(A, \Gamma)$ wavelet set!', font_size=fontsize, tex_template=cmbright
            ).to_corner(UL).shift(2*DOWN)

        self.next_section('conjunto_dilataciones')
        
        numberplane = make_numberplane()
        self.next_section('V')
        matrix2 = make_matrix_for_dilations(1.5, 1/3, -0.75, 3/2)
        matrix2inv = np.linalg.inv(matrix2)
        c = Circle(radius=1, fill_opacity=0.2, stroke_opacity=0.5, color=RED)
        c2 = c.copy().apply_matrix(np.linalg.inv(matrix2))
        V = Difference(c, c2, fill_opacity=0.2, stroke_opacity=0.5, color=RED)

        self.play(FadeIn(txt_hipexp))
        self.play(FadeIn(axes, V))
        V_dilates=[V]

        self.next_section('V_tesela')
        accel = 0.5
        for i in range(1,7):
            self.play(FadeIn(numberplane) , run_time=0.3*(accel**(i-1)))
            s =  V.copy().apply_matrix(np.linalg.matrix_power(matrix2, i-1))
            self.play(ApplyMatrix(matrix2, s), ApplyMatrix(matrix2, numberplane) , run_time=0.3*(accel**(i-1)))
            self.play(FadeOut(numberplane) , run_time=0.3*(accel**(i-1)))
            V_dilates.append(s)
            numberplane = numberplane.apply_matrix(np.linalg.inv(matrix2))
        for i in range(1,4):
            self.play(FadeIn(numberplane) , run_time=0.3*(accel**(i-1)))
            s =  V.copy().apply_matrix(np.linalg.matrix_power(matrix2, -(i-1)))
            self.play(ApplyMatrix(matrix2inv, s), ApplyMatrix(matrix2inv, numberplane) , run_time=0.3*(accel**(i-1)))
            self.play(FadeOut(numberplane) , run_time=0.3*(accel**(i-1)))
            V_dilates.append(s)
            numberplane = numberplane.apply_matrix(matrix2)
        self.wait()
        self.play(FadeOut(*V_dilates[1:]))
        self.play(FadeOut(V, txt_hipexp))

        self.next_section('mostrar_lattice')

        lattice = make_lattice()
        A = make_matrix_for_dilations(1.1, -0.5, 0.2, 1.2)
        A = A * 1.2
        new_positions = [A @ (dot.get_center()) for dot in lattice]
        for dot, new_position in zip(lattice, new_positions):
            dot.move_to(new_position)
        self.play(FadeIn(lattice))
        self.wait(.2)

        self.next_section('F_existe')

        F = Intervalo(-0.5, 0.5, -0.5, 0.5).apply_matrix(A).set_fill(color=BLUE, opacity=0.1).set_stroke(opacity=0.7, color=BLUE)
        self.play(FadeIn(F, txt_hipg))
        self.wait()

        fila = [F]
        for i in range(1,7):
            r = F.copy()
            l = F.copy()
            self.add(r.shift(A @ (i*RIGHT)))
            self.wait(0.1)
            self.add(l.shift(A @ (i*LEFT)))
            self.wait(0.1)
            fila.append(r)
            fila.append(l)

        mob_fila = VGroup(*fila)
        filas = [mob_fila]
        for j in range(1, 4):
            u = mob_fila.copy()
            d = mob_fila.copy()
            self.add(u.shift(A @ (j*UP)))
            self.wait(0.1)
            self.add(d.shift(A @ (j*DOWN)))
            self.wait(0.1)
            filas.append(u)
            filas.append(d)
        self.wait()

        filas[0] -= F

        self.next_section('vuelve_V')
        self.play(FadeOut(*filas, txt_hipg))


        self.play(FadeIn(V))
        self.wait()

        self.next_section('V_se_contrae')
        self.play(FadeIn(txt_contrae))
        V_chicos = [V]
        for i in range(1,3):
            self.play(FadeIn(numberplane) , run_time=0.3)
            s =  V.copy().apply_matrix(np.linalg.matrix_power(matrix2, -(i-1)))
            self.play(ApplyMatrix(matrix2inv, s), ApplyMatrix(matrix2inv, numberplane) , run_time=0.3)
            self.play(FadeOut(numberplane) , run_time=0.3)
            V_chicos.append(s)
            numberplane = numberplane.apply_matrix(matrix2)
        self.play(FadeOut(*V_chicos[:-1]))
        self.wait()
 

       
        W = V_chicos[-1]

        self.next_section('W_tesela')
        self.play(FadeOut(txt_contrae))

        self.next_section('pausita_dramatica')
        self.play(FadeIn(*V_dilates, txt_cumple[0]))
        self.wait(.2)

        self.next_section('chau_W_tesela')
        self.play(FadeOut(*V_dilates))
        self.wait(.2)

        self.next_section('W_empaca')
        self.play(FadeIn(txt_cumple[1]))
        filaw = [W]
        for i in range(1,7):
            r = W.copy()
            l = W.copy()
            self.add(r.shift(A @ (i*RIGHT)))
            self.wait(0.1)
            self.add(l.shift(A @ (i*LEFT)))
            self.wait(0.1)
            filaw.append(r)
            filaw.append(l)

        mob_filaw = VGroup(*filaw)
        filasw = [mob_filaw]
        for j in range(1, 4):
            u = mob_filaw.copy()
            d = mob_filaw.copy()
            self.add(u.shift(A @ (j*UP)))
            self.wait(0.1)
            self.add(d.shift(A @ (j*DOWN)))
            self.wait(0.1)
            filasw.append(u)
            filasw.append(d)
        self.wait()

        self.next_section('mostrar_w_empaca')
        self.play(FadeIn(*filas))
        self.wait()

        filasw[0] -= W  

        self.next_section('W_solito')
        self.play(FadeOut(*filas, *filasw, F, txt_cumple))
        self.play(FadeIn(txt_fin))
