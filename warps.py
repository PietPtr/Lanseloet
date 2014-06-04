import pygame, sys
from pygame.locals import *

#chamber1 = raw_input("First Chamber ID: ")
#chamber2 = raw_input("Second Chamber ID: ")

chamber1 = 0
chamber2 = 1

chamber1 = pygame.transform.scale(pygame.image.load("resources/chamber" + str(chamber1) + ".png"), (1216, 768))
chamber2 = pygame.transform.scale(pygame.image.load("resources/chamber" + str(chamber2) + ".png"), (1216, 768))

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

chamber = 'first'

# --- Constants ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# --- Objects ---

# --- Image & music Loading --- 


# --- Main loop ---
while True:
    frameTime = mainClock.tick(1000)
    FPS = mainClock.get_fps()
    currentTime = pygame.time.get_ticks()
    mousePosition = pygame.mouse.get_pos()
    loopTrack = loopTrack + 1

    windowSurface.fill(BLACK)
    if chamber == 'first':
        windowSurface.blit(chamber1, (0, 0))
    elif chamber == 'second':
        windowSurface.blit(chamber2, (0, 0))
    
    if showDebug == True:
        debug = True
        debugText = basicFont.render(str(debug), True, YELLOW) #text | antialiasing | color
        windowSurface.blit(debugText, (1, 1))

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == KEYUP:
            if event.key == 284:
                showDebug = not showDebug
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                chamber = "second"
                warpPos1 = [(mousePosition[0] - (mousePosition[0] % 64)) / 64, (mousePosition[1] - (mousePosition[1] % 64)) / 64]
                print warpPos1
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
