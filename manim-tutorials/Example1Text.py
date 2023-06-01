from manimlib import *

class Example1Text(Scene):
    def construct(self):
        text = Tex(r'Hello\ world').scale(3)
        self.add(text)