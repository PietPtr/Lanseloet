import pygame, sys, pickle, csv
from pygame.locals import *

mapimageloading = raw_input("chamber ID: ")
mapimageloading = 'chamber' + mapimageloading

# --- Functions ---
def distance(speed, time):
    distance = time * speed
    return distance

# --- Classes ---

# --- Set up ---
pygame.init()

windowSurface = pygame.display.set_mode((1216, 768), 0, 32) #always 0 and 32
pygame.display.set_caption('NAME')

basicFont = pygame.font.SysFont(None, 23)

mainClock = pygame.time.Clock()

# --- Other variables ---
showDebug = True

loopTrack = 0

mapname = pygame.transform.scale(pygame.image.load("resources/" + mapimageloading + '.png'), (1216, 768))

script = ['pic|' + mapimageloading + '.png']

mode = "walls"

# --- Constants ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# --- Objects ---

# --- Image & music Loading --- 
tile = pygame.image.load('resources/TILE.png')
tileC = pygame.image.load('resources/TILEC.png')

# --- Main loop ---
while True:
    frameTime = mainClock.tick(1000)
    FPS = mainClock.get_fps()
    currentTime = pygame.time.get_ticks()
    mousePosition = pygame.mouse.get_pos()
    loopTrack = loopTrack + 1

    windowSurface.blit(mapname, (0, 0))

    for y in range(-1, 12):
        for x in range(-1, 19):
            windowSurface.blit(tile, (x * 64, y * 64))

    if pygame.mouse.get_pressed()[0] and mode == 'walls':
        coords = [(mousePosition[0] - ((mousePosition[0]) % 64)) / 64, (mousePosition[1] - ((mousePosition[1]) % 64)) / 64]
        if 'wall|' + str(coords[0]) + '|' + str(coords[1]) not in script:
            script.append('wall|' + str(coords[0]) + '|' + str(coords[1]))
    
    if showDebug == True:
        debug = mode
        debugText = basicFont.render(str(debug), True, YELLOW) #text | antialiasing | color
        windowSurface.blit(debugText, (1, 1))

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == KEYUP:
            if event.key == 284:
                showDebug = not showDebug
            if event.key == 13:
                print script
                if mode == "walls":
                    with open(mapimageloading + '.txt', 'wb') as scriptFile:
                        scriptWriter = csv.writer(scriptFile, delimiter=' ')
                        for line in script:
                            scriptWriter.writerow([line])
                
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
