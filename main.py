import pygame as pg
import sys
from win32api import GetSystemMetrics
from random import choice, randint
pg.init()

# ~~~~~~~~~~~~~~~ Setup ~~~~~~~~~~~~~~~ 
winW, winH = ((GetSystemMetrics(0)-100)//100)*100, ((GetSystemMetrics(1)-100)//100)*100
WIN = pg.display.set_mode((winW, winH))
pg.display.set_caption("Lost Aliens")
FPS = 120
clock = pg.time.Clock()
size = 50
newSize = 50
border = False 
pathSpeed = .5
alienSpeed = .1
lobby = True

# ~~~~~~~~~~~~~~~ Images ~~~~~~~~~~~~~~~
background = pg.transform.scale(pg.image.load("Sprites\\Background.png"), (winW, winH))
lobbyBackground = pg.transform.scale(pg.image.load("Sprites\\Lobby Background.png"), (winW, winH))
planet = pg.image.load("Sprites\\Planet.png").convert_alpha()
alien = pg.image.load("Sprites\\Alien.png").convert_alpha()
asteroid1 = pg.image.load("Sprites\\Asteroid1.png").convert_alpha()
asteroid2 = pg.image.load("Sprites\\Asteroid2.png").convert_alpha()

# ~~~~~~~~~~~~~~~ Sounds ~~~~~~~~~~~~~~~
pg.mixer.music.load("Sounds\\Music.wav")
pg.mixer.music.set_volume(0.2)
pg.mixer.music.play(-1)
screech1 = pg.mixer.Sound("Sounds\\Screech1.mp3")
screech2 = pg.mixer.Sound("Sounds\\Screech2.mp3")
screech3 = pg.mixer.Sound("Sounds\\Screech3.mp3")
screech4 = pg.mixer.Sound("Sounds\\Screech4.mp3")
screech5 = pg.mixer.Sound("Sounds\\Screech5.mp3")
screech6 = pg.mixer.Sound("Sounds\\Screech6.mp3")
error = pg.mixer.Sound("Sounds\\Error.wav")
error.set_volume(0.3)
enter = pg.mixer.Sound("Sounds\\Enter.wav")
enter.set_volume(0.4)
screeches = [screech1, screech2, screech3, screech4, screech5, screech6]

# ~~~~~~~~~~~~~~~ Colors ~~~~~~~~~~~~~~~
GRAY = (60, 60, 60)
BLUE = (120, 120, 255)

# ~~~~~~~~~~~~~~~ Functions ~~~~~~~~~~~~~~~
def generate():
    grid = []
    for y in range(0, winH, size):
        row = []
        for x in range(0, winW, size):
            row.append(Box(x, y, BLUE))
        grid.append(row)
    return grid

def random_asteroid(x, y):
    if not (x == lastX and y == lastY):        
        asteroids = [asteroid1, asteroid2]
        img = choice(asteroids)
        img = pg.transform.rotate(img, 90*randint(1, 4))
        return img
    else:
        return lastAsteroid

def get_path():
    global pathLen
    path = []
    maxStep = 0
    for yI, row in enumerate(grid):
        for xI, box in enumerate(row):
            if box.type == "goal" and box.move != "":
                maxStep = box.move
                i = box.y//size
                j = box.x//size
            if box.move == 0:
                firstPath = (yI, xI)

    pathLen = maxStep
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

    path.append(firstPath)
    return path

def color_path(path):
    for coordinates in path:
        for row in grid:
            for box in row:
                if box.x//size == coordinates[1] and box.y//size == coordinates[0]:
                    r = 255 - int((box.move/pathLen)*135)
                    g = 120 + int((box.move/pathLen)*135)                    
                    box.type = "path"
                    box.color = (r, g, 120)


def draw_alien():
    global screeched
    path.reverse()
    
    for coordinates in path:
        for row in grid:
            for box in row:
                if box.x//size == coordinates[1] and box.y//size == coordinates[0]:
                    if box.move == int(alienStep):
                        WIN.blit(alien, (box.x, box.y))
                        if coordinates == path[-1]:

                            # Play sound effect
                            if not screeched:
                                choice(screeches).play()
                                screeched = True
                            return False
                            
    return True
                    

def draw_grid():
    for row in grid:
        for box in row:
            pg.draw.rect(WIN, GRAY, (box.x, box.y, size, size), 1)

def draw_lobby():
    WIN.blit(lobbyBackground, (0, 0))        

def draw():
    global moveAlien, alienStep, alienStep
    WIN.blit(background, (0, 0)) 
    if pathStep != 0:
        moveAlien = True

    for row in grid:
        for box in row:
            if not begin:
                if box.type != "":
                    WIN.blit(box.color, (box.x, box.y))
         
            else:
                if box.type != "":
                    # Draw path
                    if box.type == "path":
                        
                        if box.move < pathStep:
                            pg.draw.rect(WIN, box.color, (box.x, box.y, size, size))
                        else:
                            moveAlien = False
                    else:
                        WIN.blit(box.color, (box.x, box.y))

                    if box.type == "path" and alienStep == 0:     
                        for coordinates in path:
                            if coordinates == path[-1]:
                                WIN.blit(alien, (coordinates[1]*size, coordinates[0]*size))

    if moveAlien:
        if draw_alien():
            alienStep += alienSpeed

    if border:
        draw_grid()

    
def reset():
    global begin, stop, moveAlien, hasStart, hasGoal, screeched, step, pathStep, alienStep, grid, planet, alien, asteroid1, asteroid2
    begin = False
    stop = False
    moveAlien = False
    hasStart = False
    hasGoal = False
    screeched = False
    step = 0
    pathStep = 0
    alienStep = 0
    grid = generate()

    # Resize images
    planet = pg.transform.scale(planet, (size, size))
    alien = pg.transform.scale(alien, (size, size))
    asteroid1 = pg.transform.scale(asteroid1, (size, size))
    asteroid2 = pg.transform.scale(asteroid2, (size, size))


# ~~~~~~~~~~~~~~~ Classes ~~~~~~~~~~~~~~~
class Box:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.type = ""
        self.move = ""

    def pathfind(self, step):
        if self.type == "" or self.type == "goal":
            i = self.y//size
            j = self.x//size            

            try: # Bottom
                if grid[i+1][j].move == step-1:
                    self.move = step
                    if self.type == "goal":
                        return True
            except IndexError:
                pass
            
            try: # Top
                if i-1 < 0:
                    raise IndexError
                if grid[i-1][j].move == step-1:
                    self.move = step
                    if self.type == "goal":
                        return True
            except IndexError:
                pass
            
            try: # Right
                if grid[i][j+1].move == step-1:
                    self.move = step
                    if self.type == "goal":
                        return True
            except IndexError:
                pass
            
            try: # Left
                if j-1 < 0:
                    raise IndexError
                if grid[i][j-1].move == step-1:
                    self.move = step
                    if self.type == "goal":
                        return True
            except IndexError:
                pass
        return False

# ~~~~~~~~~~~~~~~ Main Loop ~~~~~~~~~~~~~~~
reset()

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
                    box.color = BLUE

        # Start game
        elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE and lobby:
            lobby = False
            enter.play()
        
        # Reset grid    
        elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE and begin:
            size = newSize
            reset()
            enter.play()

        # Start pathfinding
        elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            if hasStart and hasGoal:
                begin = True
                enter.play()
            else:
                error.play()

        # Toggle border
        if event.type == pg.KEYDOWN and event.key == pg.K_b:
            if border == True:
                border = False
            else:
                border = True

        # Change sizes
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_1:
                newSize = 25
            if event.key == pg.K_2:
                newSize = 50
            if event.key == pg.K_3:
                newSize = 100

    
    if lobby:
        draw_lobby()
    else:

        # Initialize last asteroid
        try:
            lastX, lastY= hover.x, hover.y
        except NameError:
            lastX, lastY = 0, 0
        
        try:
            if type(hover.color) == tuple:
                lastAsteroid = asteroid1
            else:
                lastAsteroid = hover.color
        except NameError:
            lastAsteroid = asteroid1

        # Useful mouse info
        mosX, mosY = pg.mouse.get_pos()
        hover = grid[mosY//size][mosX//size]
        mosL, mosM, mosR, mos4, mos5 = pg.mouse.get_pressed(num_buttons=5)
        keys = pg.key.get_pressed()
        
        if not begin:
            # Update box states
            if mosL:
                hover.type = "wall"
                hover.color = random_asteroid(hover.x, hover.y)
                hover.move = ""
            elif mos5 or keys[pg.K_q]:
                hover.type = "goal"
                hover.color = planet
                hover.move = ""
            elif mosR:
                hover.type = ""
                hover.color = BLUE
                hover.move = ""
            elif mos4 or keys[pg.K_e]:
                hasStart = False
                for row in grid:
                    for box in row:
                        if box.type == "start":
                            hasStart = True
                if not hasStart:
                    hover.type = "start"
                    hover.color = alien
                    hover.move = 0
            
            hasGoal = False
            for row in grid:
                for box in row:
                    if box.type == "goal":
                        hasGoal = True
        
        # Start path finding 
        if begin and not stop:
            step += 1
            step = round(step, 1)
            if step % 1 == 0:
                step = int(step)

                for row in grid:
                    for box in row:
                        if box.move == "":
                            if box.pathfind(step):
                                stop = True

        draw()

    if stop:
        pathStep += pathSpeed
        path = get_path()[:-1]
        color_path(path)    

    pg.display.update()