# https://leetcode.com/problems/course-schedule/editorial/
from manim import *
import queue

class Node(VGroup):
    def __init__(self, value, radius=0.22, color=BLUE):
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

class VectorData(VGroup):
    def __init__(self, box_width, box_pos, val, i, color):
        super().__init__()
        self.box_width = box_width
        self.box_pos = box_pos
        self.val = val
        self.i = i
        self.color = color
        
        self.current_pos = RIGHT * self.i * (self.box_width + 0.1)
        
        self.indegree_box = Rectangle(width=box_width, height=box_width, fill_opacity=0.1, color=color).move_to(box_pos + self.current_pos)
        self.indegree_val = Tex(str(val), font_size=18).move_to(box_pos +  self.current_pos )
        
        self.add(self.indegree_box, self.indegree_val)
    
    def get_info_pos(self):
        return self.box_pos, self.i, self.box_width
    
    def get_pos(self):
        return self.box_pos + self.current_pos
    
    def reset_position(self, i):
        self.remove(self.indegree_box, self.indegree_val)
        self.i = i
        self.current_pos = RIGHT * i * (self.box_width + 0.1)
        self.indegree_box = Rectangle(width=self.box_width, height=self.box_width, fill_opacity=0.1, color=self.color).move_to(self.box_pos + self.current_pos)
        self.indegree_val = Tex(str(self.val), font_size=18).move_to(self.box_pos + self.current_pos)
        self.add(self.indegree_box, self.indegree_val)
    
    def set_color(self, color):
        self.remove(self.indegree_box)
        self.indegree_box = Rectangle(width=self.box_width, height=self.box_width, fill_opacity=0.1, color=color).move_to(self.box_pos + self.current_pos)
        self.color = color
        self.add(self.indegree_box)
    
    def set_val(self, val):
        self.remove(self.indegree_val)
        self.indegree_val = Tex(str(val), font_size=18).move_to(self.box_pos +  self.current_pos)
        self.val = val
        self.add(self.indegree_val)
            

class GraphScene(Scene):
    def construct(self):
        # Define the nodes and their positions
        # (x, y, z)
        nodes = {
            0: (-1,  3, 0),
            2: (-1, -1, 0),
            3: (-1, 1, 0),
            4: (1, 0, 0),
            1: (1, 2, 0),
        }
        
        # Define the edges between the nodes
        # from -> to
        edges = {
            0 : [1, 3],
            1 : [3, 4],
            2 : [3],
            3 : [4],
            4 : [],
        }

        # Create the nodes as circles and position them
        nodes_group = VGroup()
        nodes_objects = {}  # Store the Node objects for each node
        for val, pos in nodes.items():
            node = Node(val)
            node.set_position(pos)
            nodes_group.add(node)
            nodes_objects[val] = node
        self.play(Create(nodes_group), run_time=1)

        # Calculate the max length among all edges
        max_length = -1
        first_time = True
        for k in edges:
            for v in edges[k]:
                if(first_time):
                    max_length = np.linalg.norm(np.array(nodes[k]) - np.array(nodes[v]))
                    first_time = False
                else:
                    max_length = max(max_length, np.linalg.norm(np.array(nodes[k]) - np.array(nodes[v])) )

        indegree = [0 for i in range(len(nodes))]
        # Connect the nodes with edges
        edges_group = VGroup()
        edges_objects = {i : {} for i in range(len(nodes))}
        for k in edges:
            for v in edges[k]:
                start_pos = nodes[k]
                end_pos = nodes[v]
                indegree[v]+=1
                arr = Arrow(
                    start_pos, 
                    end_pos,
                    stroke_width=3,
                    buff=0.2,
                    max_tip_length_to_length_ratio=0.05 * max_length,
                    max_stroke_width_to_length_ratio=3 * max_length,
                    )
                edges_objects[k][v] = arr
                edges_group.add(arr)
        self.play(Create(edges_group), run_time=1)

        self.wait()
        
        # Create box to display indegree values
        box_pos = np.array([-1, -1.8, 0])
        box_width = 0.4
        
        indegree_text = Text("Indegree:", font_size=15).move_to(box_pos + LEFT * box_width * 1.7)
        indegree_values = VGroup()
        indegree_indexs = VGroup()
        indegree_objects = {}
        for i, val in enumerate(indegree):
            vector_data = VectorData(box_width, box_pos, val, i, BLUE)
            indegree_index = Tex(f"{i}", font_size=14).move_to(vector_data.get_pos() + DOWN * box_width)
            indegree_values.add(vector_data)
            indegree_indexs.add(indegree_index)
            indegree_objects[i] = vector_data
        self.play(Write(indegree_text), Create(indegree_values), FadeIn(indegree_indexs), run_time=1)
        self.wait()
        
        # Kahn algorithm
        q = queue.Queue()
        queue_list = []
        queue_pos = DOWN * box_width * 1.9
        queue_text = Text("Queue:", font_size=15).move_to(box_pos + LEFT * box_width * 1.6 + queue_pos)
        queue_values = VGroup()
        queue_objects = {}
        for i in range(len(indegree)):
            if(indegree[i] == 0):
                q.put(i)
                queue_list.append(i)
                vector_data = VectorData(box_width, box_pos + queue_pos, val = i, i = q.qsize()-1, color = YELLOW)
                queue_values.add(vector_data)
                queue_objects[i] = vector_data
        self.play(Write(queue_text), Create(queue_values), run_time=1)
        self.wait()
        
        num_nodes = len(nodes)
        num_nodes_kahn = 0
        pointer_indegree = Rectangle(width=box_width, height=box_width, fill_opacity=0.2, color = GRAY)
        pointer_select = Rectangle(width=box_width, height=box_width, fill_opacity=0.2, color = RED)
        
        
        topological_sort = []
        topo_text = None
        topo_val = None
        topo_pos = DOWN * box_width * 3.3
        prev_pos = 0
        while not q.empty():
            n = q.get()
            num_nodes_kahn += 1
            nodes_objects[n].set_color(RED_D)
            queue_objects[n].set_color(RED_D)
            pointer_select.move_to(indegree_objects[n].get_pos())
            self.play(FadeIn(nodes_objects[n].circle), FadeIn(queue_objects[n].indegree_box), Create(pointer_select), run_time=1)
            self.wait()
            topological_sort.append(n)
            
            for nn in edges[n]:
                pointer_indegree.move_to(indegree_objects[nn].get_pos())
                self.play(Create(pointer_indegree), run_time=1)
                indegree[nn]-=1
                indegree_objects[nn].set_val(indegree[nn])
                edges_objects[n][nn].set_color(GRAY)
                self.play(FadeIn(edges_objects[n][nn]), FadeIn(indegree_objects[nn]), run_time=1)
                if(indegree[nn]==0):
                    q.put(nn)
                    vector_data = VectorData(box_width, box_pos + queue_pos, val = nn, i = q.qsize(), color = YELLOW)
                    queue_values.add(vector_data)
                    queue_objects[nn] = vector_data
                    queue_list.append(nn)
                    self.play(Create(vector_data))
            nodes_objects[n].set_color(DARK_BLUE)
            indegree_objects[n].set_color(DARK_BLUE)
            self.play(FadeOut(pointer_indegree), FadeOut(pointer_select), run_time=0.5)
            self.play(Create(nodes_objects[n]), FadeIn(indegree_objects[n]), run_time=0.5)
            
            if(len(topological_sort)<=1):
                topo_text = Text("Topological\nSorting:", font_size=12).move_to(box_pos + LEFT * box_width * 2 + topo_pos)
                self.play(Write(topo_text),runtime=0.5)
            vector_data = VectorData(box_width, box_pos + topo_pos, val = n, i = len(topological_sort)-1, color = GREEN)
            self.play(FadeIn(vector_data),runtime=0.5)
            
            # clean queue
            queue_pos_last, i, box_width = queue_objects[n].get_info_pos()
            queue_list.pop(0)
            self.play(FadeOut(queue_objects[n]))
            self.remove(queue_objects[n])
            for i,nn in enumerate(queue_list):
                #new_position = queue_pos_last + (RIGHT * i * (box_width + 0.1))
                self.play(queue_objects[nn].animate.shift(LEFT * 1 * (box_width + 0.1)))
                queue_objects[nn].reset_position(i)
                self.add(queue_objects[nn])
                
        self.wait(5)
        
# Create the graph scene
graph_scene = GraphScene()

# Render the graph scene
graph_scene.render()
