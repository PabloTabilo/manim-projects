from manim import *

class RecursionVisualization(VGroup):
    def __init__(self, n, level=0, **kwargs):
        super().__init__(**kwargs)
        self.n = n
        self.level = level

        self.text = Text(f"Level {self.level}: {self.n}").shift(DOWN * self.level)
        self.add(self.text)

        if self.n > 0:
            self.add(*self.create_submobjects())

    def create_submobjects(self):
        submobjects = []

        submobjects.extend(self.create_submobjects_recursive(self.n - 1, self.level + 1))
        
        text = self.text.copy()
        text.set_color(RED)
        submobjects.append(text)
        
        submobjects.extend(self.create_submobjects_recursive(self.n - 1, self.level + 1))
        
        return submobjects

    def create_submobjects_recursive(self, n, level):
        if n == 0:
            return []
        
        text = Text(f"Level {level}: {n}").shift(DOWN * level)
        return [text] + self.create_submobjects_recursive(n - 1, level + 1)

class RecursionDemo(Scene):
    def construct(self):
        title = Title("Recursion Visualization")
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        recursion_visualization = RecursionVisualization(5)
        self.play(Create(recursion_visualization))
        self.wait(5)

        self.play(FadeOut(recursion_visualization))
        self.wait(1)

        outro = Text("That's recursion!")
        self.play(Write(outro))
        self.wait(2)
        self.play(FadeOut(outro))
        self.wait(1)

if __name__ == "__main__":
    config = {
        "pixel_height": 720,
        "pixel_width": 1280,
        "background_color": WHITE,
        "frame_rate": 30,
    }
    scene = RecursionDemo()
    scene.render(config=config)
