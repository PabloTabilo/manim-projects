from manim import *

# any integer number x, i can use binary combination to get it
# For example,
# 19 = 2^4 + 2^1 + 2^0
# 10011
# bitwise operation
# floor(log2(19)) = log = 4 
# SUM = 0 to log2 inclusive
# kth = SUM 2^i * (k & (1<<i) != 0)
# 19  = 2^0 * (10011 & 00001 != 0) + 2^1 * (10011 & 00010 != 0) + 2^2 * (10011 & 00100 != 0) + 2^3 * (10011 & 01000 != 0) + 2^4 * (10011 & 10000 != 0)
# SUM 1 to log

class GeneralizationCase(Scene):
    def __init__(self):
        super().__init__()
        self.num = 19
        self.log = 0
        self.bits = 8
        while((1 << self.log) < self.num): self.log+=1
    
    def calculate_size_of_l(self):
        tx1 = Tex("if")
        tx1.move_to(ORIGIN+1.0*UP)
        tx2 = MathTex(f"k = {self.num}",color=YELLOW)
        tx2.next_to(tx1,RIGHT)
        p1 = VGroup(tx1,tx2)
        
        tx3 = Tex("and we want to find an")
        tx4 = MathTex("l",color=YELLOW)
        tx5 = Tex("that achieves:")
        tx3.next_to(tx4,LEFT)
        tx5.next_to(tx4,RIGHT)
        p2 = VGroup(tx3,tx4,tx5)
        p2.next_to(p1,DOWN)
        
        tx6 = MathTex(f"2^l \ge k",color=YELLOW)
        tx6.next_to(p2,DOWN)
        
        g1 = VGroup(p1,p2,tx6)
        g1.center() # Center the group on the screen
        
        self.play(Write(p1), Write(p2),run_time=0.5)
        self.play(Write(tx6))
        self.wait()
        self.play(*[FadeOut(elem) for elem in g1])
        
        tx7 = Tex("For example, with")
        tx7.move_to(ORIGIN+1.0*UP)
        tx8 = MathTex(f"k = {self.num}",color=YELLOW)
        tx8.next_to(tx7,RIGHT)
        p3 = VGroup(tx7,tx8)
        
        tx9 = MathTex(f"2^{self.log} \ge {self.num}",color=YELLOW)
        tx9.next_to(p3,DOWN)
        
        tx10 = Tex("So,") 
        tx11 = MathTex(f"l = {self.log}",color=YELLOW)
        tx11.next_to(tx10,RIGHT)
        p4 = VGroup(tx10,tx11)
        p4.next_to(tx9,DOWN)
        
        g2 = VGroup(p3,tx9,p4)
        g2.center() # Center the group on the screen
        
        self.play(Write(p3), Write(tx9),run_time=0.5)
        self.play(Write(p4))
        self.wait()
        
        self.play(*[FadeOut(elem) for elem in g2])

    def generic_equation(self):
        self.eq1 = MathTex(r"k = \sum_{i=0}^{l} 2^i \cdot")
        self.eq2 = MathTex(r"(k \& (1 << i) \neq 0)")
        
        self.eq = VGroup(self.eq1,self.eq2)
        self.eq.arrange(RIGHT, buff=0.1) 
        
        self.play(Write(self.eq))
        self.wait(2)
        
        eq2c = MathTex(r"(k \& (1 << i) \neq 0)").next_to(self.eq1, RIGHT)
        tx1 = MathTex("1").next_to(self.eq1, RIGHT)
        tx0 = MathTex("0").next_to(self.eq1, RIGHT)
        
        self.play(Transform(self.eq2,tx1),run_time=0.5)
        self.wait(0.5)
        
        self.play(Transform(self.eq2,tx0),run_time=0.5)
        self.wait(0.5)
        
        self.play(Transform(self.eq2,eq2c),run_time=0.5)
        self.wait(0.5)
        
        self.play(
            self.eq.animate.move_to(ORIGIN+2.1*UP)
        )
    
    def clean(self):
        self.play(
            *[FadeOut(mob)for mob in self.mobjects]
        )
    
    def get_binary(self,x):
        ans = ""
        binary_str = bin(x)[2:] 
        binary_digits = [0 for i in range(self.bits)]
        for i in range(len(binary_str)):
            binary_digits[len(binary_digits)-1-i] = int(binary_str[len(binary_str) - 1 - i])
        i = 0
        n = len(binary_digits)
        while(i < n):
            if i > 3 and i%4 == 0:
                ans += " "
            ans += str(binary_digits[i])
            i+=1
        return ans
    
    def explain_bitwise_operation(self):
        txk = MathTex(f"k = {self.num}")
        txk.next_to(self.eq,DOWN)
        
        self.play(Write(txk))
        self.wait()
        
        g1 = VGroup()
        ref = txk
        for i in range(self.log+1):
            if(i!=0): ref = g1[i-1]
            tx = MathTex(f"1 << {i} = 2^{i} = {2**i}").next_to(ref,DOWN)
            self.play(Write(tx))
            g1.add(tx)
        
        self.wait()
        self.play(*[FadeOut(elem) for elem in g1])
        
        size_font = 35
        
        g2 = VGroup()
        ref = txk.get_center()
        binary_k = self.get_binary(self.num)
        for i in range(self.log+1):
            binary_shift = self.get_binary(1 << i)
            res = self.num & (1 << i)
            
            tx1 = MathTex(f"k \& 1<<{i} = {self.num} \& {(1 << i)} = {binary_k} \& {binary_shift} = {res}",font_size=size_font)
            tx2 = MathTex(r" \neq 0 >>",font_size=size_font).next_to(tx1,RIGHT)

            ans = "true" if res != 0 else "false"
            if ans == "true": tx3 = MathTex(ans, color=GREEN,font_size=size_font).next_to(tx2,RIGHT)
            else: tx3 = MathTex(ans, color=RED,font_size=size_font).next_to(tx2,RIGHT)
            
            g3 = VGroup(tx1,tx2,tx3)
            g3.center()
            g3.move_to(ref + DOWN*0.7*(i+1))
            
            self.play(Write(g3))
            g2.add(g3)
            
        self.wait()
        self.play(*[FadeOut(elem) for elem in g2])
        
    def generalization(self):
        # Perform bitwise operation
        self.title = Tex("Extracting bits using bitwise operations:")
        self.title.to_edge(UP)
        self.play(Write(self.title))
        self.wait()
    
    def construct(self):
        self.generalization()
        self.calculate_size_of_l()
        self.generic_equation()
        self.explain_bitwise_operation()
        self.clean()
        
        
        
        
        

        
