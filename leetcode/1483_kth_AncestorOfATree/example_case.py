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

class ExampleCase(Scene):
    def __init__(self):
        super().__init__()
        self.num = 19
        # Convert the number to binary representation
        self.binary_str = bin(self.num)[2:]  # [2:] is used to remove the '0b' prefix
        self.binary_digits = [int(digit) for digit in self.binary_str]
        
        self.binary_objects = VGroup()
        self.binary_powers = VGroup()
        self.binary_power_values = VGroup()
    
    def display_binary_representation(self):
        binary_text = Text("Binary representation:")
        binary_text.to_edge(UP)
        self.play(Write(binary_text))
        
        for i, digit in enumerate(self.binary_digits):
            binary_digit = Tex(str(digit))
            binary_digit.next_to(binary_text, DOWN)
            binary_digit.shift(RIGHT * i * 0.5)
            self.binary_objects.add(binary_digit)

        number_text = Text(f"{self.num} = ")
        number_text.next_to(self.binary_objects, LEFT)
        self.play(Write(number_text),Write(self.binary_objects))
    
    def display_powers_of_2(self):
        for i in range(len(self.binary_objects)):
            power = len(self.binary_objects) - 1 - i
            binary_power = MathTex(f"2^{power}")
            power_value = MathTex(str(2**power))
            binary_power.next_to(self.binary_objects[i], DOWN)
            power_value.next_to(binary_power, DOWN)
            self.binary_powers.add(binary_power)
            self.binary_power_values.add(power_value)

        self.play(Write(self.binary_powers), Write(self.binary_power_values))
        self.wait()
    
    def display_sum_of_power_of_2(self):
        values_for_add = []
        for i in range(len(self.binary_digits)):
            if self.binary_digits[i] == 1:
                self.play(
                    self.binary_objects[i].animate.set_color(YELLOW),
                    self.binary_powers[i].animate.set_color(YELLOW), 
                    self.binary_power_values[i].animate.set_color(YELLOW),
                    run_time=0.5
                    )
                self.wait()
                values_for_add.append(self.binary_power_values[i].get_tex_string())
        equation = f"{self.num} = "
        for i in range(len(values_for_add)): equation += values_for_add[i] + " + " if i != len(values_for_add)-1 else values_for_add[i]
        equation_text = MathTex(equation)
        self.play(Write(equation_text))
        
    def example_case(self):
        self.display_binary_representation()
        self.display_powers_of_2()
        self.display_sum_of_power_of_2()
        self.wait()
    
    def generalization(self):
        # Perform bitwise operation
        kth_text = Text("Extracting bits using bitwise operations:")
        kth_text.to_edge(UP)
        self.play(kth_text)
        self.wait()
    
    def code_kth(self):
        code = '''
        int getKthAncestor(int node = 10, int k = 4)'''
        rendered_code = Code(
            code=code, 
            tab_width=4, 
            background="window",
            language="C++",
            line_spacing=1,
            font="Monospace")
        self.play(Create(rendered_code))
        self.wait(1)
        self.play(FadeOut(rendered_code))
        
        code = '''
        int getKthAncestor(int node = 10, int k = 3)'''
        rendered_code = Code(
            code=code, 
            tab_width=4, 
            background="window",
            language="C++",
            line_spacing=1,
            font="Monospace")
        self.play(Create(rendered_code))
        self.wait(1)
        self.play(FadeOut(rendered_code))
    
    def calculate_log(self):
        code = '''
        self.log = 0
        while((1<<self.log)<n): self.log+=1'''
        rendered_code = Code(
            code=code, 
            tab_width=4, 
            background="window",
            language="Python",
            line_spacing=1,
            font="Monospace")
        self.play(Create(rendered_code))
        self.wait(1)
        self.play(FadeOut(rendered_code))
    
    def build_blt(self):
        code = '''
        self.blt = [[-1 for l in range(self.log)] for i in range(n)]'''
        rendered_code = Code(
            code=code, 
            tab_width=4, 
            background="window",
            language="Python",
            line_spacing=1,
            font="Monospace")
        self.play(Create(rendered_code))
        self.wait(1)
        self.play(FadeOut(rendered_code))
    
    def fill_blt(self):
        code = '''
        for l in range(self.log):
            for i in range(n):
                if(l > 0):
                    if(self.blt[i][l-1] != -1):
                        self.blt[i][l] = self.blt[ self.blt[i][l-1] ][l-1]
                else:
                    self.blt[i][l] = parent[i]'''
        rendered_code = Code(
            code=code, 
            tab_width=4, 
            background="window",
            language="Python",
            line_spacing=1,
            font_size=20,
            font="Monospace")
        self.play(Create(rendered_code))
        self.wait(1)
        self.play(FadeOut(rendered_code))
    
    def get_ancestor_code(self):
        code = '''
        def getKthAncestor(self, node: int, k: int) -> int:
            start = node
            for l in range(self.log):
                if(k & (1<<l))!=0:
                    start = self.blt[start][l]
                    if(start == -1): return -1
            return -1 if start == node else start'''
        rendered_code = Code(
            code=code, 
            tab_width=4, 
            background="window",
            language="Python",
            line_spacing=1,
            font="Monospace")
        self.play(Create(rendered_code))
        self.wait(1)
        self.play(FadeOut(rendered_code))
    
    def complete_code(self):
        code = '''
        class TreeAncestor:
            def __init__(self, n: int, parent: List[int]):
                self.log = 0
                while((1<<self.log)<n): self.log+=1

                self.blt = [[-1 for l in range(self.log)] for i in range(n)]

                for l in range(self.log):
                    for i in range(n):
                        if(l > 0):
                            if(self.blt[i][l-1] != -1):
                                self.blt[i][l] = self.blt[ self.blt[i][l-1] ][l-1]
                        else:
                            self.blt[i][l] = parent[i]

            def getKthAncestor(self, node: int, k: int) -> int:
                start = node
                for l in range(self.log):
                    if(k & (1<<l))!=0:
                        start = self.blt[start][l]
                        if(start == -1): return -1
                return -1 if start == node else start'''
        rendered_code = Code(
            code=code, 
            tab_width=4, 
            background="window",
            language="Python",
            line_spacing=1,
            font_size=15,
            font="Monospace")
        self.play(Create(rendered_code))
        self.wait(1)
        self.play(FadeOut(rendered_code))
    
    def clean(self):
        self.play(
            *[FadeOut(mob)for mob in self.mobjects]
        )
    
    def construct(self):
        self.example_case()
        self.wait()
        self.clean()
        self.calculate_log()
        self.build_blt()
        self.fill_blt()
        self.code_kth()
        self.get_ancestor_code()
        self.clean()
        self.complete_code()
        self.wait()
        
        
        
        

        
