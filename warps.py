import pygame, sys, csv
from pygame.locals import *

chamber1 = raw_input("First Chamber ID: ")
chamber2 = raw_input("Second Chamber ID: ")

chamberpic1 = pygame.transform.scale(pygame.image.load("resources/chamber" + str(chamber1) + ".png"), (1216, 768))
chamberpic2 = pygame.transform.scale(pygame.image.load("resources/chamber" + str(chamber2) + ".png"), (1216, 768))

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

warpList = []

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
        windowSurface.blit(chamberpic1, (0, 0))
    elif chamber == 'second':
        windowSurface.blit(chamberpic2, (0, 0))
    
    if showDebug == True:
        try:
            debug = warpPos1, warpPos2
        except NameError:
            debug = "Undefined"

        debugText = basicFont.render(str(debug), True, YELLOW) #text | antialiasing | color
        windowSurface.blit(debugText, (1, 1))

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == KEYUP:
            if event.key == 284:
                showDebug = not showDebug
            if event.key == 13:
                if chamber == "second":
                    with open(str(chamber1) + '.txt', 'wb') as scriptFile:
                        scriptWriter = csv.writer(scriptFile, delimiter=' ')
                        for warp in warpList:
                            print warp
                            scriptWriter.writerow(['warp|' + str(warp[0][0]) + '|' + str(warp[0][1]) + '|' + str(warp[1][0]) + '|' + str(warp[1][1]) + '|' + str(chamber2)])
                    chamber = 'first'

        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                if chamber == 'first':
                    chamber = 'second'
                    warpPos1 = [(mousePosition[0] - (mousePosition[0] % 64)) / 64, (mousePosition[1] - (mousePosition[1] % 64)) / 64]
                    print warpPos1
                elif chamber == 'second':
                    warpPos2 = [(mousePosition[0] - (mousePosition[0] % 64)) / 64, (mousePosition[1] - (mousePosition[1] % 64)) / 64]
                    print warpPos2
                    warpList.append([warpPos1, warpPos2])
                
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


















