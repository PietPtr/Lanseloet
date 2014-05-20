"""
TODO:

Footsteps

Create script interpreter
- Should be able to understand commands from a text file
    - available commands should be:
        - walk <dir> <amount>    |
        - playsound <soundname>  |
        - say <text>             | subtitles?
Read maps from textFile
- should be able to read warps to/from coordinates.
    - Example:
        chamber1.png
        warp,12,0,chamber0,2     | Warp at x: 12, y:0 to warp 1 in chamber0 map. If player stands on the warp it will be teleported to the warp ID in the room

"""
import pygame, sys, os
from pygame.locals import *

# --- Functions ---
def distance(speed, time):
    distance = time * speed
    return distance

def changeGameState(newState):
    global GameState
    GameState = newState

# --- Classes ---
class Character(object):
    def __init__(self, position, direction, spriteList):
        self.position = position
        self.direction = direction
        self.spriteList = spriteList
        self.nextPosition = [self.position[0], self.position[1]]
        self.animationRunning = False
    def move(self, direction):
        self.direction = direction
        if self.animationRunning == False:
            if self.direction == 0:
                self.nextPosition[1] = self.nextPosition[1] - 64
            elif self.direction == 1:
                self.nextPosition[0] = self.nextPosition[0] - 64
            elif self.direction == 2:
                self.nextPosition[1] = self.nextPosition[1] + 64
            elif self.direction == 3:
                self.nextPosition[0] = self.nextPosition[0] + 64
    def updateAnimation(self):
        if self.position[0] != self.nextPosition[0]:
            if self.position[0] < self.nextPosition[0]:
                self.position[0] += int(distance(0.5, frameTime))
            elif self.position[0] > self.nextPosition[0]:
                self.position[0] -= int(distance(0.5, frameTime))
            self.animationRunning = True
        if self.position[1] != self.nextPosition[1]:
            if self.position[1] < self.nextPosition[1]:
                self.position[1] += int(distance(0.5, frameTime))
            elif self.position[1] > self.nextPosition[1]:
                self.position[1] -= int(distance(0.5, frameTime))
            self.animationRunning = True
        if self.position[1] == self.nextPosition[1] and self.position[0] == self.nextPosition[0]:
            self.animationRunning = False
    def update(self):
        # --- Checks if position is valid, and blits to windowSurface ---
        if self.nextPosition[0] > 64 * 18:
            self.nextPosition[0] = 64 * 18
        elif self.nextPosition[0] < 0:
            self.nextPosition[0] = 0
        if self.nextPosition[1] > 64 * 11:
            self.nextPosition[1] = 64 * 11
        elif self.nextPosition[1] < 0:
            self.nextPosition[1] = 0
    
        windowSurface.blit(self.spriteList[self.direction], (self.position[0], self.position[1]))

class Button(object):
    def __init__(self, position, text, function):   
        self.position = position
        self.text = text
        self.function = function
        self.image = [pygame.image.load('button.png'), pygame.image.load('buttonH.png')]
        self.hovering = False
    def doTasks(self):
        global clicked
        if self.hovering == False:
            windowSurface.blit(self.image[0], (self.position[0], self.position[1]))
        elif self.hovering == True:
            windowSurface.blit(self.image[1], (self.position[0], self.position[1]))
        
        buttonText = basicFont.render(str(self.text), False, GREEN)
        buttonTextSize = buttonText.get_size()
        windowSurface.blit(buttonText, (self.position[0] + (100 - (buttonTextSize[0] / 2)), self.position[1] + (50 - (buttonTextSize[1] / 2))))

        if mousePosition[0] > self.position[0] and mousePosition[0] < self.position[0] + 200 and mousePosition[1] > self.position[1] and mousePosition[1] < self.position[1] + 100: #Button is 200x100 px
            self.hovering = True
        else:
            self.hovering = False

        if self.hovering == True and clicked == True:
            clicked = False
            self.function()
            return True
        else:
            return False
    
# --- Set up ---
pygame.init()

windowSurface = pygame.display.set_mode((1216, 768), 0, 32) #always 0 and 32
pygame.display.set_caption('Lanceloet van Denemerken')

basicFont = pygame.font.SysFont("palatinolinotype", 23)

mainClock = pygame.time.Clock()

# --- Other variables ---
showDebug = True

loopTrack = 0

playerPos = [0, 0]
nextPlayerPos = [0, 0]

lastPress = 0

clicked = False
screenshot = False

# --- Constants ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

"""GameState system"""
MENU = 0
CUTSCENE = 1
SEARCHPLAY = 2
RUNPLAY = 3
PAUSE = 4
GameState = 0

# --- Image & music Loading --- 
directionList = [pygame.image.load('up.png'),
                 pygame.image.load('left.png'),
                 pygame.image.load('down.png'),
                 pygame.image.load('right.png'),
                 pygame.image.load('upl.png'),
                 pygame.image.load('leftl.png'),
                 pygame.image.load('downl.png'),
                 pygame.image.load('rightl.png'),
                 pygame.image.load('upr.png'),
                 pygame.image.load('leftr.png'),
                 pygame.image.load('downr.png'),
                 pygame.image.load('rightr.png')] 

picScaleTrack = 0
for picture in directionList:
    directionList[picScaleTrack] = pygame.transform.scale(picture, (64, 64))
    picScaleTrack += 1

player = directionList[5]

tile = pygame.image.load('tile.png')

menuBg = pygame.image.load('background.png')

# --- Objects ---
playerChar = Character([0, 0], 0, directionList)

B_start = Button([64, 64], "RESUME", lambda:changeGameState(SEARCHPLAY))

# --- Main loop ---
while True:
    # --- Variables outside gamestate ---
    frameTime = mainClock.tick(1000)
    FPS = mainClock.get_fps()
    currentTime = pygame.time.get_ticks()
    mousePosition = pygame.mouse.get_pos()
    loopTrack = loopTrack + 1
    
    # --- Events --- 
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == KEYUP:
            if event.key == 284:
                showDebug = not showDebug
            elif event.key == 283:
                screenshot = True
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                clicked = True
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    # ----- Gamestates -----
    if GameState == MENU:
        windowSurface.blit(menuBg, (0, 0))
        B_start.doTasks()
        
    if GameState == PAUSE:
        pass
    if GameState == SEARCHPLAY:
        # --- first blit/fill --- 
        windowSurface.fill(GREEN)

        playerChar.updateAnimation()
        playerChar.update()

        # --- Movement ---
        if pygame.key.get_pressed()[119] and pygame.time.get_ticks() - lastPress >= 100:
            playerChar.move(0)
        elif pygame.key.get_pressed()[97] and pygame.time.get_ticks() - lastPress >= 100:
            playerChar.move(1)
        elif pygame.key.get_pressed()[115] and pygame.time.get_ticks() - lastPress >= 100:
            playerChar.move(2)
        elif pygame.key.get_pressed()[100] and pygame.time.get_ticks() - lastPress >= 100:
            playerChar.move(3)
        if (pygame.key.get_pressed()[119] or pygame.key.get_pressed()[97] or pygame.key.get_pressed()[115] or pygame.key.get_pressed()[100]) and pygame.time.get_ticks() - lastPress >= 100:
            lastPress = pygame.time.get_ticks() 

        # --- Tile visualisation ---
        for y in range(-1, 12):
            for x in range(-1, 19):
                windowSurface.blit(tile, (x * 64, y * 64))
            
        
    # --- Debug ---
    if showDebug == True:
        debug = True
        debugText = basicFont.render(str(debug), True, RED) #text | antialiasing | color
        windowSurface.blit(debugText, (1, 1))

    # --- Run outside GameState system ---
    """"Reset variables"""
    clicked = False

    """Screenshot"""
    if screenshot == True:
        screenshot = False
        for x in range(0, 65536):
            if os.path.exists("screenshot" + str(x) + ".png") == True:
                next
            elif os.path.exists("screenshot" + str(x) + ".png") == False:
                pygame.image.save(windowSurface, "screenshot" + str(x) + ".png")
                break
