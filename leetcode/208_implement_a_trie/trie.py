from manim import *

class StructRepresentation(VGroup):
    def __init__(self, pos, radius, node_text, *vmobjects, **kwargs):
        super().__init__(*vmobjects, **kwargs)
        self.radius = radius
        self.pos = pos
        self.node_text = node_text
        
        self.circle = Circle(radius=self.radius,color=BLUE_B,fill_opacity=0.3).move_to(self.pos)
        self.text = Text("Node", font_size=self.node_text,color=BLUE_B).move_to(self.circle.get_center()+UP*(self.radius+0.2))
        self.add(self.circle, self.text)
    
    def flag_representation(self):
        self.bool_text = Text("bool flag",font_size=self.node_text-5,color=RED_B).move_to(self.circle.get_center()+UP*(self.radius*0.2))
        self.add(self.bool_text)
    
    def link_representation(self):
        self.link_text = Text("Node * links[26]", font_size=self.node_text-7,color=PINK).move_to(self.circle.get_center()+DOWN*(self.radius*0.2))
        self.add(self.link_text)

class LinksData(VGroup):
    def __init__(self, k, value, box_width, box_pos,*vmobjects, **kwargs):
        super().__init__(*vmobjects, **kwargs)
        self.box_pos = box_pos
        self.box_width = box_width
        self.value = value
        self.k = k
        
        self.current_pos = RIGHT * self.k * (self.box_width + 0.1)
        self.box = Rectangle(width=self.box_width, height=self.box_width, fill_opacity=0.2, color=LIGHT_PINK).move_to(box_pos + self.current_pos)
        self.arrow = Arrow(start=self.box.get_center()+UP*0.1, end=self.box.get_center()+UP*(0.4+self.box_width))
        self.link_text = Text("Node *", font_size=13,color=PINK).move_to(self.box.get_center())
        self.value_text = Text(str(self.value), font_size=16).move_to(self.box.get_center()+DOWN*self.box_width*0.8)
        self.add(self.box,
                 self.arrow,
                 self.link_text,
                 self.value_text)

class LinksRepresentation(VGroup):
    def __init__(self,box_pos, box_width, *vmobjects, **kwargs):
        super().__init__(*vmobjects, **kwargs)
        self.link_group = VGroup()
        self.box_pos = box_pos
        self.box_width = box_width
        k = 0
        for i in [0,1,2,-1,-1,-1,24,25]:
            if(i != -1):
                data = LinksData(k,i,self.box_width,self.box_pos)
                self.link_group.add(data)
            else:
                self.link_group.add(Dot(point=self.box_pos+RIGHT * k * (self.box_width + 0.1)))
            k+=1
                
        self.add(self.link_group)

class StructNodeCode(VGroup):
    def __init__(self,pos):
        super().__init__()
        code_str = '''
        struct Node{
            Node* links[26];
            bool flag=false;
        };'''
        self.pos=pos
        self.code = self.build_code_block(code_str)
    
    def build_code_block(self, code_str):
        def remove_invisible_chars(mobject: SVGMobject) -> SVGMobject:
            """Function to remove unwanted invisible characters from some mobjects.

            Parameters
            ----------
            mobject
                Any SVGMobject from which we want to remove unwanted invisible characters.

            Returns
            -------
            :class:`~.SVGMobject`
                The SVGMobject without unwanted invisible characters.
            """
            # TODO: Refactor needed
            iscode = False
            if mobject.__class__.__name__ == "Text":
                mobject = mobject[:]
            elif mobject.__class__.__name__ == "Code":
                iscode = True
                code = mobject
                mobject = mobject.code
            mobject_without_dots = VGroup()
            if mobject[0].__class__ == VGroup:
                for i in range(len(mobject)):
                    mobject_without_dots.add(VGroup())
                    mobject_without_dots[i].add(*(k for k in mobject[i] if k.__class__ != Dot))
            else:
                mobject_without_dots.add(*(k for k in mobject if k.__class__ != Dot))
            if iscode:
                code.code = mobject_without_dots
                return code
            return mobject_without_dots
        # build the code block
        code = Code(code=code_str, language='C++', background="window",line_spacing=1,font_size=20).move_to(self.pos)
        code.code = remove_invisible_chars(code.code)
        self.add(code)
        # build sliding windows (SurroundingRectangle)
        self.sliding_wins = VGroup()
        height = code.code[0].height
        for line in code.code:
            self.sliding_wins.add(
                SurroundingRectangle(line)
                .set_fill(YELLOW)
                .set_opacity(0)
                .stretch_to_fit_width(code.background_mobject.get_width())
                .align_to(code.background_mobject, LEFT)
            )

        self.add(self.sliding_wins)
        return code
    
    def highlight_scene(self, scene):
        for i in range(len(self.code.code)-1):
            self.highlight(i, i+1, scene)
            
    def highlight(self, prev_line, line, scene):
        scene.play(self.sliding_wins[prev_line].animate.set_opacity(0.3))
        scene.play(ReplacementTransform(self.sliding_wins[prev_line], self.sliding_wins[line]))
        scene.play(self.sliding_wins[line].animate.set_opacity(0.3))

class InsertChars(VGroup):
    def __init__(self, insert_char, pos,*vmobjects, **kwargs):
        super().__init__(*vmobjects, **kwargs)
        self.ic = insert_char # 1
        self.ii = ord(insert_char) # 2 or 3
        self.m = ord(insert_char)-ord('a') # 1 or 2
        
        self.tx1 = "1. Insert '{}'".format(self.ic)
        self.tx2 = "2. Map: '{}' - 'a' = {}".format(self.ic, self.m)
        self.tx3 = "3. Ascii code: '{}' = {}".format(self.ic, self.ii)
        self.tx4 = "4. Map: {} - 97 = {}".format(self.ii, self.m)
        self.tx5 = "5. p->links[{}] = new Node()".format(self.m)
        
        t1 = Text(self.tx1)
        t2 = Text(self.tx2)
        t3 = Text(self.tx3)
        t4 = Text(self.tx4)
        t5 = Text(self.tx5)
        self.x = VGroup(t1, t2, t3, t4, t5).arrange(direction=DOWN, aligned_edge=LEFT).scale(0.4).move_to(pos)
        self.add(self.x)
        
    def apply_change(self, tx : str, ctx : str, i : int, color : str, scene, start=0):
        li = tx.replace(" ","").index(ctx, start)
        colored_text = self.x[i][li:li + len(ctx)].copy()
        colored_text.set_color(color)
        scene.play(Transform(self.x[i][li:li + len(ctx)], colored_text))
    
    def cc1(self, scene):
        self.apply_change(self.tx1,str(self.ic),0,YELLOW_C,scene)

    def cc2(self, scene):
        self.apply_change(self.tx2,str(self.ic),1,YELLOW_C,scene,6)
        self.apply_change(self.tx2,str(self.m),1,GREEN_C,scene)
        
    def cc3(self, scene):
        self.apply_change(self.tx3,str(self.ic),2,YELLOW_C,scene)
        self.apply_change(self.tx3,str(self.ii),2,BLUE_C,scene)

    def cc4(self, scene):
        self.apply_change(self.tx4,str(self.ii),3,BLUE_C,scene)
        self.apply_change(self.tx4,str(self.m),3,GREEN_C,scene)

    def cc5(self, scene):
        self.apply_change(self.tx5,str(self.m),4,GREEN_C,scene)
        self.apply_change(self.tx5,"new",4,BLUE_C,scene)
        self.apply_change(self.tx5,"Node",4,YELLOW_C,scene)
        
class Trie(Scene):
    def construct(self):
        struct_code = StructNodeCode(pos=ORIGIN+DOWN*1.5)
        self.play(Write(struct_code[0]), run_time=1)
        struct_representation = StructRepresentation(pos=ORIGIN+UP*1.5, radius=1.0, node_text=25)
        self.wait(2)
        
        struct_code.highlight(0, 0, self)
        self.add(struct_representation)
        self.play(FadeIn(struct_representation), run_time=1)
        self.wait(1)
        
        struct_code.highlight(0, 2, self)
        struct_representation.flag_representation()
        self.play(FadeIn(struct_representation.bool_text), run_time=1)
        self.wait(1)
        
        struct_code.highlight(2, 1, self)
        struct_representation.link_representation()
        self.play(FadeIn(struct_representation.link_text), run_time=1)
        self.wait(1)
        
        box_pos = np.array([[-2.2, -1.5, 0]])
        box_width = 0.7
        link_representation = LinksRepresentation(box_pos=box_pos, box_width=box_width)
        self.play(FadeOut(struct_code))
        self.add(link_representation)
        self.play(Create(link_representation))
        self.wait(1)
        
        self.play(FadeOut(struct_representation), run_time=1)
        self.wait(1)
        
        title = Title("Mapping", color=WHITE)
        self.add(title)
        
        # Si insertamos un char 'a' - 'a' = 0  
        # el ascii code del caracter 'a' = 97 -> 97 - 97 = 0
        # Por lo tanto, creamos una instancia Node en la posición 0 del array
        i = InsertChars('a',pos=ORIGIN+UP*1.8)
        self.play(Write(i), run_time=1)
        self.wait(1)
        
        struct_representation = StructRepresentation(pos=link_representation[0][0].get_center()+UP*(1.3), radius=0.5, node_text=15)
        struct_representation.flag_representation()
        struct_representation.link_representation()
        self.add(struct_representation)
        self.play(Create(struct_representation), run_time=3)
        self.wait(2)
        
        i.cc1(self)
        self.wait(0.5)
        i.cc2(self)
        self.wait(0.5)
        i.cc3(self)
        self.wait(0.5)
        i.cc4(self)
        self.wait(0.5)
        i.cc5(self)
        
        self.wait(1)
        
        self.play(FadeOut(i, struct_representation))
        
        # Si insertamos un char 'b' para mapearlo en el array 'b' - 'a' = 1
        # el ascii code del caracter 'b' = 98 -> 98 - 97 = 1
        # Por lo tanto, creamos una instancia Node en la posición 1 del array
        i = InsertChars('y',pos=ORIGIN+UP*1.8)
        self.play(Write(i), run_time=1)
        self.wait(1)
        
        struct_representation = StructRepresentation(pos=link_representation[0][6].get_center()+UP*(1.3), radius=0.5, node_text=15)
        struct_representation.flag_representation()
        struct_representation.link_representation()
        self.add(struct_representation)
        self.play(Create(struct_representation), run_time=3)
        self.wait(2)
        
        i.cc1(self)
        self.wait(0.5)
        i.cc2(self)
        self.wait(0.5)
        i.cc3(self)
        self.wait(0.5)
        i.cc4(self)
        self.wait(0.5)
        i.cc5(self)
        
        self.wait(1)
        
        
        
        
        
    
