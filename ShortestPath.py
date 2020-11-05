import pygame
import time
import collections

'''
LIST OF CONTROLS
----------------------------
Left Mouse Click + Hold: Create Blocked Spaces
Right Mouse Click + Hold: Create Path Spaces
Middle Mouse Click: Creates the Goal
S Key + Hover on Space: Create new Start Space (Default is (0,0))
R Key: Calculates the shortest path
Spacebar: Resets the board state
[X]: Quits out of the window
'''

#Game Configurations
pygame.init()
pygame.display.set_caption("Shortest Path Finder")
WINDOW_HEIGHT = 750
WINDOW_WIDTH = 750
SCREEN = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
CLOCK = pygame.time.Clock()

#Background Color
BLACK = (0, 0, 0)
#Border Color
WHITE = (200, 200, 200)
#Goal Color
GOLD = (255,200,0)
#Correct Path Color
GREEN = (0, 200, 0)
#Considering Color
RED = (200,0,0)
#Blocker Color
BLUE = (0,0,128)

#Grid Information
BLOCK_SIZE = 25
BLOCKS_X = WINDOW_WIDTH//BLOCK_SIZE
BLOCKS_Y = WINDOW_HEIGHT//BLOCK_SIZE
GRID = []

def Shortest_Path(start):
    '''
    Calculates the shortest path through the Grid
    '''
    #Setup the start
    queue = collections.deque([[(start)]])
    seen = set([(start)])
    GRID[start[0]][start[1]] = 3

    #Begin a BFS
    while queue:
        path = queue.popleft() #Check spot
        x, y = path[-1]
        for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)): #Add adjacent spots to the queue
            if 0 <= x2 < BLOCKS_X and 0 <= y2 < BLOCKS_Y and GRID[x2][y2] != 1 and (x2, y2) not in seen:
                if GRID[x2][y2] == 2: #If end found just stop
                    for x3, y3 in path:
                        GRID[x3][y3] = 4
                    return
                queue.append(path + [(x2, y2)])
                GRID[x2][y2] = 3
                seen.add((x2, y2))
                #Show the user how it's working
                Draw_Grid()
                pygame.time.delay(10)
                pygame.display.update()            

def Create_Grid():
    '''
    Creates the initial grid to store block data
    '''
    for x in range((WINDOW_WIDTH//BLOCK_SIZE)):
        temp = []
        for y in range((WINDOW_HEIGHT//BLOCK_SIZE)):
            temp.append(0)
        GRID.append(temp)

def Box_L_Clicked(position):
    '''
    Blocker Space
    Handles Left Clicking on the Grid
    '''
    x = (position[0] // BLOCK_SIZE)
    y = (position[1] // BLOCK_SIZE)
    GRID[x][y] = 1

def Box_M_Clicked(position):
    '''
    Goal Space
    Handles Middle Clicking on the Grid
    '''
    x = (position[0] // BLOCK_SIZE)
    y = (position[1] // BLOCK_SIZE)
    GRID[x][y] = 2

def Box_R_Clicked(position):
    '''
    Path Space
    Handles Right Clicking on the Grid
    '''
    x = (position[0] // BLOCK_SIZE)
    y = (position[1] // BLOCK_SIZE)
    GRID[x][y] = 0

def Box_Start(position):
    '''
    Start Space
    Handles Setting a Space on Grid
    '''
    x = (position[0] // BLOCK_SIZE)
    y = (position[1] // BLOCK_SIZE)
    GRID[x][y] = 4
    return (x, y)

def Draw_Grid():
    '''
    Draw the Grid to be navigated on screen
    '''
    SCREEN.fill(BLACK)
    for x in range((WINDOW_WIDTH//BLOCK_SIZE)):
        for y in range((WINDOW_HEIGHT//BLOCK_SIZE)):
            if GRID[x][y] == 0: #Base Blocks
                rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(SCREEN, WHITE, rect, 1)
            elif GRID[x][y] == 1: #Blockers
                rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(SCREEN, BLUE, rect, 0)
            elif GRID[x][y] == 3: #Checked
                rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(SCREEN, RED, rect, 0)
            elif GRID[x][y] == 4: #Correct Path
                rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(SCREEN, GREEN, rect, 0)
            else: #Start Position
                rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(SCREEN, GOLD, rect, 0)

if __name__ == "__main__":
    SCREEN.fill(BLACK)
    Create_Grid()
    start = (0,0)
    GRID[0][0] = 4

    while True:
        Draw_Grid()
        for event in pygame.event.get():
            #Clicking Quit on Window (Quit)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            #Space Bar Pressed (Reset Game)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                GRID = []
                Create_Grid()
                start = (0, 0)
                GRID[0][0] = 4

            #R Button Pressed (Calculates Shortest Path)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                Shortest_Path(start)

            #S Button Pressed (Set Start)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                try:
                    position = pygame.mouse.get_pos()
                    GRID[start[0]][start[1]] = 0
                    start = Box_Start(position)
                except AttributeError:
                    pass

            #Left Clcking on the Grid (Blockers)
            if pygame.mouse.get_pressed()[0]:
                try:
                    position = pygame.mouse.get_pos()
                    Box_L_Clicked(position)
                except AttributeError:
                    pass
            
            #Middle Clicking on Grid (Goal)
            if pygame.mouse.get_pressed()[1]:
                try:
                    position = pygame.mouse.get_pos()
                    Box_M_Clicked(position)
                except AttributeError:
                    pass

            #Right Clicking on the Grid (Paths)
            if pygame.mouse.get_pressed()[2]:
                try:
                    position = pygame.mouse.get_pos()
                    Box_R_Clicked(position)
                except AttributeError:
                    pass

        pygame.display.update()
