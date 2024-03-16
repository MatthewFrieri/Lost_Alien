import pygame as pg
import sys
from win32api import GetSystemMetrics

# ~~~~~~~~~~~~~~~ Window setup ~~~~~~~~~~~~~~~ 
winW, winH = ((GetSystemMetrics(0)-100)//100)*100, ((GetSystemMetrics(1)-100)//100)*100
WIN = pg.display.set_mode((winW, winH))
pg.display.set_caption("Pathfinder")
FPS = 120
clock = pg.time.Clock()
size = 50
border = True
speed = .2


# ~~~~~~~~~~~~~~~ Colors ~~~~~~~~~~~~~~~
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (120, 120, 255)
RED = (200, 0, 0)
PURPLE = (200, 0, 200)

# ~~~~~~~~~~~~~~~ Functions ~~~~~~~~~~~~~~~
def generate(): # Create grid of box objects
    grid = []
    for y in range(0, winH, size):
        row = []
        for x in range(0, winW, size):
            row.append(Box(x, y, CYAN))
        grid.append(row)
    return grid

def draw_grid(): # Draws outlines for all boxes
    for row in grid:
        for box in row:
            pg.draw.rect(WIN, BLACK, (box.x, box.y, size, size), 1)
                
def draw(): # Draw all boxes
    WIN.fill(WHITE) 
    for row in grid:
        for box in row:
            if not begin:
                if box.type != "":
                    pg.draw.rect(WIN, box.color, (box.x, box.y, size, size))
            else:
                if box.type != "" or box.move:
                    pg.draw.rect(WIN, box.color, (box.x, box.y, size, size))

    if not begin:
        pg.draw.rect(WIN, hover.color, (hover.x, hover.y, size, size))

    if border:
        draw_grid()


def display():
    steps = []
    for row in grid:
        line = []
        for box in row:
            line.append(box.move)
        steps.append(line)
    
    for row in steps:
        print()
        for item in row:
            if item == "":
                print(".", end="")
            else:
                print(item, end="")
    
def get_path():
    path = []
    maxStep = 0
    for row in grid:
        for box in row:
            if box.type == "goal" and box.move != "":
                maxStep = box.move
                i = box.y//size
                j = box.x//size           

    while maxStep > 0:
        maxStep -= 1
        try: # Bottom
            if grid[i+1][j].move == maxStep:
                path.append((i+1, j))
                i += 1
                continue
        except IndexError:
            pass
        
        try: # Top
            if grid[i-1][j].move == maxStep:
                path.append((i-1, j))
                i -= 1
                continue
        except IndexError:
            pass

        try: # Right
            if grid[i][j+1].move == maxStep:
                path.append((i, j+1))
                j += 1
                continue
        except IndexError:
            pass

        try: # Left
            if grid[i][j-1].move == maxStep:
                path.append((i, j-1))
                j -= 1
                continue
        except IndexError:
            pass
    return path

def draw_path(path):
    for coordinates in path:
        for row in grid:
            for box in row:
                if box.x//size == coordinates[1] and box.y//size == coordinates[0]:
                    box.type = "path"
                    box.color = CYAN

def reset():
    global begin, stop, step, cancel, grid
    begin = False
    stop = False
    step = 0
    cancel = 0
    grid = generate()

def get_color(step):
    if step*2 <= 255:
        return (255-step*2, 255, 120)
    elif step*2 <= 510:
        return (0, 255-step*2+255, 120)
    else:
        return (0, 0, 120)  

# ~~~~~~~~~~~~~~~ Classes ~~~~~~~~~~~~~~~
class Box:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.type = ""
        self.move = ""

    def pathfind(self, step):
        global cancel
        if self.type == "" or self.type == "goal":
            i = self.y//size
            j = self.x//size            

            try: # Bottom
                if grid[i+1][j].move == step-1:
                    found = True
                    self.move = step
                    if self.type == "goal":
                        return True
                    self.color = get_color(step)
                        
            except IndexError:
                pass
            
            try: # Top
                if i-1 < 0:
                    raise IndexError
                if grid[i-1][j].move == step-1:
                    found = True
                    self.move = step
                    if self.type == "goal":
                        return True
                    self.color = get_color(step)

            except IndexError:
                pass
            
            try: # Right
                if grid[i][j+1].move == step-1:
                    found = True
                    self.move = step
                    if self.type == "goal":
                        return True
                    self.color = get_color(step)

            except IndexError:
                pass
            
            try: # Left
                if j-1 < 0:
                    raise IndexError
                if grid[i][j-1].move == step-1:
                    found = True
                    self.move = step
                    if self.type == "goal":
                        return True
                    self.color = get_color(step)

            except IndexError:
                pass

        return False

# ~~~~~~~~~~~~~~~ Main Loop ~~~~~~~~~~~~~~~
reset()
hasStart = False
hasGoal = False
while True:
    clock.tick(FPS)
    for event in pg.event.get():
        # Check quit
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            pg.quit()
            sys.exit()
            
        # Reset boxes
        elif (event.type == pg.KEYDOWN and event.key == pg.K_c) and not begin:
            for row in grid:
                for box in row:
                    box.type = ""
                    box.color = CYAN
                    
        # Reset grid
        elif (event.type == pg.KEYDOWN and event.key == pg.K_SPACE) and begin:
            reset()

        # Start pathfinding
        elif (event.type == pg.KEYDOWN and event.key == pg.K_SPACE) and hasStart and hasGoal:
            begin = True

        # Toggle border
        if event.type == pg.KEYDOWN and event.key == pg.K_b:
            if border:
                border = False
            else:
                border = True
            
    # Useful mouse info
    mosX, mosY = pg.mouse.get_pos()
    hover = grid[mosY//size][mosX//size]
    mosL, mosM, mosR, mos4, mos5 = pg.mouse.get_pressed(num_buttons=5)
    keys = pg.key.get_pressed()

    if not begin:
        # Update box states
        if mosL:
            hover.type = "wall"
            hover.color = BLACK
            hover.move = ""
        elif mos5 or keys[pg.K_q]:
            hover.type = "goal"
            hover.color = PURPLE
            hover.move = ""
        elif mosR:
            hover.type = ""
            hover.color = CYAN
            hover.move = ""
        elif mos4 or keys[pg.K_e]:
            hasStart = False
            for row in grid:
                for box in row:
                    if box.type == "start":
                        hasStart = True
            if not hasStart:
                hover.type = "start"
                hover.color = RED
                hover.move = 0
        
        hasGoal = False
        for row in grid:
            for box in row:
                if box.type == "goal":
                    hasGoal = True
    
    # Start path finding 
    if begin and not stop:
        step += speed
        step = round(step, len(str(speed)))
        if step % 1 == 0:
            step = int(step)

            for row in grid:
                for box in row:
                    if box.move == "":
                        if box.pathfind(step):
                            stop = True

    draw()

    if stop:
        path = get_path()[:-1]
        draw_path(path)
        
    pg.display.update()