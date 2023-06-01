# https://leetcode.com/problems/course-schedule/editorial/
from manim import *

class Node(VGroup):
    def __init__(self, value, radius=0.25, color=BLUE):
        super().__init__()
        self.radius = radius
        self.circle = Circle(radius=radius, color=color)
        self.text = Text(str(value), font_size=25)
        self.add(self.circle, self.text)

    def set_position(self, position):
        self.move_to(position)
    
    def set_color(self, color):
        self.remove(self.circle)  # Remove the current circle
        self.circle = Circle(radius=self.radius, color=color)
        self.add(self.circle)  # Add the new circle to the scene
        self.circle.move_to(self.text.get_center())

class GraphScene(Scene):
    def construct(self):
        # Define the nodes and their positions
        # (x, y, z)
        nodes = {
            0: (0,  3, 0),
            1: (-1, 2, 0),
            2: (-1, 0, 0),
            3: (1, -1, 0),
            4: (1, 1, 0),
        }

        # Create the nodes as circles and position them
        circle_group = VGroup()
        for val, pos in nodes.items():
            node = Node(val)
            node.set_position(pos)
            circle_group.add(node)
        self.play(Create(circle_group), run_time=1)

        # Define the edges between the nodes
        # from -> to
        edges = [
            (0, 1), 
            (0, 2), 
            (0, 4), 
            (1, 2),
            (2, 4), 
            (2, 3), 
            (3, 4),
            ]
        
        # Calculate the max length among all edges
        max_length = max([np.linalg.norm(np.array(nodes[edge[0]]) - np.array(nodes[edge[1]])) for edge in edges])

        # Connect the nodes with edges
        edges_group = VGroup()
        for edge in edges:
            start_pos = nodes[edge[0]]
            end_pos = nodes[edge[1]]
            arr = Arrow(
                start_pos, 
                end_pos,
                stroke_width=3,
                buff=0.2,
                max_tip_length_to_length_ratio=0.025 * max_length,
                max_stroke_width_to_length_ratio=3 * max_length,
                )
            edges_group.add(arr)
        self.play(Create(edges_group), run_time=1)

        self.wait()
        
        # Kahn algorithm

# Create the graph scene
graph_scene = GraphScene()

# Render the graph scene
graph_scene.render()
