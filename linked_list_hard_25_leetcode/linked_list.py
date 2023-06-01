from manim import *

class Node(VGroup):
    def __init__(self, value, radius=0.3, color=BLUE):
        super().__init__()
        self.radius = radius
        self.circle = Circle(radius=radius, color=color)
        self.text = Text(str(value))
        self.add(self.circle, self.text)

    def set_position(self, position):
        self.move_to(position)
    
    def set_color(self, color):
        self.remove(self.circle)  # Remove the current circle
        self.circle = Circle(radius=self.radius, color=color)
        self.add(self.circle)  # Add the new circle to the scene
        self.circle.move_to(self.text.get_center()) 

class Pointers(VGroup):
    def __init__(self, node, name, unit=1):
        super().__init__()
        self.is_up = unit
        self.arrow = Arrow(
            node.get_center() + self.is_up * 1.5 * UP,
            node.get_center() + self.is_up * 0.5 * UP,
            buff=0.2,
            max_tip_length_to_length_ratio=0.15,
            max_stroke_width_to_length_ratio=5,
        )

        self.name = Text(name, font_size=30).next_to(self.arrow, UP if self.is_up == 1 else DOWN)
        self.add(self.arrow, self.name)

    def set_position(self, node_start, node_end):
        offset = 0.5 if self.is_up == 1 else -0.5
        self.arrow.put_start_and_end_on(
            node_start.get_center() + self.is_up * 1.5 * UP + offset * RIGHT,  
            node_end.get_center() + self.is_up * 0.5 * UP - offset * RIGHT, 
        )
        self.name.next_to(self.arrow, UP if self.is_up == 1 else DOWN)

class LinkedList(Scene):
    def construct(self):
        
        # Add title and subtitle
        title = Text("Leetcode: 25 Reverse Nodes in K-group", font_size=40)
        subtitle = Text("Time O(n) and Space O(1)", font_size=30)
        title_subtitle = VGroup(title, subtitle)
        title_subtitle.arrange(DOWN, center=False)
        title_subtitle.move_to(ORIGIN)
        self.play(Create(title_subtitle), run_time=1)
        self.wait(2)
        self.play(FadeOut(title_subtitle), run_time=1)
        
        # Add additional text
        logic_text = Text("The Logic of this code divides into two parts:", font_size=30)
        logic_text.to_edge(UP)
        part1_text = Text("1. Reverse the nodes of the kth group at the moment.", font_size=25)
        part2_text = Text("2. Unite the previous group (last_k_pointer) with the current group kth.", font_size=25)
        part3_text = Text("Check an example, with k = 3", font_size=30)
        logic_parts = VGroup(logic_text, part1_text, part2_text,part3_text)
        logic_parts.move_to(ORIGIN)
        logic_parts.arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        self.play(Create(logic_parts), run_time=1)
        self.wait(3)
        self.play(FadeOut(logic_parts), run_time=1)
        
        values = [1, 2, 3, 4, 5, 6, 7, 8]  # The values in the linked list
        node_spacing = 1.5

        nodes = VGroup()  # Group to hold all the nodes
        prev_node = None

        for value in values:
            node = Node(value)
            nodes.add(node)

            if prev_node:
                # Set position of the current node based on the position of the previous node
                node.set_position(prev_node.get_center() + node_spacing * RIGHT)

            prev_node = node

        # Center the linked list on the screen
        nodes.move_to(ORIGIN)

        # Animate the creation of nodes
        self.play(*[Create(node) for node in nodes], run_time=1)

        # Animate arrows between nodes
        arrows = VGroup()
        for i in range(len(nodes) - 1):
            arrow = Arrow(
                nodes[i].get_center() + 0.1 * RIGHT,
                nodes[i + 1].get_center() - 0.1 * RIGHT,
                buff=0.2,
                max_tip_length_to_length_ratio=0.15,
                max_stroke_width_to_length_ratio=5,
            )
            arrows.add(arrow)

        self.play(Create(arrows), run_time=1)

        # Create an arrow at node 1
        change_pointer = Pointers(nodes[0], "change")
        nxt_pointer = Pointers(nodes[1], "nxt")
        prev_pointer = Pointers(nodes[0], "prev", unit=-1)

        # Add the arrows to the respective nodes

        self.play(Create(change_pointer), Create(nxt_pointer), Create(prev_pointer), run_time=1)

        # Move the change pointer to the second node
        self.play(Transform(change_pointer, Pointers(nodes[1], "change")),
                Transform(nxt_pointer, Pointers(nodes[2], "nxt")),
                run_time=1)
        
        start_pointer = Pointers(nodes[0], "start")
        
        self.play(Create(start_pointer), run_time=1)
        self.play(FadeOut(arrows[0]))
        self.remove(arrows[0])
        self.play(FadeOut(arrows[1]))
        arrows[1] = Arrow(
                nodes[1].get_center() + 0.2 * LEFT,
                nodes[0].get_center() - 0.1 * LEFT,
                buff=0.2,
                max_tip_length_to_length_ratio=0.15,
                max_stroke_width_to_length_ratio=5,)
        self.play(FadeIn(arrows[1]))
        
        # Move the change pointer to the second node
        self.play(
            Transform(prev_pointer, Pointers(nodes[1], "prev", unit=-1)),
            Transform(change_pointer, Pointers(nodes[2], "change")),
            Transform(nxt_pointer, Pointers(nodes[3], "nxt")),
            run_time=1)
        self.play(FadeOut(arrows[2]))
        arrows[2] = Arrow(
                nodes[2].get_center() + 0.2 * LEFT,
                nodes[1].get_center() - 0.1 * LEFT,
                buff=0.2,
                max_tip_length_to_length_ratio=0.15,
                max_stroke_width_to_length_ratio=5,)
        self.play(FadeIn(arrows[2]))
        
        end_pointer = Pointers(nodes[2],"end", unit=-1)
        last_k_pointer = Pointers(nodes[0], "last_k", unit=-1)
        
        self.play(Create(end_pointer), Create(last_k_pointer),run_time=1)
        
        self.play(
            Transform(prev_pointer, Pointers(nodes[3], "prev", unit=-1)),
            Transform(change_pointer, Pointers(nodes[3], "change")),
            Transform(nxt_pointer, Pointers(nodes[4], "nxt")),
            run_time=1)
        
        nodes[0].set_color(RED)
        nodes[1].set_color(RED)
        nodes[2].set_color(RED)
        self.play(*[Transform(node.circle, node.circle) for node in nodes[0:3]], run_time=1)
        
        self.play(FadeOut(arrows[3]))
        self.remove(arrows[3])
        self.play(Transform(change_pointer, Pointers(nodes[4], "change")),
                Transform(nxt_pointer, Pointers(nodes[5], "nxt")),
                run_time=1)
        self.play(FadeOut(arrows[4]))
        arrows[4] = Arrow(
                nodes[4].get_center() + 0.2 * LEFT,
                nodes[3].get_center() - 0.1 * LEFT,
                buff=0.2,
                max_tip_length_to_length_ratio=0.15,
                max_stroke_width_to_length_ratio=5,)
        self.play(FadeIn(arrows[4]))
        
        self.play(
            Transform(prev_pointer, Pointers(nodes[4], "prev", unit=-1)),
            Transform(change_pointer, Pointers(nodes[5], "change")),
            Transform(nxt_pointer, Pointers(nodes[6], "nxt")),
            run_time=1)
        self.play(FadeOut(arrows[5]))
        arrows[5] = Arrow(
                nodes[5].get_center() + 0.2 * LEFT,
                nodes[4].get_center() - 0.1 * LEFT,
                buff=0.2,
                max_tip_length_to_length_ratio=0.15,
                max_stroke_width_to_length_ratio=5,)
        self.play(FadeIn(arrows[5]))
        
        self.play(
            Transform(start_pointer, Pointers(nodes[3], "start")),
            Transform(end_pointer, Pointers(nodes[5], "end",unit=-1)),
            run_time=1
        )
        
        self.play(
            Transform(prev_pointer, Pointers(nodes[6], "prev", unit=-1)),
            Transform(change_pointer, Pointers(nodes[6], "change")),
            Transform(nxt_pointer, Pointers(nodes[7], "nxt")),
            run_time=1)
        

        nodes[3].set_color(GREEN)
        nodes[4].set_color(GREEN)
        nodes[5].set_color(GREEN)
        self.play(*[Transform(node.circle, node.circle) for node in nodes[3:6]], run_time=1)
        
                
        m4 = CurvedArrow(
            start_point = nodes[0].get_center() + 0.3 * UP, 
            end_point = nodes[5].get_center() + 0.3 * UP,
            radius= -5,
            angle=-TAU / 2,  # Adjust the angle to create a curved arrow
            tip_length=0.15,  # Adjust the tip_length for a smaller arrowhead
            )
        self.play(Create(m4))
        
        self.play(
            Transform(last_k_pointer, Pointers(nodes[3], "last_k", unit=-1)),
            run_time=1)
        self.play(FadeOut(start_pointer), FadeOut(end_pointer))
        
        m5 = CurvedArrow(
            start_point = nodes[3].get_center() + 0.3 * DOWN, 
            end_point = nodes[6].get_center() + 0.3 * DOWN,
            radius= 5,
            angle=-TAU / 2,  # Adjust the angle to create a curved arrow
            tip_length=0.15,  # Adjust the tip_length for a smaller arrowhead
            )
        self.play(Create(m5))
        
        self.play(FadeOut(last_k_pointer), FadeOut(change_pointer), FadeOut(prev_pointer), FadeOut(nxt_pointer))
        
        self.wait(1)
        
        self.play(FadeOut(m4), FadeOut(m5))
        self.remove(m4,m5)
        
        self.play(*[FadeOut(arrows[i]) for i in range(1,3)], *[FadeOut(arrows[i]) for i in range(4,7)])
        self.play(*[FadeOut(n) for n in nodes])
        
        self.remove(nodes, arrows)
        
        values = [3, 2, 1, 6, 5, 4, 7, 8]  # The values in the linked list
        node_spacing = 1.5

        nodes = VGroup()  # Group to hold all the nodes
        prev_node = None

        for value in values:
            if(value < 4):
                color = RED
            elif(value < 7):
                color = GREEN
            else:
                color = BLUE
            node = Node(value, color = color)
            nodes.add(node)

            if prev_node:
                # Set position of the current node based on the position of the previous node
                node.set_position(prev_node.get_center() + node_spacing * RIGHT)

            prev_node = node

        # Center the linked list on the screen
        nodes.move_to(ORIGIN)
        
        # Animate the creation of nodes
        self.play(*[Create(node) for node in nodes], run_time=1)
        arrows = VGroup()
        for i in range(len(nodes) - 1):
            arrow = Arrow(
                nodes[i].get_center() + 0.1 * RIGHT,
                nodes[i + 1].get_center() - 0.1 * RIGHT,
                buff=0.2,
                max_tip_length_to_length_ratio=0.15,
                max_stroke_width_to_length_ratio=5,
            )
            arrows.add(arrow)

        self.play(Create(arrows), run_time=1)
        
        self.wait(1)
        self.remove(nodes)
        
        values = [3, 2, 1, 6, 5, 4, 7, 8]  # The values in the linked list
        node_spacing = 1.5

        nodes = VGroup()  # Group to hold all the nodes
        prev_node = None

        for value in values:
            node = Node(value, color = BLUE)
            nodes.add(node)
            if prev_node:
                # Set position of the current node based on the position of the previous node
                node.set_position(prev_node.get_center() + node_spacing * RIGHT)
            prev_node = node

        # Center the linked list on the screen
        nodes.move_to(ORIGIN)
        
        # Animate the creation of nodes
        self.play(*[Create(node) for node in nodes], run_time=1)
        
        self.wait(3)
