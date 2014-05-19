import pygame, sys
from pygame.locals import *

# --- Functions ---
def distance(speed, time):
    distance = time * speed
    return distance

# --- Classes ---

# --- Set up ---
pygame.init()

windowSurface = pygame.display.set_mode((1216, 768), 0, 32) #always 0 and 32
pygame.display.set_caption('Lanceloet van Denemerken')

basicFont = pygame.font.SysFont(None, 23)

mainClock = pygame.time.Clock()

# --- Other variables ---
showDebug = True

loopTrack = 0

# --- Constants ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# --- Objects ---

# --- Image & music Loading --- 
directionList = [pygame.image.load('up.png'), pygame.image.load('left.png'), pygame.image.load('down.png'), pygame.image.load('right.png')]

player = directionList[0]

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
    
    windowSurface.blit(player, (100, 100))

    # --- movement ---
    if pygame.key.get_pressed()[119]:
        player = directionList[0]
    elif pygame.key.get_pressed()[97]:
        player = directionList[1]
    elif pygame.key.get_pressed()[115]:
        player = directionList[2]
    elif pygame.key.get_pressed()[100]:
        player = directionList[3]

    # --- Tile visualisation ---
    for i in range(0, 12):
        for j in range(0, 19):
            pygame.draw.rect(windowSurface, BLUE, (i * 64, j * 64, i * 64, j * 64), 1)
    
    # --- Debug ---
    if showDebug == True:
        debug = "string"
        debugText = basicFont.render(str(debug), True, YELLOW) #text | antialiasing | color
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




