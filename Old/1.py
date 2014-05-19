import pygame, sys
from pygame.locals import *

# --- Functions ---
def distance(speed, time):
    distance = time * speed
    return distance

def keyDownRemove(item):
    global keyDown
    for key in keyDown:
        if key == item:
            keyDown.remove(key)

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

playerPos = [0, 0]

keyDown = []

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
directionList = [pygame.image.load('up.png'), pygame.image.load('left.png'), pygame.image.load('down.png'), pygame.image.load('right.png')]

picScaleTrack = 0
for picture in directionList:
    directionList[picScaleTrack] = pygame.transform.scale(picture, (64, 64))
    picScaleTrack += 1

print directionList[0]

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
    windowSurface.fill(GREEN)
    
    windowSurface.blit(player, (playerPos[0] * 64, playerPos[1] * 64))

    # --- movement ---
    if 119 in keyDown and pygame.time.get_ticks() - lastPress >= 100:
        player = directionList[0]
        playerPos[1] -= 1
        keyDownRemove(119)
    elif 97 in keyDown and pygame.time.get_ticks() - lastPress >= 100:
        player = directionList[1]
        playerPos[0] -= 1
        keyDownRemove(97)
    elif 115 in keyDown and pygame.time.get_ticks() - lastPress >= 100:
        player = directionList[2]
        playerPos[1] += 1
        keyDownRemove(115)
    elif 100 in keyDown and pygame.time.get_ticks() - lastPress >= 100:
        player = directionList[3]
        playerPos[0] += 1
        keyDownRemove(100)
    if True in pygame.key.get_pressed() and pygame.time.get_ticks() - lastPress >= 100:
        lastPress = pygame.time.get_ticks()

    # --- Tile visualisation ---
    for i in range(0, 12):
        for j in range(0, 19):
            #pygame.draw.rect(windowSurface, BLUE, (j * 64, i * 64 + 64, j * 64, i * 64 + 64), 1)
            pass
    
    # --- Debug ---
    if showDebug == True:
        debug = playerPos
        debugText = basicFont.render(str(debug), True, YELLOW) #text | antialiasing | color
        windowSurface.blit(debugText, (1, 1))

    # --- Events --- 
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == KEYUP:
            if event.key == 284:
                showDebug = not showDebug
        elif event.type == KEYDOWN:
            if event.key not in keyDown:
                keyDown.append(event.key)
                print keyDown
        if event.type == QUIT:
            pygame.quit()
            sys.exit()




