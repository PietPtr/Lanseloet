import pygame, sys
from pygame.locals import *

chamber1 = raw_input("First Chamber: ")
chamber2 = raw_input("Second Chamber: ")

chamber1 = pygame.image.load("resources" + chamber1 + "png")
chamber2 = pygame.image.load("resources" + chamber2 + "png")

# --- Functions ---
def distance(speed, time):
    distance = time * speed
    return distance

# --- Classes ---

# --- Set up ---
pygame.init()

windowSurface = pygame.display.set_mode((500, 400), 0, 32) #always 0 and 32
pygame.display.set_caption('NAME')

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


# --- Main loop ---
while True:
    frameTime = mainClock.tick(1000)
    FPS = mainClock.get_fps()
    currentTime = pygame.time.get_ticks()
    mousePosition = pygame.mouse.get_pos()
    loopTrack = loopTrack + 1

    windowSurface.fill(BLACK)
    
    if showDebug == True:
        debug = "string"
        debugText = basicFont.render(str(debug), True, YELLOW) #text | antialiasing | color
        windowSurface.blit(debugText, (1, 1))

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == KEYUP:
            if event.key == 284:
                showDebug = not showDebug
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
