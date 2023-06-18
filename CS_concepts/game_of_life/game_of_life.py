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
        self.is_live = False
        self.box = Rectangle(
            width=self.box_width, 
            height=self.box_width, 
            fill_opacity=self.fill_opacity, 
            color=self.color, 
            fill_color=self.color_live, 
            stroke_width=1
        ).move_to(self.pos)
        self.add(self.box)
    
    def get_is_live(self):
        return self.is_live
    
    def set_is_live(self):
        self.is_live = not self.is_live
    
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
        
        automata_x_axis = int(length_x_axis / box_width) # m : number of cols
        automata_y_axis = int(length_y_axis / box_width) # n : number of rows
        
        print(automata_x_axis, automata_y_axis)
        
        automata_cell_vgroup = VGroup()
        grid = [[None for i in range(automata_x_axis)] for j in range(automata_y_axis)]
        for i in range(1, automata_y_axis):
            for j in range(1, automata_x_axis):
                automata_cell = AutomataCell(cells_init + DOWN*i*box_width + RIGHT*j*box_width, box_width)
                grid[i][j] = automata_cell
                automata_cell_vgroup.add(automata_cell)
        
        
        
        self.add(automata_cell_vgroup)
        self.play(FadeIn(automata_cell_vgroup), run_time=2)
        self.wait()
        
        # start from middle
        mid_y = int(automata_y_axis/2)
        mid_x = int(automata_x_axis/2)
        automata_cell = grid[mid_y][mid_x]
        automata_cell.set_live()
        self.play(MoveToTarget(automata_cell.box))
        
        # Check the neighs
        # horizontal
        anims = []
        horizontal = [1, -1]
        for h in horizontal:
            automata_cell = grid[mid_y+h][mid_x]
            automata_cell.set_live()
            anims.append(MoveToTarget(automata_cell.box))
        self.play(*anims)
        
        anims = []
        for h in horizontal:
            automata_cell = grid[mid_y+h][mid_x]
            automata_cell.set_died()
            anims.append(MoveToTarget(automata_cell.box))
        self.play(*anims)
        
        # vertical
        anims = []
        for v in horizontal:
            automata_cell = grid[mid_y][mid_x+v]
            automata_cell.set_live()
            anims.append(MoveToTarget(automata_cell.box))
        self.play(*anims)
        
        anims = []
        for v in horizontal:
            automata_cell = grid[mid_y][mid_x+v]
            automata_cell.set_died()
            anims.append(MoveToTarget(automata_cell.box))
        self.play(*anims)
        
        # diag
        dx = [1, -1, 1, -1] 
        dy = [1, -1, -1, 1]
        anims = []
        for d in range(len(dx)):
            automata_cell = grid[mid_y+dy[d]][mid_x+dx[d]]
            automata_cell.set_live()
            anims.append(MoveToTarget(automata_cell.box))
        self.play(*anims)
        
        anims = []
        for d in range(len(dx)):
            automata_cell = grid[mid_y+dy[d]][mid_x+dx[d]]
            automata_cell.set_died()
            anims.append(MoveToTarget(automata_cell.box))
        self.play(*anims)
        
        # Check the rules
        # Rule 1: Any live cell with fewer than two live neighbours dies, as if by underpopulation.
        automata_cell = grid[mid_y+1][mid_x+1]
        automata_cell.set_live()
        self.play(MoveToTarget(automata_cell.box))
        
        self.wait()
        
        automata_cell = grid[mid_y][mid_x]
        automata_cell.set_died()
        self.play(MoveToTarget(automata_cell.box))
        
        self.wait()
        
        # reset
        automata_cell = grid[mid_y+1][mid_x+1]
        automata_cell.set_died()
        self.play(MoveToTarget(automata_cell.box))
        
        automata_cell = grid[mid_y][mid_x]
        automata_cell.set_live()
        self.play(MoveToTarget(automata_cell.box))
        
        # Rule 2: Any live cell with two or three live neighbours lives on to the next generation.
        anims = []
        npy = [-1, -1] # neighbor position on y
        npx = [-1, 1] # neighbor position on x
        for i in range(len(npy)):
            automata_cell = grid[mid_y+npy[i]][mid_x+npx[i]]
            automata_cell.set_live()
            anims.append(MoveToTarget(automata_cell.box))
        self.play(*anims)
        
        self.wait()
        
        # reset
        anims = []
        npy = [-1, -1] # neighbor position on y
        npx = [-1, 1] # neighbor position on x
        for i in range(len(npy)):
            automata_cell = grid[mid_y+npy[i]][mid_x+npx[i]]
            automata_cell.set_died()
            anims.append(MoveToTarget(automata_cell.box))
        self.play(*anims)
        
        # Rule 3: Any live cell with more than three live neighbours dies, as if by overpopulation.
        anims = []
        npy = [0, -1, 1, -1] # neighbor position on y
        npx = [1, 0, 1, -1] # neighbor position on x
        for i in range(len(npy)):
            automata_cell = grid[mid_y+npy[i]][mid_x+npx[i]]
            automata_cell.set_live()
            anims.append(MoveToTarget(automata_cell.box))
        self.play(*anims)
        
        self.wait()
        
        automata_cell = grid[mid_y][mid_x]
        automata_cell.set_died()
        self.play(MoveToTarget(automata_cell.box))
        
        self.wait()
        
        # reset
        anims = []
        for i in range(len(npy)):
            automata_cell = grid[mid_y+npy[i]][mid_x+npx[i]]
            automata_cell.set_died()
            anims.append(MoveToTarget(automata_cell.box))
        self.play(*anims)
        
        # Rule 4: Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
        anims = []
        npy = [0, -1, 1] # neighbor position on y
        npx = [1, 0, -1] # neighbor position on x
        
        for i in range(len(npy)):
            automata_cell = grid[mid_y+npy[i]][mid_x+npx[i]]
            automata_cell.set_live()
            anims.append(MoveToTarget(automata_cell.box))
        self.play(*anims)
        
        self.wait()
        
        automata_cell = grid[mid_y][mid_x]
        automata_cell.set_live()
        self.play(MoveToTarget(automata_cell.box))
        
        self.wait()
        
        # reset
        anims = []
        for i in range(len(npy)):
            automata_cell = grid[mid_y+npy[i]][mid_x+npx[i]]
            automata_cell.set_died()
            anims.append(MoveToTarget(automata_cell.box))
        self.play(*anims)
        
        # Pattern Examples
        # Penta - decathlon pattern init
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
            automata_cell.set_is_live()
            anims.append(MoveToTarget(automata_cell.box))

        self.play(*anims)
        self.wait()
        
        
        moves_x = [1, -1, 0, 0, -1, -1, 1, 1]
        moves_y = [0, 0, 1, -1, 1, -1, -1, 1]
        
        n = len(grid)
        m = len(grid[0])
        number_of_iterations = 30
        while(number_of_iterations > 0):
            change_vals = []
            number_of_iterations -= 1
            for i in range(1,n):
                for j in range(1,m):
                    tot_neighbors = 0
                    for k in range(len(moves_x)):
                        if(i+moves_y[k] >= 1 and i+moves_y[k] < n and j+moves_x[k] >= 1 and j+moves_x[k] < m and grid[i+moves_y[k]][j+moves_x[k]].get_is_live()==1):
                            tot_neighbors+=1
                    if(grid[i][j].get_is_live() == 1):
                        if(tot_neighbors < 2 or tot_neighbors > 3): # died for under or over pop
                            change_vals.append((i,j,0))
                    else:
                        if(tot_neighbors == 3): # reproduction
                            change_vals.append((i,j,1))
            # apply animation
            anims = []
            for c in change_vals:
                automata_cell = grid[c[0]][c[1]]
                automata_cell.set_is_live()
                if(c[2] == 1):
                    automata_cell.set_live()
                else:
                    automata_cell.set_died()
                anims.append(MoveToTarget(automata_cell.box))
            self.play(*anims, run_time=0.4)
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