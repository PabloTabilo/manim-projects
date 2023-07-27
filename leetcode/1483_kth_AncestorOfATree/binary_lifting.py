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
        self.text = Text(str(self.value), font_size=25)
        
        self.add(self.circle, self.text)
        self.move_to(self.position)  # Maintain relative position
    
    def set_position(self, position):
        self.position = position
        self.move_to(self.position)

class Tree(VGroup):
    def __init__(self, n : int, *vmobjects, **kwargs):
        super().__init__(*vmobjects, **kwargs)
        self.n = n
        
    def connection(self, node_start : Node, node_end : Node):
        pass

class BinaryLiftingTable(VGroup):
    def __init__(self, *vmobjects, **kwargs):
        super().__init__(*vmobjects, **kwargs)

class BinaryLiftingScene(Scene):
    def construct(self):
        # Tree and connections
        start_position = (3.5, 3, 0)
        n = 11 # number of nodes
        positions = {
            0:start_position,
            
            1:(2.5, 2, 0),
            2:(3.5, 2, 0),
            5:(4.5, 2, 0),
            
            3:(1.0, 1, 0),
            6:(1.75, 1, 0),
            9:(2.5, 1, 0),
            4:(3.5, 1, 0),
            
            7:(1.0, 0, 0),
            8:(1.75, 0, 0),
            10:(1.75, -1, 0),
        }
        nodes = {}
        nodes_obj = VGroup()
        for i in range(n):
            node = Node(
                radius=0.22,
                color=BLUE_A,
                value=i,
                position=positions[i])
            nodes[i] = node
            nodes_obj.add(node)
        
        tree = VGroup()
        connections = [
            (0, 1), 
            (0, 2), 
            (1, 3), 
            (2, 4), 
            (0, 5), 
            (1, 6), 
            (3, 7), 
            (6, 8), 
            (1, 9),
            (8,10),
            ]

        edges_objects = {i : {} for i in range(len(connections))}
        
        for i, j in connections:
            p1 = nodes[i].get_center()
            p2 = nodes[j].get_center()
            m = float(p2[0]-p1[0]) / float(p2[1]-p1[1])
            x1,y1 = p1[0],p1[1]
            x2,y2 = p2[0],p2[1]
            r = nodes[i].radius * 0.2
            # x1 izq x2
            if(x1 < x2):
                x1+=r
                y1 = (x1 - p1[0])*m + p1[1]
                x2-=r
                y2 = (x2 - p2[0])*m + p2[1]
            elif(x1 > x2):
                x1-=r
                y1 = (x1 - p1[0])*m + p1[1]
                x2+=r
                y2 = (x2 - p2[0])*m + p2[1]
            else:
                if(y1 > y2):
                    y1-=r
                    y2 += r
                else:
                    y1+=r
                    y2 -= r
            print("x1,y1 =",x1,y1)
            print("x2,y2 =",x2,y2)
            arr = Line(
                start=(x1,y1,0), 
                end=(x2,y2,0), 
                buff=0.2,
                stroke_width=3,
                )
            tree.add(arr)
            edges_objects[i][j] = arr

        self.play(Create(nodes_obj),Create(tree))
        self.wait()

        # Binary Lifting table
        col_labels = [Text(f"{i}") for i in range(4)]
        row_labels = [Text(f"{i}") for i in range(10)]

        table_data = [
            ["-1", "-1", "-1", "-1"], # 0 
            ["0", "-1", "-1", "-1"], # 1
            ["0", "-1", "-1", "-1"], # 2
            ["1", "0", "-1", "-1"], # 3 
            ["2", "0", "-1", "-1"], # 4
            ["0", "-1", "-1", "-1"], # 5
            ["1", "0", "-1", "-1"], # 6
            ["3", "1", "-1", "-1"], # 7
            ["6", "1", "-1", "-1"], # 8
            ["1", "0", "-1", "-1"], # 9
        ]

        table = Table(
            table_data, 
            row_labels=row_labels, 
            col_labels=col_labels,
            include_outer_lines=True,
            arrange_in_grid_config={"cell_alignment": RIGHT}
            )
        table.scale(0.4)
        table.move_to(3 * LEFT)

        self.play(Create(table))
        self.wait()
        
