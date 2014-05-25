"""
TODO:

Create script interpreter
- Should be able to understand commands from a text file
    - available commands should be:
        - walk <dir> <amount>    |
        - playsound <soundname>  |
        - say <text>             | subtitles?

pics|lanseloetup.png|lanseloetleft.png|lanseloetleft.png|lanseloetright.png
position|4|1|2|0   X:4 Y:1 direction facing: 2 (down) in chamber0
trigger|4|2        trigger tile 0 is at X:4 Y:2
trigger|3|1        trigger tile 1 is at X:3 Y:1
walk|4|3           when triggered, start with the walk command: walk 4 blocks to direction 3 (right)
                   only go to next command when the previous one is finished.
"""
import pygame, sys, os, pickle, csv
from pygame.locals import *

defaultSaveState = [[3 * 64, 1 * 64, 0], [], [], [], True]

# --- Functions ---
def distance(speed, time):
    distance = time * speed
    return distance

"""font"""
def loadFont():
    global alphabetPictures
    path = os.path.abspath("font")
    for picture in os.listdir(path):
        alphabetPictures.append([pygame.image.load("font/" + picture), picture])
    
    sortedAlphabetPictures = sorted(alphabetPictures, key=lambda x: int(x[1].split('.')[0]))

    alphabetPictures = []
    
    for i in sortedAlphabetPictures:
        alphabetPictures.append(i[0])

def text(text, coords):
    global alphabetPictures
    
    outputList = []
    alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", " ", ".", ",", "?", "!"]
    index = 0
    for letter in text:
        outputList.append(alphabet.index(text[index]))
        index += 1
    #print outputList

    textLength = 0
    count = 0
    for index in outputList:
        windowSurface.blit(alphabetPictures[outputList[count]], (coords[0] + textLength, coords[1]))
        textLength = textLength + int(alphabetPictures[outputList[count]].get_size()[0])
        count += 1

def getTextLength(text):
    global letterSizeList

    textLength = 0

    outputList = []
    alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", " ", ".", ",", "?", "!"]
    count = 0
    for letter in text:
        outputList.append(alphabet.index(text[count]))
        textLength = textLength + int(letterSizeList[alphabet.index(text[count])])
        count += 1

    return textLength

"""saveState"""
def saveAll():
    global playerPos
    global showDebug
    global nextPlayerPos
    global saveState
    saveState = [[playerChar.position[0], playerChar.position[1], 0], [], [], [], showDebug]
    try:
        pickle.dump(saveState, open("sav.sav", "wb"))
        return True
    except:
        return False

def loadAll():
    global saveState
    try:
        saveState = pickle.load(open("sav.sav", "rb"))
    except IOError:
        saveState = defaultSaveState
        pickle.dump(saveState, open("sav.sav", "wb"))

def resetSaveState():
    global saveState, playerChar
    loadAll()

    saveState = defaultSaveState

    showDebug = saveState[4]
    playerChar = Character([saveState[0][0], saveState[0][1]], 0, directionList, chamberList[0], None, [])


"""Button functions"""
def newGame():
    newGame = True
    return newGame

def quitGame():
    saveAll()
    pygame.quit()
    sys.exit()
    
def changeGameState(newState):
    global GameState
    GameState = newState

def yes():
    return True

def no():
    return False

# --- Classes ---
class Chamber(object):
    def __init__(self, mapPicture, warps, events, wallList):
        self.mapPicture = mapPicture
        self.warps = warps    #list of lists: [[pos1, pos2], warpto]
        self.events = events  #list of character objects
        self.wallList = wallList    #list of coordinates
        self.i = 0
        for coordList in self.wallList:
            coordList = [coordList[0] * 64, coordList[1] * 64]
            self.wallList[self.i] = coordList
            self.i += 1

    def render(self):
        windowSurface.blit(self.mapPicture, (0, 0))
        #for event in events: blit in right pos (event is a character class)
    def walls(self, position):  #To check if a player collides with a wall
        if position in self.wallList:
            return True
        else:
            return False

class Character(object):
    def __init__(self, position, direction, spriteList, currentChamber, triggerTile, commandList):
        self.position = position
        self.direction = direction
        self.spriteList = spriteList
        self.currentChamber = currentChamber
        self.triggerTile = triggerTile
        self.commandList = commandList
        self.nextPosition = [self.position[0], self.position[1]]
        self.animationRunning = False
        self.warped = False
        
    def move(self, direction):
        self.direction = direction
        if self.animationRunning == False:
            if self.direction == 0 and self.currentChamber.walls([self.nextPosition[0], self.nextPosition[1] - 64]) == False:
                self.nextPosition[1] = self.nextPosition[1] - 64
            elif self.direction == 1 and self.currentChamber.walls([self.nextPosition[0] - 64, self.nextPosition[1]]) == False:
                self.nextPosition[0] = self.nextPosition[0] - 64
            elif self.direction == 2 and self.currentChamber.walls([self.nextPosition[0], self.nextPosition[1] + 64]) == False:
                self.nextPosition[1] = self.nextPosition[1] + 64
            elif self.direction == 3 and self.currentChamber.walls([self.nextPosition[0] + 64, self.nextPosition[1]]) == False:
                self.nextPosition[0] = self.nextPosition[0] + 64
        self.warped = False
        
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
            
    def exeCommands(self):
        print commandList
        self.commandArgs = commandList[0][0].split('|')
        if self.commandArgs[0] == "walk" and self.animationRunning == False:
            if int(self.commandArgs[2]) == 0:
                self.nextPosition[1] = self.nextPosition[1] - 64 * int(self.commandArgs[1])
            elif int(self.commandArgs[2]) == 1:
                self.nextPosition[0] = self.nextPosition[0] - 64 * int(self.commandArgs[1])
            elif int(self.commandArgs[2]) == 2:
                self.nextPosition[1] = self.nextPosition[1] + 64 * int(self.commandArgs[1])
            elif int(self.commandArgs[2]) == 3:
                self.nextPosition[0] = self.nextPosition[0] + 64 * int(self.commandArgs[1])
            del self.commandList[0]
    
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

        self.tracker = 0
        for warp in self.currentChamber.warps:
            if [self.nextPosition[0] / 64, self.nextPosition[1] / 64] == warp.position and self.warped == False:
                #play a sound: door
                self.currentChamber = chamberList[warp.destinationChamber]
                self.nextPosition[0] = chamberList[warp.destinationChamber].warps[warp.destinationID].position[0] * 64
                self.nextPosition[1] = chamberList[warp.destinationChamber].warps[warp.destinationID].position[1] * 64
                self.position[0] = self.nextPosition[0]
                self.position[1] = self.nextPosition[1]
                self.warped = True
            self.tracker += 1

        if playerChar.currentChamber == self.currentChamber:
            windowSurface.blit(self.spriteList[self.direction], (self.position[0], self.position[1]))

class Button(object):
    def __init__(self, position, text, function):
        self.position = position
        self.text = text
        self.function = function
        self.image = [pygame.image.load('resources/button.png'), pygame.image.load('resources/buttonH.png')]
        self.hovering = False
        self.size = [self.image[0].get_size()[0], self.image[0].get_size()[1]]
    def doTasks(self):
        global clicked
        if self.hovering == False:
            windowSurface.blit(self.image[0], (self.position[0], self.position[1]))
        elif self.hovering == True:
            windowSurface.blit(self.image[1], (self.position[0], self.position[1]))

        text(self.text, [(self.position[0] + (self.size[0] / 2)) - getTextLength(self.text) / 2,
                         (self.position[1] + (self.size[1] / 2)) - 45 / 2])

        if mousePosition[0] > self.position[0] and mousePosition[0] < self.position[0] + self.size[0] and mousePosition[1] > self.position[1] and mousePosition[1] < self.position[1] + self.size[1]: #Button is 200x100 px
            self.hovering = True
        else:
            self.hovering = False

        if self.hovering == True and clicked == True:
            clicked = False
            self.function()
            return True
        else:
            return False

class Warp(object):
    def __init__(self, position, destinationChamber, destinationID): #ownID = index
        self.position = position
        self.destinationChamber = destinationChamber
        self.destinationID = destinationID

# --- Set up ---
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50,40)

pygame.init()

windowSurface = pygame.display.set_mode((1216, 768), 0, 32) #always 0 and 32
pygame.display.set_caption('Lanceloet van Denemerken')

mainClock = pygame.time.Clock()

"""Fonts"""
basicFont = pygame.font.SysFont("palatinolinotype", 23)
bigFont = pygame.font.SysFont("palatinolinotype", 51)
alphabetPictures = []
loadFont()

# --- Other variables ---

#saveState = [[3, 1, 0], [], [], [], True] #position [x, y, Chamber] | Boosts | sounds played | options | debug
saveState = None
loadAll()

showDebug = saveState[4]

playerPos = [saveState[0][0], saveState[0][1]]
nextPlayerPos = [saveState[0][0], saveState[0][1]]

loopTrack = 0
lastPress = 0

clicked = False
screenshot = False

escape = False

reverseDirection = [2, 3, 0, 1]

letterSizeList = []
for picture in alphabetPictures:
    letterSizeList.append(picture.get_size()[0])

chamberList = []
eventList = []

path = os.path.abspath("scripts")
for script in os.listdir(path):
    with open('scripts/' + script, 'rb') as csvscript:
        scriptReader = csv.reader(csvscript, delimiter=' ', quotechar='"')
        scriptList = []
        if script.startswith('chamber'):
            for command in scriptReader:
                scriptList.append(command)
            mapWalls = []
            mapWarps = []
            for command in scriptList:
                comArgs = command[0].split('|')
                if comArgs[0].startswith("pic"):
                    mapImage = pygame.image.load('resources/' + comArgs[1])
                elif comArgs[0].startswith("wall"):
                    mapWalls.append([int(comArgs[1]), int(comArgs[2])])
                elif comArgs[0].startswith("warp"): #warp|0|3|1 means warp at X:0 Y:3, goes to chamber1s warp ID == INDEX
                    mapWarps.append(Warp([int(comArgs[1]), int(comArgs[2])], int(comArgs[3]), int(comArgs[4])))
                    
            chamberList.append(Chamber(mapImage, mapWarps, [], mapWalls))
        elif script.startswith('event'):
            for command in scriptReader:
                scriptList.append(command)

            commandList = []
            eventTrigger = []

            for command in scriptList:
                comArgs = command[0].split("|")
                if comArgs[0].startswith("pic"):
                    eventSpriteList = []
                    for eventPicture in comArgs:
                        if eventPicture != 'pics':
                            eventSpriteList.append(pygame.transform.scale(pygame.image.load("resources/" + eventPicture), (64, 64)))
                elif comArgs[0].startswith("position"):
                    eventPosition = [int(comArgs[1]) * 64, int(comArgs[2]) * 64]
                    eventDirection = int(comArgs[3])
                    eventChamber = chamberList[int(comArgs[4])]
                elif comArgs[0].startswith("trigger"):
                    eventTrigger.append([int(comArgs[1]) * 64, int(comArgs[2]) * 64])
                else:
                    commandList.append(command)

            eventList.append(Character(eventPosition, eventDirection, eventSpriteList, eventChamber, eventTrigger, commandList))
                
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
NEWGAME = 5
OPTIONS = 6
GameState = 0

# --- Image & music Loading --- 
directionList = [pygame.image.load('resources/up.png'),
                 pygame.image.load('resources/left.png'),
                 pygame.image.load('resources/down.png'),
                 pygame.image.load('resources/right.png'),
                 pygame.image.load('resources/upl.png'),
                 pygame.image.load('resources/leftl.png'),
                 pygame.image.load('resources/downl.png'),
                 pygame.image.load('resources/rightl.png'),
                 pygame.image.load('resources/upr.png'),
                 pygame.image.load('resources/leftr.png'),
                 pygame.image.load('resources/downr.png'),
                 pygame.image.load('resources/rightr.png')] 

picScaleTrack = 0
for picture in directionList:
    directionList[picScaleTrack] = pygame.transform.scale(picture, (64, 64))
    picScaleTrack += 1

player = directionList[5]

tile = pygame.image.load('resources/tile.png')

menuBg = pygame.image.load('resources/background.png')
pauseBg = pygame.image.load('resources/pause.png')

chamber0 = pygame.image.load('resources/chamber0.png')

# --- Objects ---
playerChar = Character([saveState[0][0], saveState[0][1]], 0, directionList, chamberList[0], None, [])

B_start = Button([720, 64], "VERDER GAEN", lambda:changeGameState(SEARCHPLAY))
B_new = Button([720, 165], "NIEWE SPEL", lambda:changeGameState(NEWGAME))
B_options = Button([720, 266], "MOGELIJCHEDE", lambda:changeGameState(OPTIONS))
B_quit = Button([720, 367], "SLUIJTEN", lambda:quitGame())

B_yes = Button([608 - 469, 367], "JA", lambda:yes())
B_no = Button([608 + 5, 367], "NEEN", lambda:no())

B_continue = Button([720, 165], "VERDER GAEN", lambda:changeGameState(SEARCHPLAY))
B_menu = Button([720, 266], "MENU", lambda:changeGameState(MENU))

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
            elif event.key == 27:
                escape = True
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                clicked = True
        if event.type == QUIT:
            saveAll()
            pygame.quit()
            sys.exit()
            
    # ----- Gamestates -----
    if GameState == MENU:
        windowSurface.blit(menuBg, (0, 0))
        if saveState != defaultSaveState:
            B_start.doTasks()
        B_new.doTasks()
        B_options.doTasks()
        B_quit.doTasks()
    if GameState == OPTIONS:
        windowSurface.blit(menuBg, (0, 0))
        B_menu.doTasks()
    if GameState == NEWGAME:
        windowSurface.blit(menuBg, (0, 0))
        if saveState != defaultSaveState:
            warningText = ["PASSET DI OP!", "ALSDU EEN NIEWE SPEL BEGHINT,", "EN WERT ALDE SPEL NIE BEWAERT.", "BISDU SEEKER?"]

            count = 0
            for warningSentence in warningText:
                text(warningText[count], [(1216 / 2) - (getTextLength(warningText[count]) / 2), 45 * count + 40])
                count += 1
            count = 0
            if B_yes.doTasks() == True:
                os.remove("sav.sav")
                resetSaveState()
                GameState = SEARCHPLAY
            elif B_no.doTasks() == True:
                GameState = MENU
        elif saveState == defaultSaveState:
            saveState = defaultSaveState
            GameState = SEARCHPLAY
    
    if GameState == PAUSE:
        windowSurface.blit(pauseBg, (0, 0))
        B_continue.doTasks()
        B_quit.doTasks()
        if B_menu.doTasks():
            saveAll()
            
    if GameState == SEARCHPLAY:
        # --- first blit/fill ---
        windowSurface.fill(BLACK)
        playerChar.currentChamber.render()

        playerChar.updateAnimation()
        playerChar.update()

        for event in eventList:
            event.updateAnimation()
            event.update()

            if playerChar.position in event.triggerTile and event.commandList != [] and reverseDirection[playerChar.direction] == event.direction:
                event.exeCommands()

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
                #windowSurface.blit(tile, (x * 64, y * 64))
                pass

        # --- Pause ---
        if escape:
            GameState = PAUSE
            escape = False
            
    # --- Debug ---
    if showDebug == True:
        debug = playerChar.nextPosition
        debugText = basicFont.render(str(debug), True, RED) #text | antialiasing | color
        windowSurface.blit(debugText, (1, 1))

    # --- Run outside GameState system ---
    """"Reset variables"""
    clicked = False

    if GameState != SEARCHPLAY:
        escape = False

    """Screenshot"""
    if screenshot == True:
        screenshot = False
        for x in range(0, 65536):
            if os.path.exists("screenshot" + str(x) + ".png") == True:
                next
            elif os.path.exists("screenshot" + str(x) + ".png") == False:
                pygame.image.save(windowSurface, "screenshot" + str(x) + ".png")
                break
