from manim import *

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
    
    def set_color(self, color):
        self.color = color
        self.circle.set_stroke(color, width=3)

class MyCell(VGroup):
    def __init__(self, box_pos : tuple, val : int, color : str, box_width : float = 0.4, box_height : float = 0.4, *vmobjects, **kwargs):
        super().__init__(*vmobjects, **kwargs)
        self.box_width = box_width
        self.box_height = box_height
        self.box_pos = box_pos
        self.val = val
        self.color = color
        
        self.font_size = 22
        
        self.box = Rectangle(width=self.box_width, height=self.box_height, fill_opacity=0.1, color=self.color).move_to(self.box_pos)
        self.val_box = Tex(str(val), font_size=self.font_size).move_to(self.box_pos)
        
        self.add(self.box, self.val_box)
    
    def set_color(self, color):
        self.color = color
        self.box.set_stroke(color, width=3)
    
    def set_val(self, val):
        self.remove(self.val_box)
        self.val_box = Tex(str(val), font_size=self.font_size).move_to(self.box_pos)
        self.val = val
        self.add(self.val_box)

class BinaryLiftingTable(VGroup):
    def __init__(self, number_of_nodes : int, position_table : tuple, box_width : float, box_height : float, color : str,*vmobjects, **kwargs):
        super().__init__(*vmobjects, **kwargs)
        self.n = number_of_nodes
        self.position_table = position_table
        self.box_width = box_width
        self.box_height = box_height
        self.log = 1
        self.color = color
        
        # number of columns
        while((1 << self.log-1) <= self.n):
            self.log+=1
        
        self.table_map_blt_object = [[None for k in range(self.log+1)] for node in range(self.n+1)]
        self.binary_lifting_calc = [[-1 for k in range(self.log)] for node in range(self.n)]
        
        index_blt = 0
        self.blt = VGroup()  # Create a VGroup to hold all MyCell objects

        for j in range(self.log):
            cell = MyCell(
                box_pos=(position_table + (RIGHT * (box_width + 0.025) * (j + 1))), 
                val=f"{j}", 
                color=self.color,
                box_width=box_width,
                box_height=box_width
                )
            self.table_map_blt_object[0][j+1] = index_blt
            index_blt+=1
            self.blt.add(cell)

        for i in range(self.n):
            cell = MyCell(
                box_pos=(position_table + (DOWN * (box_width + 0.025) * (i + 1))), 
                val=f"{i}", 
                color=self.color,
                box_width=box_width,
                box_height=box_width
                )
            self.table_map_blt_object[i+1][0] = index_blt
            index_blt+=1
            self.blt.add(cell)

        for i in range(self.n):
            first_element_index_blt = self.table_map_blt_object[i+1][0]
            position_of_row_i = self.blt[first_element_index_blt].box_pos
            for j in range(self.log):
                cell = MyCell(
                    box_pos=(position_of_row_i + (RIGHT * (box_width + 0.025) * (j + 1))), 
                    val="-1",
                    color=self.color, 
                    box_width=box_width,
                    box_height=box_width
                    )
                self.table_map_blt_object[i+1][j+1] = index_blt
                self.blt.add(cell)
                index_blt+=1

        self.add(self.blt)

class BinaryLiftingScene(Scene):
    def __init__(self):
        super().__init__()
        # Tree and connections
        self.start_position = (3.5, 3, 0)
        self.n = 11 # number of nodes
        self.positions = {
            0:self.start_position,
            
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
        self.connections = [
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
        
        self.nodes_obj = VGroup()
        self._create_all_nodes()
        self.edges_objects = {i : {} for i in range(len(self.connections))} # map node i to node j arc and return position on tree VGroup
        self.tree = VGroup()
        self._create_all_arcs()
        # first parent of each node ith
        self.parents = [-1,0,0,1,2,0,1,3,6,1,8]
        # Binary Lifting table
        self.blt = BinaryLiftingTable(
            number_of_nodes=self.n,
            position_table=(-4,3,0),
            box_width=0.5,
            box_height=0.5,
            color=GRAY_A
            )
        
        # calculate inmediate parent
        for i in range(self.blt.n):
            self.blt.binary_lifting_calc[i][0] = self.parents[i]
        
        # calculate rest of parents
        for i in range(1, self.n):
            for j in range(1, self.blt.log):
                self.blt.binary_lifting_calc[i][j] = self.blt.binary_lifting_calc[ self.blt.binary_lifting_calc[i][j-1] ][j - 1]
        
        self.orig_node_color = self.nodes_obj[0].get_color()
        self.orig_parent_color = self.nodes_obj[0].get_color()
        self.orig_table_color = self.blt.blt[self.blt.table_map_blt_object[1][1]].box.get_color()
        self.orig_arc_color = self.tree[0].get_color()
    
    def _create_all_nodes(self):
        for i in range(self.n):
            node = Node(
                radius=0.22,
                color=BLUE_A,
                value=i,
                position=self.positions[i])
            self.nodes_obj.add(node)
    
    def _create_all_arcs(self):
        tree_index = 0 # position on VGroup
        for i, j in self.connections:
            # This part is only for aesthetics
            # The line start from point x1,y1 + GAP
            # to x2,y2 + GAP
            # where x1, y1 is the center of the start object
            # and x2, y2 is the center of the end object
            # So, without this part the line start from x1,y1 to x2,y2
            # that's the case where GAP = 0. But this is not very
            # comfortable to see, and for that reason
            # we add this part on the code
            p1 = self.nodes_obj[i].get_center()
            p2 = self.nodes_obj[j].get_center()
            m = float(p2[0]-p1[0]) / float(p2[1]-p1[1])
            x1,y1 = p1[0],p1[1]
            x2,y2 = p2[0],p2[1]
            r = self.nodes_obj[i].radius * 0.2
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
            self.tree.add(
                Line(
                    start=(x1,y1,0), 
                    end=(x2,y2,0), 
                    buff=0.2,
                    stroke_width=3,
                )
            )
            self.edges_objects[i][j] = tree_index
            tree_index+=1
        
    def animation_fill_parents_on_table(self):
        
        for j in range(self.blt.log):
            # Iterator animation for binary lifting table
            id_blt_1 = self.blt.table_map_blt_object[1][2]
            id_blt_2 = self.blt.table_map_blt_object[1][3]
            
            id_blt_1_pos = self.blt.blt[id_blt_1].box_pos
            id_blt_2_pos = self.blt.blt[id_blt_2].box_pos
            
            init_pos = (id_blt_1_pos + id_blt_2_pos)/2
            
            ite_blt = Rectangle(width=0.51*(self.blt.log+1), height=0.5, fill_opacity=0.01, color=YELLOW_C).move_to(init_pos)
            ite_blt.set_stroke(color=YELLOW_C,width=2)
            
            id_blt = self.blt.table_map_blt_object[1][j+1]
            current_cell_position = self.blt.blt[id_blt].box_pos
            current_cell = Rectangle(width=0.5, height=0.5, fill_opacity=0.1, color=BLUE_C).move_to(current_cell_position)
            current_cell.set_stroke(color=BLUE_C,width=3)
            
            self.play(FadeIn(ite_blt),FadeIn(current_cell))
            
            for i in range(self.blt.n):
                init_pos_target = init_pos + (DOWN * (0.5 + 0.025) * i)
                id_blt = self.blt.table_map_blt_object[i+1][j+1]
                current_cell_position = self.blt.blt[id_blt].box_pos
                
                self.play(
                    ite_blt.animate.move_to(init_pos_target),
                    current_cell.animate.move_to(current_cell_position),
                    run_time=0.5
                    )
                
                self.play(self.nodes_obj[i].animate.set_color(BLUE_C),  run_time=1)
                    
                #print(f"node ith = {i}, jth = {j}")
                #print("Solution >> self.blt.binary_lifting_calc[i][j] =", self.blt.binary_lifting_calc[i][j])
                if(self.blt.binary_lifting_calc[i][j] != -1):
                    
                    node_id_previous_ancestor = self.blt.binary_lifting_calc[i][j-1]
                    id_blt_prev = self.blt.table_map_blt_object[i+1][j]
                    
                    if (j != 0): self.play(self.blt.blt[id_blt_prev].box.animate.set_color(GREEN_A),run_time=0.5)
                    
                    node_id_current_ancestor = self.blt.binary_lifting_calc[i][j]
                    id_blt_take = self.blt.table_map_blt_object[node_id_previous_ancestor+1][j]
                    
                    arc_change = VGroup()
                    node_change = VGroup()
                    start = i
                    while(start != node_id_current_ancestor):
                        id_tree = self.edges_objects[self.parents[start]][start]
                        self.play(self.tree[id_tree].animate.set_color(BLUE_C), run_time=0.5)
                        self.play(self.nodes_obj[self.parents[start]].animate.set_color(BLUE_C), run_time=0.5)
                        arc_change.add(self.tree[id_tree])
                        node_change.add(self.nodes_obj[self.parents[start]])
                        start = self.parents[start]
                    
                    if(j != 0): self.play(self.blt.blt[id_blt_take].box.animate.set_color(GREEN_A),run_time=0.5)     
                    self.play(self.blt.blt[id_blt].animate.set_val(start),run_time=0.5)
                    
                    self.wait(2)
                    
                    # Animation to return all changes to the original color
                    self.play(
                        arc_change.animate.set_color(self.orig_arc_color),  # Return arc color to original
                        node_change.animate.set_color(self.orig_parent_color),  # Return parent node color to original
                        run_time=0.5
                    )
                    
                    self.play(self.nodes_obj[i].animate.set_color(self.orig_node_color),run_time=0.5)  # Return current node color to original
                    if(j != 0): self.play(self.blt.blt[id_blt_take].box.animate.set_color(self.orig_table_color),run_time=0.5)
                    if(j != 0): self.play(self.blt.blt[id_blt_prev].box.animate.set_color(self.orig_table_color),run_time=0.5)
                else:
                    # Return current node color to original
                    self.play(self.nodes_obj[i].animate.set_color(self.orig_node_color), run_time=0.5)
                    continue
            self.play(FadeOut(ite_blt),FadeOut(current_cell),run_time=0.5)
                    
    def animate_kth_ancestor(self,k : int, leaf : int, res : int):  
        node_change = VGroup()
        arc_change = VGroup()
        
        id_blt = self.blt.table_map_blt_object[leaf+1][0]
        current_cell_position = self.blt.blt[id_blt].box_pos
        current_cell = Rectangle(width=0.5, height=0.5, fill_opacity=0.1, color=BLUE_C).move_to(current_cell_position)
        current_cell.set_stroke(color=BLUE_C,width=3)
        self.play(self.nodes_obj[leaf].animate.set_color(BLUE_C), FadeIn(current_cell),run_time=1)
        node_change.add(self.nodes_obj[leaf])
        self.wait()
        
        start = leaf
        for j in range(self.blt.log):
            if( k & (1<<j) ):
                #print(f"start, k = {start}, {k}")
                #print(f"j, (1 << j) = {j}, {(1<<j)}")
                #print("blt.binary_lifting_calc[start][j] =",self.blt.binary_lifting_calc[start][j])
                id_blt = self.blt.table_map_blt_object[start+1][j+1]
                current_cell_position = self.blt.blt[id_blt].box_pos
                self.play(current_cell.animate.move_to(current_cell_position),run_time=0.5)
                
                node_from = start
                node_to = self.blt.binary_lifting_calc[start][j]
                while(node_from != node_to):
                    id_tree = self.edges_objects[self.parents[node_from]][node_from]
                    self.play(self.tree[id_tree].animate.set_color(BLUE_C), run_time=0.5)
                    self.play(self.nodes_obj[self.parents[node_from]].animate.set_color(BLUE_C), run_time=0.5)
                    arc_change.add(self.tree[id_tree])
                    node_change.add(self.nodes_obj[self.parents[node_from]])
                    node_from = self.parents[node_from]
                
                id_blt = self.blt.table_map_blt_object[self.blt.binary_lifting_calc[start][j]+1][0]
                current_cell_position = self.blt.blt[id_blt].box_pos
                self.play(current_cell.animate.move_to(current_cell_position),run_time=0.5)
                
                node_change.add(self.nodes_obj[self.blt.binary_lifting_calc[start][j]])
                arc_change.add(self.tree[id_tree])
                
                start = self.blt.binary_lifting_calc[start][j]
        self.wait(2)
        self.play(
                arc_change.animate.set_color(self.orig_arc_color),  # Return arc color to original
                node_change.animate.set_color(self.orig_node_color),  # Return parent node color to original
                FadeOut(current_cell),
                run_time=0.5
            )
        
        #print(f"el kth = {k} ancestor of node {leaf} is {start}")
        
    def construct(self):
        self.play(Create(self.nodes_obj), Create(self.tree))
        self.wait()
        
        self.play(Create(self.blt))
        self.wait()
        
        self.animation_fill_parents_on_table()
        self.wait()
        
        # Calculate kth = 4 ancestor for node 10, the answers is node 0
        # get all the path on table and the graph for animation
        self.animate_kth_ancestor(k=4,leaf=10,res=0)
        self.wait(1)  
              
        # Calculate kth = 3 ancestor for node 10, the answers is node 1
        # get all the path on table and the graph for animation
        self.animate_kth_ancestor(k=3,leaf=10,res=0)
        self.wait(1)
        
