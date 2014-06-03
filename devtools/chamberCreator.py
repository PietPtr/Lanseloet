import pygame, sys, os, random
from pygame.locals import *

# --- Functions ---
def distance(speed, time):
    distance = time * speed
    return distance

class Tile(object):
    def __init__(self, position, picture, inChamber):
        self.isActive = False
        self.position = position
        self.picture = picture
        self.inChamber = inChamber
    def update(self):
        if self.inChamber == False
            windowSurface.blit(self.picture)
        else:
            tileSurface.blit(self.picture)

# --- Classes ---

# --- Set up ---
pygame.init()

windowSurface = pygame.display.set_mode((608, 896), 0, 32) #always 0 and 32
tileSurface = pygame.Surface((608, 384), 0, 32)
pygame.display.set_caption('Chamber Creator')

basicFont = pygame.font.SysFont(None, 23)

mainClock = pygame.time.Clock()

# --- Other variables ---
showDebug = False
screenshot = True

loopTrack = 0

chamber = []
for y in range(0, 12):
    chamber.append([])
    for x in range(0, 19):
        chamber[y].append(None)

tiles = []
for maxTile in range(0, 99):
    tiles.append(None)

# --- Constants ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# --- Objects ---

# --- Image & music Loading --- 
path = os.path.abspath("tiles")
for tile in os.listdir(path):
    tiles[int(tile[0]) + int(tile[1])] = pygame.image.load("tiles/" + tile)

print tiles

# --- Main loop ---
while True:
    frameTime = mainClock.tick(1000)
    FPS = mainClock.get_fps()
    currentTime = pygame.time.get_ticks()
    mousePosition = pygame.mouse.get_pos()
    loopTrack = loopTrack + 1

    windowSurface.fill(WHITE)

    pygame.draw.rect(windowSurface, BLACK, (608, 0, 3, 384))

    tileTrack = 0
    for tile in tiles:
        if tile != None:
            
        tileTrack += 1

    yTrack = 0
    for y in chamber:
        xTrack = 0
        for x in y:
            if x != None:
                tileSurface.blit(x.picture, (xTrack * 32, yTrack * 32))
            xTrack += 1
        yTrack += 1

    windowSurface.blit(tileSurface, (0, 0))
    
    if showDebug == True:
        debug = "string"
        debugText = basicFont.render(str(debug), True, YELLOW) #text | antialiasing | color
        windowSurface.blit(debugText, (1, 1))

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == KEYUP:
            if event.key == 284:
                showDebug = not showDebug
            if event.key == 282:
                screenshot = True
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    if screenshot == True:
        screenshot = False
        for x in range(0, 65536):
            if os.path.exists("chamber" + str(x) + ".png") == True:
                next
            elif os.path.exists("chamber" + str(x) + ".png") == False:
                pygame.image.save(tileSurface, "chamber" + str(x) + ".png")
                break
