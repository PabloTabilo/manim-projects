from manim import *

class CodeTrackingAnimation(Scene):
    def construct(self):
        code_str = '''
        #include<iostream>
        using namespace std;
        int main(){
            int sum = 0;
            for(int i=0;i<n;i++){
                sum += i;
            }
            return 0;
        }'''
        code = self.build_code_block(code_str)
        for i in range(len(code.code)-1):
            self.highlight(i, i+1)
    
    def build_code_block(self, code_str):
        def remove_invisible_chars(lines):
            filtered_lines = []
            for line in lines:
                visible_chars = []
                for char in line:
                    if not isinstance(char, Dot):
                        visible_chars.append(char)
                filtered_lines.append(visible_chars)
            return filtered_lines

        # build the code block
        code = Code(code=code_str, language='C++', background="window",
                    line_spacing=1)
        print(code.code)
        code.code = remove_invisible_chars(code.code)
        print(code.code)
        self.add(code)
        # build sliding windows (SurroundingRectangle)
        self.sliding_wins = VGroup()
        max_width = max([line[0].get_width() for line in code.code])
        for line in code.code:
            line_height = line[0].get_height()
            self.sliding_wins.add(
                SurroundingRectangle(line)
                .set_fill(YELLOW)
                .set_opacity(0)
                .stretch_to_fit_width(max_width)
                .stretch_to_fit_height(line_height)
                .align_to(code.background_mobject, LEFT)
            )

        self.add(self.sliding_wins)
        return code

    def highlight(self, prev_line, line):
        self.play(self.sliding_wins[prev_line].animate.set_opacity(0.3))
        self.play(ReplacementTransform(self.sliding_wins[prev_line], self.sliding_wins[line]))
        self.play(self.sliding_wins[line].animate.set_opacity(0.3))

# Run the scene
scene = CodeTrackingAnimation()
scene.render()
