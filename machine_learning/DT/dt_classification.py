import random
from manim import *

class Points(VGroup):
    def __init__(self, point_possition, color, classification) -> None:
        super().__init__()
        self.px = point_possition
        self.color = color
        self.classification = classification
        
        self.mydot = Dot(
            point=point_possition,
            color=color
            )
        self.add(self.mydot)

class Node(VGroup):
    def __init__(self, value, color=BLUE):
        super().__init__()
        self.radius = 0.42
        self.font_size = 18
        self.circle = Circle(radius=self.radius, color=color)
        self.text = MathTex(value, font_size=self.font_size)
        self.add(self.circle, self.text)
    
    def set_position(self, position):
        self.move_to(position)
    
    def set_text(self, value):
        self.remove(self.text)
        self.text = MathTex(value, font_size=self.font_size)
        self.add(self.text)
        self.text.move_to(self.circle.get_center())
    
    def set_color(self, color):
        self.remove(self.circle)  # Remove the current circle
        self.circle = Circle(radius=self.radius, color=color)
        self.add(self.circle)  # Add the new circle to the scene
        self.circle.move_to(self.text.get_center())

class Graph(Scene):
    def construct(self):
        # Define the number of points
        num_points = 10

        # Generate random positions for the points
        point_positions = [
            [0.3,0.3,0],
            [-0.4, 0.3,0],
            [-0.3,-0.2,0],
            [-0.5,-0.8,0],
            [0.1,-1.1,0],
            
            [0.2,0.8,0],
            [-1.1,-0.5,0],
            [0.8,-0.3,0],
            [0.9,1.1,0],
            [0.7,0.9,0],
        ]
        
        classification = [
            1,1,1,1,1,
            0,0,0,0,0,
        ]

        # Create the plane
        plane = NumberPlane(
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1,
                "stroke_opacity": 0.3
                },
            faded_line_ratio = 3
            )

        # Create the points
        points = VGroup(*[Points(point_positions[i], 
                                 RED if classification[i]==1 else BLUE, 
                                 classification[i]) for i in range(num_points)])
        
        GAP_X = -5
        position_of_nodes = {
            1: [0,3.5],
            2: [-1,2.5],
            3: [1,2.5],
            4: [2,1.5],
            5: [0,1.5],
            6: [-1,0.5],
            7: [1,0.5],
        }
        
        position_of_nodes = {k : [position_of_nodes[k][0]+GAP_X,position_of_nodes[k][1]] for k in position_of_nodes}
        nodes_objects = {}
        
        # Create the separating line
        # X <= -0.8 Blue
        separating_line = Line(
            plane.coords_to_point(-0.8, plane.y_range[0]),
            plane.coords_to_point(-0.8, plane.y_range[1]),
            color=BLUE,
            stroke_width=3,
            stroke_opacity=0.7,
        )
        node_1 = Node(value=r"X \leq -0.8",color=YELLOW)
        node_1.set_position(plane.coords_to_point(position_of_nodes[1][0],position_of_nodes[1][1]))
        nodes_objects[1] = node_1
        
        # Color the left side of the plane blue with opacity
        plane_left = Polygon( 
            plane.coords_to_point(plane.x_range[0], plane.y_range[0]), # -7.1 , -4.0
            plane.coords_to_point(-0.8, plane.y_range[0]), # -0.8, -4.0
            plane.coords_to_point(-0.8, plane.y_range[1]), # -0.8, 4.0
            plane.coords_to_point(plane.x_range[0], plane.y_range[1]), # -7.1, 4.0
            fill_color=BLUE,
            fill_opacity=0.1,
            stroke_width=0,
        )
        node_2 = Node(r"\{1, 0\}",color=BLUE)
        node_2.set_position(plane.coords_to_point(position_of_nodes[2][0],position_of_nodes[2][1]))
        nodes_objects[2] = node_2
        
        # Color the right side of the plane red with opacity
        plane_right = Polygon(
            plane.coords_to_point(-0.8, plane.y_range[0]), # -0.8, -4.0
            plane.coords_to_point(plane.x_range[1], plane.y_range[0]), # 7.1, -4.0
            plane.coords_to_point(plane.x_range[1], plane.y_range[1]), # 7.1, 4.0
            plane.coords_to_point(-0.8, plane.y_range[1]), # -0.8, 4.0
            fill_color=RED,
            fill_opacity=0.1,
            stroke_width=0,
        )
        node_3 = Node(r"\{4, 5\}",color=RED)
        node_3.set_position(plane.coords_to_point(position_of_nodes[3][0],position_of_nodes[3][1]))
        nodes_objects[3] = node_3
        
        # Y <= 0.3 RED
        separating_line_rule2 = Line(
            plane.coords_to_point(-0.8, 0.3),
            plane.coords_to_point(plane.x_range[1], 0.3),
            color=RED,
            stroke_width=3,
            stroke_opacity=0.7,
        )
        
        plane_up = Polygon(
            # -0.8,4.0
            # -0.8,0.3
            # 7.1, 0.3
            # 7.1, 4.0
            plane.coords_to_point(-0.8, plane.y_range[1]),
            plane.coords_to_point(-0.8, 0.3),
            plane.coords_to_point(plane.x_range[1], 0.3),
            plane.coords_to_point(plane.x_range[1], plane.y_range[1]),
            fill_color=BLUE,
            fill_opacity=0.3,
            stroke_width=0,
        )
        node_4 = Node(r"\{3, 0\}",color=BLUE)
        node_4.set_position(plane.coords_to_point(position_of_nodes[4][0],position_of_nodes[4][1]))
        nodes_objects[4] = node_4
        
        plane_down = Polygon(
            # -0.8,-4.0
            # -0.8,0.3
            # 7.1, 0.3
            # 7.1, -4.0
            plane.coords_to_point(-0.8, plane.y_range[0]),
            plane.coords_to_point(-0.8, 0.3),
            plane.coords_to_point(plane.x_range[1], 0.3),
            plane.coords_to_point(plane.x_range[1], plane.y_range[0]),
            fill_color=RED,
            fill_opacity=0.1,
            stroke_width=0,
        )
        node_5 = Node(r"\{1, 5\}",color=RED)
        node_5.set_position(plane.coords_to_point(position_of_nodes[5][0],position_of_nodes[5][1]))
        nodes_objects[5] = node_5
        
        # X <= 0.4 RED
        separating_line_rule3 = Line(
            plane.coords_to_point(0.4, 0.3),
            plane.coords_to_point(0.4, plane.y_range[0]),
            color=RED,
            stroke_width=3,
            stroke_opacity=0.7,
        )
        
        plane_left_rule3 = Polygon(
            # -0.8,0.3
            # 0.4,0.3
            # -0.8, -4.0
            # 0.4, -4.0
            plane.coords_to_point(-0.8, 0.3),
            plane.coords_to_point(-0.8, plane.y_range[0]),
            plane.coords_to_point(0.4, plane.y_range[0]),
            plane.coords_to_point(0.4, 0.3),
            fill_color=RED,
            fill_opacity=0.1,
            stroke_width=0,
        )
        node_6 = Node(r"\{0, 5\}",color=RED)
        node_6.set_position(plane.coords_to_point(position_of_nodes[6][0],position_of_nodes[6][1]))
        nodes_objects[6] = node_6
        
        plane_right_rule3 = Polygon(
            # 0.4 -> max
            # 0.3 -> min
            
            # 7.1, -4.0
            # 0.4, 0.3
            # 7.1, 0.3
            # 0.4, -4.0
            plane.coords_to_point(0.4, 0.3),
            plane.coords_to_point(0.4, plane.y_range[0]),
            plane.coords_to_point(plane.x_range[1], plane.y_range[0]),
            plane.coords_to_point(plane.x_range[1], 0.3),
            fill_color=BLUE,
            fill_opacity=0.3,
            stroke_width=0,
        )
        node_7 = Node(r"\{1, 0\}",color=BLUE)
        node_7.set_position(plane.coords_to_point(position_of_nodes[7][0],position_of_nodes[7][1]))
        nodes_objects[7] = node_7
        
        # add Edges
        edges = [
            (1,2),
            (1,3),
            (3,4),
            (3,5),
            (5,6),
            (5,7)
        ]
        edges_object = {k:[] for k in nodes_objects}
        for edge in edges:
            start_node = nodes_objects[edge[0]]
            end_node = nodes_objects[edge[1]]
            edge_line = Line(
                start=start_node.get_center() + DOWN*0.42,
                end=end_node.get_center() + RIGHT*0.42 if end_node.get_center()[0]<start_node.get_center()[0] else end_node.get_center() + LEFT*0.42,
                stroke_color=WHITE,
                stroke_width=2,
            )
            edges_object[edge[0]].append(edge_line)
        
        # Add elements to the scene
        self.add(plane, points)
        self.play(Create(points))
        self.wait(1)
        
        # Rule 1
        self.add(separating_line)
        self.play(Create(separating_line))
        self.play(FadeIn(nodes_objects[1]))
        
        self.add(nodes_objects[2],plane_left)
        self.play(FadeIn(nodes_objects[2]),FadeIn(plane_left))
        
        self.add(nodes_objects[3],plane_right)
        self.play(FadeIn(nodes_objects[3]),FadeIn(plane_right))

        self.add(edges_object[1][0],edges_object[1][1])
        self.play(Create(edges_object[1][0]),Create(edges_object[1][1]))
        self.wait(1)
        
        # Rule 2
        self.add(separating_line_rule2)
        nodes_objects[3].set_text(r"Y \leq 0.3")
        nodes_objects[3].set_color(YELLOW)
        self.play(Create(separating_line_rule2),Create(nodes_objects[3]))
        
        self.add(nodes_objects[4],plane_up)
        self.play(FadeIn(nodes_objects[4]),FadeIn(plane_up))
        self.add(nodes_objects[5],plane_down)
        self.play(FadeIn(nodes_objects[5]),FadeIn(plane_down))
        
        self.add(edges_object[3][0],edges_object[3][1])
        self.play(Create(edges_object[3][0]),Create(edges_object[3][1]))
        
        self.wait(1)
        
        # Rule 3
        self.add(separating_line_rule3)
        nodes_objects[5].set_text(r"X \leq 0.3")
        nodes_objects[5].set_color(YELLOW)
        self.play(Create(separating_line_rule3),Create(nodes_objects[5]))
        
        self.add(nodes_objects[6],plane_left_rule3)
        self.play(FadeIn(nodes_objects[6]),FadeIn(plane_left_rule3))
        
        self.add(nodes_objects[7],plane_right_rule3)
        self.play(FadeIn(nodes_objects[7]),FadeIn(plane_right_rule3))
        
        self.add(edges_object[5][0],edges_object[5][1])
        self.play(Create(edges_object[5][0]),Create(edges_object[5][1]))
        
        self.wait(1)
    
