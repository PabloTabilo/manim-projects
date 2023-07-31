from manim import *
from manim.camera.camera import Camera

class Miss(Scene):
    def __init__(self):
        super().__init__()
        self.n = 11
    
    def title_binary_lifting_table(self):
        title = Title("Binary Lifting Table").move_to(ORIGIN)
        self.play(Write(title))
        self.wait()
        self.play(FadeOut(title))
    
    def n_as_number_of_nodes(self):
        tx = Tex("n : number of nodes")
        self.play(Write(tx))
        self.wait()
        self.play(FadeOut(tx))
    
    def view_logs(self):
        tx1 = MathTex(r"\log_2(11) = 3.45943")
        tx2 = MathTex(r"\left \lceil{\log_2(11)}\right \rceil = 4")
        tx3 =MathTex(r"\frac{\log_{10}(11)}{\log_{10}(2)} = \log_2(11) = 3.45943")
        tx1.move_to(ORIGIN+UP*1)
        tx2.next_to(tx1,DOWN*1.5)
        tx3.next_to(tx2,DOWN*1.5)
        self.play(Write(tx1))
        self.play(Write(tx2))
        self.play(Write(tx3))
        self.wait(2)
        self.play(FadeOut(tx1),FadeOut(tx2),FadeOut(tx3))
    
    def big_o(self):
        tx1 = MathTex(r"O(n)")
        tx2 = MathTex(r"O(\log(n))")
        self.play(Write(tx1))
        self.wait()
        self.play(Transform(tx1,tx2))
        self.wait()
        self.play(FadeOut(tx2))
    
    def construct(self):
        self.title_binary_lifting_table()
        self.n_as_number_of_nodes()
        self.view_logs()
        self.big_o()