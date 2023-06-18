from manim import *
import random

class AutomataCell(VGroup):
    def __init__(self, cells_init, box_width, color_live=BLACK):
        super().__init__()
        self.color = WHITE # color of the stroke (border)
        self.fill_opacity = 0.5
        self.pos = cells_init
        self.box_width = box_width
        self.color_live = color_live
        self.box = Rectangle(
            width=self.box_width, 
            height=self.box_width, 
            fill_opacity=self.fill_opacity, 
            color=self.color, 
            fill_color=self.color_live, 
            stroke_width=1
        ).move_to(self.pos)
        self.add(self.box)
    
    def set_neighbors(self):
        self.box.generate_target()
        self.box.target.set_fill(color=YELLOW)
    
    def set_live(self):
        self.box.generate_target()
        self.box.target.set_fill(color=WHITE)
    
    def set_died(self):
        self.box.generate_target()
        self.box.target.set_fill(color=BLACK)

class GameOfLifeScene(Scene):
    def construct(self):
        cells_init = np.array([-7, 4, 0])
        box_width = 0.3
        
        plane = NumberPlane()
        length_x_axis = abs(plane.x_range[0]) + plane.x_range[1]
        length_y_axis = abs(plane.y_range[0]) + plane.y_range[1]
        
        print(length_x_axis, length_y_axis)
        
        automata_x_axis = int(length_x_axis / box_width)
        automata_y_axis = int(length_y_axis / box_width)
        
        print(automata_x_axis, automata_y_axis)
        
        automata_cell_vgroup = VGroup()
        grid = [[None for i in range(automata_x_axis)] for j in range(automata_y_axis)]
        for i in range(automata_y_axis):
            for j in range(automata_x_axis):
                automata_cell = AutomataCell(cells_init + DOWN*i*box_width + RIGHT*j*box_width, box_width)
                grid[i][j] = automata_cell
                automata_cell_vgroup.add(automata_cell)
        
        
        
        self.add(automata_cell_vgroup)
        self.play(FadeIn(automata_cell_vgroup), run_time=2)
        self.wait()
        
        # Check the neighs
        # horizontal
        # vertical
        # diag
        
        # Check the rules
        # Rule 1: Any live cell with fewer than two live neighbours dies, as if by underpopulation.
        # Rule 2: Any live cell with two or three live neighbours lives on to the next generation.
        # Rule 3: Any live cell with more than three live neighbours dies, as if by overpopulation.
        # Rule 4: Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction. 
        
        # Pattern Examples
        # Penta - decathlon pattern init
        mid_y = int(automata_y_axis/2)
        mid_x = int(automata_x_axis/2)
        penta_init = [
            (mid_y-8,mid_x),
            (mid_y-7,mid_x),
            (mid_y-6,mid_x),
            (mid_y-6,mid_x-1),
            (mid_y-6,mid_x+1),
            
            (mid_y-3,mid_x+1),
            (mid_y-3,mid_x-1),
            (mid_y-3,mid_x),
            
            (mid_y-2,mid_x),
            (mid_y-1,mid_x),
            (mid_y,mid_x),
            (mid_y+1,mid_x),
            
            (mid_y+2,mid_x+1),
            (mid_y+2,mid_x-1),
            (mid_y+2,mid_x),
            
            (mid_y+5,mid_x+1),
            (mid_y+5,mid_x-1),
            (mid_y+5,mid_x),
            (mid_y+6,mid_x),
            (mid_y+7,mid_x),
            ]
        
        anims = []
        for p in penta_init:
            automata_cell = grid[p[0]][p[1]]
            automata_cell.set_live()
            anims.append(MoveToTarget(automata_cell.box))

        self.play(*anims)
        self.wait()

if __name__ == "__main__":
    config = {
        "pixel_height": 720,
        "pixel_width": 1280,
        "background_color": WHITE,
        "frame_rate": 30,
    }
    scene = GameOfLifeScene()
    scene.render(config=config)