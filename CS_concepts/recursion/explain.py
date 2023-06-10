from manim import *

class CubeExample(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75*DEGREES, theta=-45*DEGREES,distance=6)

        axes = ThreeDAxes()
        cube = Cube(side_length=5.5, fill_opacity=0.95, fill_color=BLUE)
        
        cpl = [[0 for i in range(5)] for i in range(5)] # cube -> to plane, python list
        cpc = [UP,2*UP,ORIGIN,DOWN,2*DOWN] # some constant for autmatic the process
        slc = 0.9 # side for each cube
        foc = 0.9 # opacity for each cube
        fcc = RED # color for each cube
        swc = 2 # width of the stroke for each cube
        for i in range(5):
            for j in range(len(cpc)):
                cpl[i][j] = VGroup(
                    Cube(side_length=slc, fill_opacity=foc, fill_color=fcc, stroke_width=swc),
                    Cube(side_length=slc, fill_opacity=foc, fill_color=fcc, stroke_width=swc).shift(1*LEFT),
                    Cube(side_length=slc, fill_opacity=foc, fill_color=fcc, stroke_width=swc).shift(1*RIGHT),
                    Cube(side_length=slc, fill_opacity=foc, fill_color=fcc, stroke_width=swc).shift(2*LEFT),
                    Cube(side_length=slc, fill_opacity=foc, fill_color=fcc, stroke_width=swc).shift(2*RIGHT)
                ).shift(cpc[j])

        vcube_plane = VGroup(cpl[0][0],cpl[0][1],cpl[0][2],cpl[0][3],cpl[0][4])
        vcube_plane1 = VGroup(cpl[1][0],cpl[1][1],cpl[1][2],cpl[1][3],cpl[1][4])
        vcube_plane2 = VGroup(cpl[2][0],cpl[2][1],cpl[2][2],cpl[2][3],cpl[2][4])
        vcube_plane3 = VGroup(cpl[3][0],cpl[3][1],cpl[3][2],cpl[3][3],cpl[3][4])
        vcube_plane4 = VGroup(cpl[4][0],cpl[4][1],cpl[4][2],cpl[4][3],cpl[4][4])
       
        
        self.play(FadeIn(cube)) # representation of a complex problem
        self.move_camera(phi=60*DEGREES)
        self.begin_ambient_camera_rotation(
            rate = PI / 10, about = "theta"
        )
        self.wait(2)
        # take the complex and break with the objective to solve trivial problems
        self.play(FadeIn(vcube_plane))
        self.play(FadeIn(vcube_plane2.shift(OUT)),FadeIn(vcube_plane1.shift(IN)))
        self.play(FadeIn(vcube_plane3.shift(2*OUT)),FadeIn(vcube_plane4.shift(2*IN)))
        self.wait(2)
        self.play(FadeOut(cube))
        self.wait(8)
        
        self.stop_ambient_camera_rotation()
        