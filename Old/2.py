import pygame, sys
from pygame.locals import *

# --- Functions ---
def distance(speed, time):
    distance = time * speed
    return distance

# --- Classes ---
class Character(object):
    def __init__(self, position, direction, sprite):
        self.position = position
        self.direction = direction
        self.sprite = sprite
        self.nextPosition = self.position
    def move(self, direction):
        if self.direction == 0:
            self.nextPosition[1] = self.nextPosition[1] - 64
        elif self.direction == 1:
            self.nextPosition[0] = self.nextPosition[0] - 64
        elif self.direction == 2:
            self.nextPosition[1] = self.nextPosition[1] + 64
        elif self.direction == 3:
            self.nextPosition[0] = self.nextPosition[0] + 64
    def updateAnimation(self):
        

# --- Set up ---
pygame.init()

windowSurface = pygame.display.set_mode((1216, 768), 0, 32) #always 0 and 32
pygame.display.set_caption('Lanceloet van Denemerken')

basicFont = pygame.font.SysFont(None, 23)

mainClock = pygame.time.Clock()

# --- Other variables ---
showDebug = True

loopTrack = 0

playerPos = [0, 0]
nextPlayerPos = [0, 0]

lastPress = 0

# --- Constants ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# --- Objects ---

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

# --- Main loop ---
while True:
    # --- Variables outside gamestate ---
    frameTime = mainClock.tick(1000)
    FPS = mainClock.get_fps()
    currentTime = pygame.time.get_ticks()
    mousePosition = pygame.mouse.get_pos()
    loopTrack = loopTrack + 1

    # --- first blit/fill --- 
    windowSurface.fill(WHITE)
    
    windowSurface.blit(player, (playerPos[0], playerPos[1]))

    # --- Movement ---
    if pygame.key.get_pressed()[119] and pygame.time.get_ticks() - lastPress >= 100:
        player = directionList[0]
        nextPlayerPos[1] -= 64
    elif pygame.key.get_pressed()[97] and pygame.time.get_ticks() - lastPress >= 100:
        player = directionList[1]
        nextPlayerPos[0] -= 64
    elif pygame.key.get_pressed()[115] and pygame.time.get_ticks() - lastPress >= 100:
        player = directionList[2]
        nextPlayerPos[1] += 64
    elif pygame.key.get_pressed()[100] and pygame.time.get_ticks() - lastPress >= 100:
        player = directionList[3]
        nextPlayerPos[0] += 64
    if (pygame.key.get_pressed()[119] or pygame.key.get_pressed()[97] or pygame.key.get_pressed()[115] or pygame.key.get_pressed()[100]) and pygame.time.get_ticks() - lastPress >= 100:
        lastPress = pygame.time.get_ticks()

    # --- Animation ---
    if playerPos[0] != nextPlayerPos[0]:
        if playerPos[0] < nextPlayerPos[0]:
            playerPos[0] += distance(1, frameTime)
        elif playerPos[0] > nextPlayerPos[0]:
            playerPos[0] -= distance(1, frameTime)
    if playerPos[1] != nextPlayerPos[1]:
        if playerPos[1] < nextPlayerPos[1]:
            playerPos[1] += distance(1, frameTime)
        elif playerPos[1] > nextPlayerPos[1]:
            playerPos[1] -= distance(1, frameTime)
            

    # --- Tile visualisation ---
    for y in range(-1, 12):
        for x in range(-1, 19):
            windowSurface.blit(tile, (x * 64, y * 64))
            
        
    # --- Debug ---
    if showDebug == True:
        debug = nextPlayerPos
        debugText = basicFont.render(str(debug), True, RED) #text | antialiasing | color
        windowSurface.blit(debugText, (1, 1))

    # --- Events --- 
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == KEYUP:
            if event.key == 284:
                showDebug = not showDebug
        if event.type == QUIT:
            pygame.quit()
            sys.exit()




