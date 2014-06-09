"""
Codes for tiles:
0: Important tile like floor/wall
1: Furniture
2: Stuff on the wall (Window, torch)
3: Garden tiles
4: 
5: Carpet
6: Paintings
"""
import pygame, sys, os, random
from pygame.locals import *

whatChamber = raw_input("What picture do you want to load? ")
if whatChamber == "":
    whatChamber = "default.png"
else:
    whatChamber = whatChamber + ".png"

# --- Functions ---
def distance(speed, time):
    distance = time * speed
    return distance

# --- Classes ---
class ChamberTile(object):
    def __init__(self, position, picture):
        self.isActive = False
        self.position = position
        self.picture = picture
    def update(self):
        tileSurface.blit(self.picture,(self.position[0], self.position[1]))
        
# --- Set up ---
pygame.init()

windowSurface = pygame.display.set_mode((608, 420 + 64), 0, 32) #always 0 and 32
tileSurface = pygame.Surface((608, 384), 0, 32)
pygame.display.set_caption('Chamber Creator')

basicFont = pygame.font.SysFont(None, 23)

mainClock = pygame.time.Clock()

# --- Other variables ---
showDebug = True
screenshot = False
screenshotOverride = False

loopTrack = 0

activeTile = 0

chamber = []
for y in range(0, 12):
    chamber.append([])
    for x in range(0, 19):
        chamber[y].append(None)

tiles = []

tileMaps = []
for y in range(0, 24):
    tileMaps.append([])
    for x in range(0, 19):
        tileMaps[y].append(None)

# --- Constants ---
BLACK = (0, 0, 0)
WHITE = (225, 225, 225)
RED = (100, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


# --- Image & music Loading --- 
path = os.path.abspath("tiles")
for tile in os.listdir(path):
    tiles.append(pygame.image.load("tiles/" + tile))

defaultChamber = pygame.image.load(whatChamber)
tileSurface.blit(defaultChamber, (0, 0))

# --- Main loop ---
while True:
    frameTime = mainClock.tick(1000)
    FPS = mainClock.get_fps()
    currentTime = pygame.time.get_ticks()
    mousePosition = pygame.mouse.get_pos()
    loopTrack = loopTrack + 1

    windowSurface.fill(WHITE)
    
    pygame.draw.rect(windowSurface, RED, (0, 384, 608, 4))

    if pygame.mouse.get_pressed()[0] and mousePosition[1] < 384:
        chamber[(mousePosition[1] - (mousePosition[1] % 32)) / 32][(mousePosition[0] - (mousePosition[0] % 32)) / 32] = ChamberTile([(mousePosition[0] - (mousePosition[0] % 32)), (mousePosition[1] - (mousePosition[1] % 32))], tiles[activeTile])

    yTrack = 0
    for y in chamber:
        xTrack = 0
        for x in y:
            if x != None:
                x.update()
            xTrack += 1
        yTrack += 1

    windowSurface.blit(tileSurface, (0, 0))
    
    if showDebug == True:
        debug = (mousePosition[0] - (mousePosition[0] % 32)) / 32, (mousePosition[1] - (mousePosition[1] % 32)) / 32
        debugText = basicFont.render(str(debug), True, YELLOW) #text | antialiasing | color
        windowSurface.blit(debugText, (1, 1))

    activeText = basicFont.render("ACTIVE TILE:", True, BLACK)
    windowSurface.blit(activeText, (1, 420 - activeText.get_size()[1] - 1))

    for event in pygame.event.get():
        if event.type == KEYUP:
            if event.key == 284:
                showDebug = not showDebug
            if event.key == 282:
                screenshot = True
            if event.key == 293:
                screenshotOverride = True
            if event.key == 275:
                tiles[activeTile] = pygame.transform.rotate(tiles[activeTile], 90)
            if event.key == 276:
                tiles[activeTile] = pygame.transform.rotate(tiles[activeTile], -90)
        if event.type == MOUSEBUTTONUP:
            if event.button == 5:
                activeTile += 1
                if activeTile >= len(tiles) - 1:
                    activeTile = len(tiles) - 1
            elif event.button == 4:
                activeTile -= 1
                if activeTile <= 0:
                    activeTile = 0
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    windowSurface.blit(tiles[activeTile], (107, 420 - 32))

    if screenshot == True:
        screenshot = False
        for x in range(0, 65536):
            if os.path.exists("room" + str(x) + ".png") == True:
                next
            elif os.path.exists("room" + str(x) + ".png") == False:
                pygame.image.save(tileSurface, "room" + str(x) + ".png")
                break
    elif screenshotOverride:
        pygame.image.save(tileSurface, whatChamber)

    pygame.display.update()
