from manim import *

class StructNodeCode(VGroup):
    def __init__(self, scene):
        super().__init__()
        code_str = '''
        struct Node{
            Node* links[26];
            bool flag=false;
        };
        '''
        self.code = self.build_code_block(code_str, scene)
    
    def build_code_block(self, code_str, scene):
        # build the code block
        code = Code(code=code_str, language='C++', background="window",line_spacing=1)
        print(code.code)
        code.code = self.remove_invisible_chars(code.code)
        self.add(code)
        # build sliding windows (SurroundingRectangle)
        self.sliding_wins = VGroup()
        print(code.code)
        height = code.code[0].height
        #for line in code.code:
        #    self.sliding_wins.add(
        #        SurroundingRectangle(line)
        #        .set_fill(YELLOW)
        #        .set_opacity(0)
       #        .stretch_to_fit_width(code.background_mobject.get_width())
        #        .align_to(code.background_mobject, LEFT)
        #    )

        #self.add(self.sliding_wins)
        return code
    
    def remove_invisible_chars(self, lines):
        filtered_lines = []
        for line in lines:
            visible_chars = []
            for char in line:
                if not isinstance(char,Dot):
                    visible_chars.append(char)
            filtered_lines.append(visible_chars)
        return filtered_lines
    
    def highlight_scene(self, scene):
        for i in range(len(self.code.code)-1):
            self.highlight(i, i+1, scene)
            
    def highlight(self, prev_line, line, scene):
        scene.play(self.sliding_wins[prev_line].animate.set_opacity(0.3))
        scene.play(ReplacementTransform(self.sliding_wins[prev_line], self.sliding_wins[line]))
        scene.play(self.sliding_wins[line].animate.set_opacity(0.3))

class Trie(Scene):
    def construct(self):
        struct_code = StructNodeCode(self)
        self.play(Write(struct_code[0]), run_time=1)
        
        #struct_code.highlight_scene(self)
        self.wait(1)
    
