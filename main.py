"""
TODO:
    Save events and boosts...

event script example:
    pics|lanseloetup.png|lanseloetleft.png|lanseloetleft.png|lanseloetright.png
    position|4|1|2|0   X:4 Y:1 direction facing: 2 (down) in chamber0
    trigger|4|2        trigger tile 0 is at X:4 Y:2
    trigger|3|1        trigger tile 1 is at X:3 Y:1
    walk|4|3           when triggered, start with the walk command: walk 4 blocks to direction 3 (right)
                       only go to next command when the previous one is finished.

boost script example:
pic|chest.png       Picture to use
position|17|1|0     X: 17, Y: 1 in chamber0
boost|0|0.1         Boost[0] + 0.1 | [0] = speed (maxSpeed - 0.1 in this case), [1] = amount of objects (2 (50% or 1/2) default), [2] = lives
"""
from __future__ import division
import pygame, sys, os, pickle, csv, random
from pygame.locals import *

defaultSaveState = [[3 * 64, 1 * 64, 0], [2, 1, 2, 500], [], [], True] #position [x, y, Chamber] | Boosts | Events Triggered | Boosts picked up | debug

# --- Functions ---
"""saveState"""
def saveAll():
    global showDebug
    global saveState

    boostOpenedList = []
    for boost in boostList:
        boostOpenedList.append(boost.opened)

    eventTriggeredList = []
    for i in range(0, len(eventList)):
        eventTriggeredList.append(False)
        
    for event in eventList:
        if event.commandList != []:
            for command in event.commandList:
                if command == ["DONE"]:
                    eventTriggeredList[eventList.index(event)] = [True, [event.position[0], event.position[1]]]
        else:
            eventTriggeredList[eventList.index(event)] = [True, [event.position[0], event.position[1]]]

    print eventTriggeredList
            
    saveState = [[playerChar.position[0], playerChar.position[1], chamberList.index(playerChar.currentChamber)], endGameBoosts, eventTriggeredList, boostOpenedList, showDebug]
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

    for i in saveState:
        print i

def resetSaveState():
    print "resetting"
    global saveState, playerChar, endGameBoosts
    loadAll()

    saveState = defaultSaveState

    showDebug = saveState[4]
    playerChar = Character([saveState[0][0], saveState[0][1]], 0, directionList, chamberList[0], None, [])
    endGameBoosts = [saveState[1][0], saveState[1][1], saveState[1][2], saveState[1][3]]

    for boost in boostList:
        boost.opened = 0

    loadChambersAndEvents()

    saveAll()

"""Others"""
def distance(speed, time):
    distance = time * speed
    return distance

def startRunning():
    global lastSpeedUp, scoreStart, mapSlices, playerY, playerX, lives, endGameBoosts, speed
    
    lastSpeedUp = pygame.time.get_ticks()
    changeGameState(RUNPLAY, "RUN.wav")
    scoreStart = pygame.time.get_ticks()
    for i in range(0, 20):
        mapSlices.append(MapSlice(i * 128, 1))
    playerY = 300
    playerX = 128
    lives = endGameBoosts[2]
    speed = endGameBoosts[1]
    speedUp = endGameBoosts[3]
    
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
    alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", " ", ".", ",", "?", "!", ":", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    index = 0
    for letter in text:
        outputList.append(alphabet.index(text[index]))
        index += 1

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
    alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", " ", ".", ",", "?", "!", ":", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    count = 0
    for letter in text:
        outputList.append(alphabet.index(text[count]))
        textLength = textLength + int(letterSizeList[alphabet.index(text[count])])
        count += 1

    return textLength

"""Check event position"""
def getEventPosition(playerPos):
    eventAtPlayer = False
    
    for event in eventList:
        if event.currentChamber == playerChar.currentChamber:
            if event.position == playerPos:
                eventAtPlayer = True
                break
            else:
                eventAtPlayer = False

    if eventAtPlayer == False:
        for boost in boostList:
            if boost.currentChamber == playerChar.currentChamber:
                if boost.position[0] * 64 == playerPos[0] and boost.position[1] * 64 == playerPos[1]:
                    eventAtPlayer = True
                    break
                else:
                    eventAtPlayer = False

    return eventAtPlayer

"""Load from file"""
def loadChambersAndEvents():
    global chamberList, eventList

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
                triggerAvailable = False
                
                for command in scriptList:
                    comArgs = command[0].split("|")
                    if comArgs[0].startswith("pic"):
                        eventSpriteList = []
                        for eventPicture in comArgs:
                            if eventPicture != 'pics':
                                eventSpriteList.append(pygame.transform.scale(pygame.image.load("resources/" + eventPicture), (64, 128)))
                    elif comArgs[0].startswith("position"):
                        eventPosition = [int(comArgs[1]) * 64, int(comArgs[2]) * 64]
                        eventDirection = int(comArgs[3])
                        eventChamber = chamberList[int(comArgs[4])]
                    elif comArgs[0].startswith("trigger"):
                        eventTrigger.append([int(comArgs[1]) * 64, int(comArgs[2]) * 64])
                        triggerAvailable = True
                    else:
                        commandList.append(command)

                if triggerAvailable == False:
                    eventTrigger.append([eventPosition[0], eventPosition[1] + 64])

                eventList.append(Character(eventPosition, eventDirection, eventSpriteList, eventChamber, eventTrigger, commandList))


"""Button functions"""
def newGame():
    newGame = True
    return newGame

def quitGame():
    saveAll()
    pygame.quit()
    sys.exit()
    
def changeGameState(newState, song):
    global GameState
    GameState = newState
    if song != None:
        pygame.mixer.music.fadeout(100)
        pygame.mixer.music.load("sounds/" + song)
        pygame.mixer.music.play(-1, 0)

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
        self.lastCmdTime = 0
        self.waited = False
        
    def move(self, direction):
        self.direction = direction
        if self.animationRunning == False:
            if self.direction == 0 and self.currentChamber.walls([self.nextPosition[0], self.nextPosition[1] - 64]) == False and getEventPosition([self.nextPosition[0], self.nextPosition[1] - 64]) == False:
                self.nextPosition[1] = self.nextPosition[1] - 64
            elif self.direction == 1 and self.currentChamber.walls([self.nextPosition[0] - 64, self.nextPosition[1]]) == False and getEventPosition([self.nextPosition[0] - 64, self.nextPosition[1]]) == False:
                self.nextPosition[0] = self.nextPosition[0] - 64
            elif self.direction == 2 and self.currentChamber.walls([self.nextPosition[0], self.nextPosition[1] + 64]) == False and getEventPosition([self.nextPosition[0], self.nextPosition[1] + 64]) == False:
                self.nextPosition[1] = self.nextPosition[1] + 64
            elif self.direction == 3 and self.currentChamber.walls([self.nextPosition[0] + 64, self.nextPosition[1]]) == False and getEventPosition([self.nextPosition[0] + 64, self.nextPosition[1]]) == False:
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
        self.cmdCount = 0
        for cmd in self.commandList:
            self.commandArgs = cmd[0].split('|')
            
            if self.commandArgs[0] == "wait":
                if pygame.time.get_ticks() - self.lastCmdTime <= int(self.commandArgs[1]):
                    self.waited = True
                    break
                elif self.waited == True and pygame.time.get_ticks() - self.lastCmdTime > int(self.commandArgs[1]):
                    self.commandList[self.cmdCount] = ["DONE"]
                    self.waited = False
                    break
                
            elif self.commandArgs[0] == "walk" and self.animationRunning == False:
                if int(self.commandArgs[2]) == 0:
                    self.nextPosition[1] = self.nextPosition[1] - 64 * int(self.commandArgs[1])
                elif int(self.commandArgs[2]) == 1:
                    self.nextPosition[0] = self.nextPosition[0] - 64 * int(self.commandArgs[1])
                elif int(self.commandArgs[2]) == 2:
                    self.nextPosition[1] = self.nextPosition[1] + 64 * int(self.commandArgs[1])
                elif int(self.commandArgs[2]) == 3:
                    self.nextPosition[0] = self.nextPosition[0] + 64 * int(self.commandArgs[1])
                self.direction = int(self.commandArgs[2])
                self.commandList[self.cmdCount] = ["DONE"]
                self.lastCmdTime = pygame.time.get_ticks()
                break

            elif self.commandArgs[0] == "playsound" and pygame.mixer.get_busy() == 0:
                soundList[int(self.commandArgs[1])].play()
                self.commandList[self.cmdCount] = ["DONE"]
                self.lastCmdTime = pygame.time.get_ticks()
                break

            elif self.commandArgs[0] == "endgame":
                startRunning()
                self.commandList[self.cmdCount] = ["DONE"]
                self.lastCmdTime = pygame.time.get_ticks()
                break

            elif self.commandList[self.cmdCount] == ["DONE"]:
                next

            self.cmdCount += 1
    
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
            windowSurface.blit(self.spriteList[self.direction], (self.position[0], self.position[1] - 64))

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
        
class MapSlice(object):
    def __init__(self, position, noBlock):
        self.position = position
        self.noBlock = noBlock
        if self.noBlock == 0:
            self.blockade = random.choice(blockadeList)
            self.blockade = [self.blockade, random.randint(2, 12 - self.blockade.height)]
    def update(self):
        windowSurface.blit(endGameBg, (self.position, 0))
        
        if self.noBlock == 0:
            windowSurface.blit(self.blockade[0].picture, (self.position, self.blockade[1] * 64))
            self.blockade[0].hitbox = pygame.Rect(self.position, self.blockade[1] * 64, self.blockade[0].height * 64, self.blockade[0].height * 64)
            #pygame.draw.rect(windowSurface, GREEN, self.blockade[0].hitbox) #debugging
        self.position = self.position - distance(speed, frameTime)

class Blockade(object):
    def __init__(self, picture, height):
        self.picture = picture
        self.height = height
        self.position = random.randint(2, 11)
        self.hitbox = None

class Boost(object):
    def __init__(self, position, picture, boost, currentChamber):
        self.position = position
        self.picture = [pygame.image.load("resources/boosts/" + picture[0]), pygame.image.load("resources/boosts/" + picture[1])]
        self.boost = boost
        self.currentChamber = currentChamber
        self.opened = 0
        self.triggerList = []
        for direction in range(0, 4):
            if direction == 0:
                self.triggerList.append([self.position[0], self.position[1] - 1, 2])
            elif direction == 1:
                self.triggerList.append([self.position[0] - 1, self.position[1], 3])
            elif direction == 2:
                self.triggerList.append([self.position[0], self.position[1] + 1, 0])
            elif direction == 3:
                self.triggerList.append([self.position[0] + 1, self.position[1], 1])
    def update(self):
        global endGameBoosts
        self.boostGiven = False
        
        if playerChar.currentChamber == self.currentChamber:
            windowSurface.blit(self.picture[self.opened], (self.position[0] * 64, self.position[1] * 64))
            for triggerTile in self.triggerList:
                if (playerChar.position[0] == triggerTile[0] * 64 and playerChar.position[1] == triggerTile[1] * 64) and (playerChar.direction == triggerTile[2]) and pygame.key.get_pressed()[13]:      
                    if self.opened == 0:
                        soundList[4].play()
                        endGameBoosts[self.boost[0]] += self.boost[1]
                        self.boostGiven = True
                    self.opened = 1
        return self.boostGiven

class BoostPic(object):
    def __init__(self, position, picture):
        self.position = position
        self.picture = pygame.image.load("resources/" + picture)
        self.spawnTime = pygame.time.get_ticks()
    def update(self):
        self.position[1] = self.position[1] - distance(0.05, frameTime)
        windowSurface.blit(self.picture, (self.position[0], int(self.position[1])))

# --- Set up ---
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50,40)

pygame.init()

#windowSurface = pygame.display.set_mode((1216, 768), pygame.FULLSCREEN, 32) #FULLSCREEN
windowSurface = pygame.display.set_mode((1216, 768), 0, 32)
pygame.display.set_caption('Lanceloet van Denemerken')

mainClock = pygame.time.Clock()

"""Fonts"""
basicFont = pygame.font.SysFont("palatinolinotype", 23)
bigFont = pygame.font.SysFont("palatinolinotype", 51)
alphabetPictures = []
loadFont()

# --- Other variables ---

#defaultSaveState = [[3 * 64, 1 * 64, 0], [2, 1, 2, 500], [], [], True] #position [x, y, Chamber] | Boosts | sounds played | options | debug
saveState = None
loadAll()

endGameBoosts = [saveState[1][0], saveState[1][1], saveState[1][2], saveState[1][3]]

showDebug = saveState[4]

loopTrack = 0
lastPress = 0

playerHitpoint = []

clicked = False
screenshot = False
grid = False

commandsLeft = False

escape = False
enter = False
playerLocked = False

playerY = 300 #Maybe temporary?
playerX = 128
speed = endGameBoosts[1]
lives = endGameBoosts[2]
speedUp = endGameBoosts[3]
playerHit = 0

playerDead = False

score = 0

reverseDirection = [2, 3, 0, 1]

letterSizeList = []
for picture in alphabetPictures:
    letterSizeList.append(picture.get_size()[0])

chamberList = []
eventList = []

loadChambersAndEvents()

for event in eventList:
    try:
        event.position[0] = saveState[2][eventList.index(event)][1][0]
        event.position[1] = saveState[2][eventList.index(event)][1][1]
        event.nextPosition[0] = saveState[2][eventList.index(event)][1][0]
        event.nextPosition[1] = saveState[2][eventList.index(event)][1][1]
    except:
        pass
    try:
        if saveState[2][eventList.index(event)] != False:
            event.commandList = []
    except:
        pass
    
boostList = []
boostPicList = []

path = os.path.abspath("scripts")
for script in os.listdir(path):
    with open('scripts/' + script, 'rb') as csvscript:
        scriptReader = csv.reader(csvscript, delimiter=' ', quotechar='"')
        scriptList = []
        if script.startswith('boost'):
            for command in scriptReader:
                scriptList.append(command)

            for command in scriptList:
                comArgs = command[0].split("|")
                if comArgs[0].startswith("pic"):
                    boostPicture = [comArgs[1], comArgs[2]]
                elif comArgs[0].startswith("position"):
                    boostPosition = [int(comArgs[1]), int(comArgs[2]), int(comArgs[3])]
                elif comArgs[0].startswith("boost"):
                    if comArgs[1] != '2':
                        boostBoost = [int(comArgs[1]), int(comArgs[2]) / 10]
                    else:
                        boostBoost = [int(comArgs[1]), int(comArgs[2])]

            boostList.append(Boost([boostPosition[0], boostPosition[1]], boostPicture, boostBoost, chamberList[0]))

for boost in boostList:
    try:
        boost.opened = saveState[3][boostList.index(boost)]
    except IndexError:
        boost.opened = 0

# --- Constants ---
BLACK = (0, 0, 0)
GRAY = (80, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

"""GameState system"""
MENU = 0
GAMEOVER = 1
SEARCHPLAY = 2
RUNPLAY = 3
PAUSE = 4
NEWGAME = 5
OPTIONS = 6
GameState = 0

# --- Image & music Loading --- 
directionList = [pygame.image.load('resources/sandrijn/up.png'),
                 pygame.image.load('resources/sandrijn/left.png'),
                 pygame.image.load('resources/sandrijn/down.png'),
                 pygame.image.load('resources/sandrijn/right.png'),
                 pygame.image.load('resources/sandrijn/upl.png'),
                 pygame.image.load('resources/sandrijn/leftl.png'),
                 pygame.image.load('resources/sandrijn/downl.png'),
                 pygame.image.load('resources/sandrijn/rightl.png'),
                 pygame.image.load('resources/sandrijn/upr.png'),
                 pygame.image.load('resources/sandrijn/leftr.png'),
                 pygame.image.load('resources/sandrijn/downr.png'),
                 pygame.image.load('resources/sandrijn/rightr.png'),
                 pygame.image.load('resources/sandrijn/fell.png'),
                 pygame.image.load('resources/sandrijn/nothing.png')]

player = directionList[5]

tile = pygame.image.load('resources/tile.png')

menuBg = pygame.image.load('resources/background.png')
pauseBg = pygame.image.load('resources/pause.png')

lifePic = pygame.image.load('resources/life.png')

soundList = []
for i in range(0, 999):
    soundList.append(None)

pygame.mixer.music.load('sounds/MENU.wav')

pygame.mixer.music.play(-1, 0.0)

path = os.path.abspath("sounds/voices")
for voice in os.listdir(path):
    soundList[int(voice[0] + voice[1] + voice[2])] = pygame.mixer.Sound('sounds/voices/' + voice)

endGameBg = pygame.image.load("resources/endgame/default.png")

blockadeList = []
mapSlices = []
path = os.path.abspath("resources/endgame")
for blockade in os.listdir(path):
    blkArgs = blockade.split(',')
    if blockade != "default.png":
        blockadeList.append(Blockade(pygame.image.load("resources/endgame/" + blockade), int(blkArgs[1][0])))

# --- Objects ---
playerChar = Character([saveState[0][0], saveState[0][1]], 0, directionList, chamberList[saveState[0][2]], None, [])

B_start = Button([720, 64], "VERDER GAEN", lambda:changeGameState(SEARCHPLAY, "SEARCH.wav"))
B_new = Button([720, 165], "NIEWE SPEL", lambda:changeGameState(NEWGAME, None))
B_options = Button([720, 266], "MOGELIJCHEDE", lambda:changeGameState(OPTIONS, None))
B_quit = Button([720, 468], "SLUIJTEN", lambda:quitGame())

B_yes = Button([608 - 469, 367], "JA", lambda:yes())
B_no = Button([608 + 5, 367], "NEEN", lambda:no())

B_continue = Button([720, 266], "VERDER GAEN", lambda:changeGameState(SEARCHPLAY, None))
B_menu = Button([720, 367], "MENU", lambda:changeGameState(MENU, "MENU.wav"))

# --- Main loop ---
while True:
    # --- Variables outside gamestate ---
    frameTime = mainClock.tick(1000)
    FPS = mainClock.get_fps()
    currentTime = pygame.time.get_ticks()
    mousePosition = pygame.mouse.get_pos()
    loopTrack = loopTrack + 1

    if frameTime > 100:
        frameTime = 2
    
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
            elif event.key == 282:
                grid = not grid
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

    # --- Settings --- 
    if GameState == OPTIONS:
        windowSurface.blit(menuBg, (0, 0))
        B_menu.doTasks()

    # --- Starting a new game ---
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
                changeGameState(SEARCHPLAY, "SEARCH.wav")
            elif B_no.doTasks() == True:
                GameState = MENU
        elif saveState == defaultSaveState:
            saveState = defaultSaveState
            changeGameState(SEARCHPLAY, "SEARCH.wav")
    
    if GameState == PAUSE:
        windowSurface.blit(pauseBg, (0, 0))
        B_continue.doTasks()
        B_quit.doTasks()
        if B_menu.doTasks():
            saveAll()

    # --- walking through the house searching for boosts ---
    if GameState == SEARCHPLAY:
        # --- blit images ---
        windowSurface.fill(BLACK)
        playerChar.currentChamber.render()

        playerLocked = False

        for event in eventList:
            event.updateAnimation()
            event.update()

            commandsLeft = False
            for command in event.commandList:
                if command != ['DONE']:
                    commandsLeft = True

            if playerChar.position in event.triggerTile and commandsLeft == True and playerChar.currentChamber == event.currentChamber:
                if event.exeCommands() or commandsLeft == True:
                    playerLocked = True
            elif commandsLeft == False:
                playerLocked = False

        for boost in boostList:
            if boost.update() == True:
                if boost.boost[0] != 2:
                    boostPicture = "speed.png"
                else:
                    boostPicture = "lives.png"
                boostPicList.append(BoostPic([playerChar.position[0] + random.randint(-16, 16), playerChar.position[1] - 32], boostPicture))

        playerChar.updateAnimation()
        playerChar.update()
        
        for boostPic in boostPicList:
            boostPic.update()
            if pygame.time.get_ticks() - boostPic.spawnTime >= 1000:
                del boostPicList[boostPicList.index(boostPic)]

        # --- Movement ---
        if playerLocked == False:
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
        if grid == True:
            for y in range(-1, 12):
                for x in range(-1, 19):
                    windowSurface.blit(tile, (x * 64, y * 64))
                    pass

        # --- Pause ---
        if escape and playerLocked == False:
            GameState = PAUSE
            escape = False

        # --- Changing to end-game ---
        if playerChar.nextPosition == [64, 64]: #temp
            startRunning()
            musicStarted = False

    # --- Fleeing for Lanseloet --- 
    if GameState == RUNPLAY:
        # --- create full map ---
        playerHitpoint = [196 - 32, int(playerY) + 120]
        playerDead = False
        for slices in mapSlices:
            slices.update()
            if slices.position < -256:
                del mapSlices[mapSlices.index(slices)]
            if slices.noBlock == 0:
                if slices.blockade[0].hitbox.collidepoint(playerHitpoint) and playerHit == 0:
                    lives = lives - 1
                    playerHit = pygame.time.get_ticks()

        if playerHit == 0:
            transparentOrNot = 11
        elif playerHit != 0:
            if pygame.time.get_ticks() - playerHit < 1500:
                transparentOrNot = 13
            elif pygame.time.get_ticks() - playerHit >= 1500:
                playerHit = 0

        # --- fill up map ---
        if len(mapSlices) < 16:
            mapSlices.append(MapSlice(mapSlices[len(mapSlices) - 1].position + 128, random.randint(0, 1)))

        # --- blit player ---
        runTime = 150
        if ((pygame.time.get_ticks() - (pygame.time.get_ticks() % runTime)) / runTime) % 2 == 0:
            windowSurface.blit(directionList[transparentOrNot], (128, playerY))
        elif ((pygame.time.get_ticks() - (pygame.time.get_ticks() % runTime)) / runTime) % 2 == 1:
            windowSurface.blit(directionList[7], (128, playerY))

        if pygame.key.get_pressed()[119]:
            playerY = playerY - distance(speed / 1.6, frameTime)
        elif pygame.key.get_pressed()[115]:
            playerY = playerY + distance(speed / 1.6, frameTime)

        if playerY <= 64:
            playerY = 64
        elif playerY >= 640:
            playerY = 640

        # --- Speed up ---
        if pygame.time.get_ticks() - lastSpeedUp >= speedUp:
            lastSpeedUp = pygame.time.get_ticks()
            if speed < endGameBoosts[0]:
                speed = speed + 0.01

        # --- Change music ---
        if lives == 1:
            if musicStarted == False:
                musicTime = pygame.mixer.music.get_pos()
                pygame.mixer.music.load("sounds/HURRYRUN.wav")
                pygame.mixer.music.play(-1, 0)
                musicStarted = True

        # --- Pause menu ---
        if escape:
            GameState = PAUSE
            escape = False

        # --- Start gameover gamestate            
        if lives <= 0:
            scoreEnd = pygame.time.get_ticks()
            score = scoreEnd - scoreStart
            resetSaveState()
            GameState = GAMEOVER

        # --- blit lives ---
        for life in range(0, lives):
            windowSurface.blit(lifePic, (life * 48 + 2, 768 - 70))

        # --- Score ---
        scoreText = "SCORE: " + str(int((pygame.time.get_ticks() / 1000) - scoreStart / 1000))
        text(scoreText, [1216 - getTextLength(scoreText), 728])

    if GameState == GAMEOVER:
        # --- Background ---
        windowSurface.fill(GRAY)
        text("EILAAS, SPEL VOREBEI", [1216 / 2 - int(getTextLength("EILAAS, SPEL VOREBEI")) / 2, 200])
        text("GIJ HEBT " + str(score / 1000) + " SEKONDEN OVERLEEFT.", [1216 / 2 - int(getTextLength("GIJ HEBT " + str(score / 1000) + " SEKONDEN OVERLEEFT.")) / 2, 250])

        B_menu.doTasks()
        B_quit.doTasks()

        # --- Clear map ---
        for slices in mapSlices:
            slices.update()
            if slices.position < -256:
                del mapSlices[mapSlices.index(slices)]

        # --- Fallen player
        playerX = playerX - distance(speed, frameTime)
        windowSurface.blit(directionList[12], (playerX, playerY + 64))
            
    # --- Debug ---
    if showDebug == True:
        try:
            #debug = "Max Speed: " + str(endGameBoosts[0]) + ", Starting Speed: " + str(endGameBoosts[1]) + ", Lives: " + str(endGameBoosts[2]) + ", Acceleration: " + str(endGameBoosts[3])
            debug = "Max Speed: " + str(endGameBoosts[0]) + ", Starting Speed: " + str(endGameBoosts[1]) + ", Acceleration: " + str(endGameBoosts[3]) + ", Speed: " + str(speed)
            #debug = playerLocked
        except NameError:
            debug = "Undefined"
        debugText = basicFont.render(str(debug), True, RED) #text | antialiasing | color
        windowSurface.blit(debugText, (1, 1))
        
    # --- Run outside GameState system ---
    """"Reset variables"""
    clicked = False

    if GameState != SEARCHPLAY:
        escape = False
    else:
        enter = False

    if GameState == SEARCHPLAY or GameState == RUNPLAY:
        pygame.mouse.set_visible(False)
    else:
        pygame.mouse.set_visible(True)

    """Screenshot"""
    if screenshot == True:
        screenshot = False
        for x in range(0, 65536):
            if os.path.exists("screenshot" + str(x) + ".png") == True:
                next
            elif os.path.exists("screenshot" + str(x) + ".png") == False:
                pygame.image.save(windowSurface, "screenshot" + str(x) + ".png")
                break
