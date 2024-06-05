from manim import *
import numpy as np

class Node(VGroup):
    def __init__(self, radius : float, color : str, value : int, position : list, *vmobjects, **kwargs):
        super().__init__(*vmobjects, **kwargs)
        self.radius = radius
        self.color = color
        self.value = value
        self.position = position
        
        self.circle = Circle(radius=self.radius,color=self.color)
        self.text = Text("f("+str(self.value)+")", font_size=25)
        
        self.add(self.circle, self.text)
        self.move_to(self.position)  # Maintain relative position
    
    def set_position(self, position):
        self.position = position
        self.move_to(self.position)
    
    def set_color(self, color):
        self.color = color
        self.circle.set_stroke(color, width=3)
        

class FibonacciTreeScene(Scene):
    def __init__(self):
        super().__init__()
        self.start_position = (-3.5,3.5,0)
        self.position = {}
        self.connections = []
        self.radius = 0.4
        self.positions = {}
        self.x_offset = 1.1
        self.y_offset = 1.0
        self.node_counter = {}
        
    def build_tree(self, n, position, depth):
        if(depth not in self.node_counter):
            self.node_counter[depth] = 0
        adjusted_position = (
            position[0] + self.node_counter[depth] * self.x_offset,
            position[1] - depth * self.y_offset * (.5 if depth > 1 else 1),
            0
        )
        self.node_counter[depth] += 1
        
        node = Node(radius=self.radius, color=BLUE, value=n, position=adjusted_position)
        self.play(FadeIn(node))

        if depth > 0:
            parent_position = self.positions[depth - 1]
            direction_vector = np.array(adjusted_position) - np.array(parent_position)
            direction_vector /= np.linalg.norm(direction_vector)
            start_point = np.array(parent_position) + direction_vector * self.radius
            end_point = np.array(adjusted_position) - direction_vector * self.radius
            edge = Line(start=start_point, end=end_point)
            self.play(Create(edge))
            self.wait(0.5)

        if n > 1:
            self.positions[depth] = adjusted_position
            self.build_tree(n - 1, adjusted_position, depth+1)
            self.build_tree(n - 2, adjusted_position, depth+1)
    
    def construct(self):
        self.build_tree(5, self.start_position, 0)
        self.wait()