# Snake Game
#-----------------------------------------------------------------------------------------------------------------------------------------------------#
import pygame, sys,random
from pygame.locals import *
from pygame import mixer
mixer.init()
#------------------------------------------------------------------------------------------------------------------------------------------------------#
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
DARKGRAY = (40, 40, 40)
BGCOLOR = BLACK
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
HEAD = 0
#------------------------------------------------------------------------------------------------------------------------------------------------#
sound_1 = pygame.mixer.Sound('Snake Game\\Resources\\Audios\\BG 1.mp3')
sound_1.set_volume(0.1)
sound_2 = pygame.mixer.Sound('Snake Game\\Resources\\Audios\\hit.wav')
sound_2.set_volume(0.4)
sound_3 = pygame.mixer.Sound('Snake Game\\Resources\\Audios\\point.wav')
sound_3.set_volume(0.8)
sound_4 = pygame.mixer.Sound('Snake Game\\Resources\\Audios\\die.mp3')
sound_4.set_volume(0.2)
#------------------------------------------------------------------------------------------------------------------------------------------------#
def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Snake Game')
    sound_1.play(-1)
    exit_game = False
    while not exit_game:
        start_screen()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            elif event.type == pygame.KEYDOWN:
                if event.key == K_F1 :
                     # pygame.time.wait(300)
                     exit_game = True

    pygame.display.update()
    pygame.time.wait(300)
    showStartScreen()
    sound_4
    while True:
        runGame()
        sound_4
        showGameOverScreen()
#------------------------------------------------------------------------------------------------------------------------------------------------#
def runGame():
    # Set a random start point.
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    wormCoords = [{'x': startx, 'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    direction = RIGHT
    # Start the apple in a random place.
    apple = getRandomLocation()
    while True:
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    sound_4.play()
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    sound_4.play()
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    sound_4.play()
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    sound_4.play()
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()
        # check if the worm has hit itself or the edge
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or \
                wormCoords[HEAD]['y'] == CELLHEIGHT:
            return  # game over
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return  # game over
        # check if worm has eaten an apply
        i = 0
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            pygame.time.Clock,wormCoords
            # don't remove worm's tail segment
            sound_3.play()
            apple = getRandomLocation()  # set a new apple somewhere
            i += 2
        else:
            del wormCoords[-1]  # remove worm's tail segment
        # move the worm by adding a segment in the direction it is moving
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}
        wormCoords.insert(0, newHead)
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(wormCoords)
        drawApple(apple)
        drawScore(len(wormCoords) - 3)
        pygame.display.update()
        sp1 = 0
        for sp1 in range(1,25):
            if (len(wormCoords)-3) >= 0 and (len(wormCoords)-3) <= 5 :
                sp1 = 10
            elif (len(wormCoords) - 3) >= 5 and (len(wormCoords)-3) <= 10 :
                sp1 = 13
            elif (len(wormCoords)-3) >= 10 and (len(wormCoords)-3) <= 15:
                sp1 = 15
            elif (len(wormCoords) - 3) >= 15 and (len(wormCoords)-3) <= 20:
                sp1 = 17
            elif (len(wormCoords)-3) >= 20 and (len(wormCoords)-3) <= 25:
                sp1 = 20
            elif (len(wormCoords) - 3) >= 25 and (len(wormCoords)-3) <= 30:
                sp1 = 23
            elif (len(wormCoords) - 3) >= 30 and (len(wormCoords)-3) >= 35:
                sp1 = 25
        Snake_Speed = sp1
        pygame.display.update()
        FPSCLOCK.tick(Snake_Speed)
#------------------------------------------------------------------------------------------------------------------------------------------------#
def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press Space to play and Esc. to Quit.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 475, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)
#------------------------------------------------------------------------------------------------------------------------------------------------#
def drawPressKeyMsg1():
    pressKeySurf = BASICFONT.render('Press a key to play again.', True, (0,233,200))
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 415, WINDOWHEIGHT - 205)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)
#------------------------------------------------------------------------------------------------------------------------------------------------#
def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()
    keyUpEvents = pygame.event.get(KEYDOWN)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key
#------------------------------------------------------------------------------------------------------------------------------------------------#
def start_screen():
    bging = pygame.image.load("Snake Game\\Resources\\Images\\Snake.JPG")
    bging = pygame.transform.scale(bging, (WINDOWWIDTH, WINDOWHEIGHT)).convert_alpha()
    DISPLAYSURF.blit(bging, (0, 0))
    pygame.display.update()
#------------------------------------------------------------------------------------------------------------------------------------------------#
def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Snake Game!', True, WHITE, DARKGREEN)
    titleSurf2 = titleFont.render('Snake Game!', True, GREEN)
    degrees1 = 0
    degrees2 = 0

    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)
        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)
        drawPressKeyMsg()
        if checkForKeyPress():
            pygame.event.get()  # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(15)
        degrees1 += 3  # rotate by 3 degrees each frame
        degrees2 += 7  # rotate by 7 degrees each frame
#------------------------------------------------------------------------------------------------------------------------------------------------#
def terminate():
    pygame.quit()
    sys.exit()
#------------------------------------------------------------------------------------------------------------------------------------------------#
def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}
#------------------------------------------------------------------------------------------------------------------------------------------------#
def showGameOverScreen():
    sound_2.play()
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    game_over = pygame.image .load("Snake Game\\Resources\\Images\\hqdefault.jpg")
    game_over = pygame.transform.scale(game_over,(WINDOWWIDTH,WINDOWHEIGHT))
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)
    DISPLAYSURF.blit(game_over, (0,0))
    pygame.display.update()
    pygame.time.wait(500)
    # clear out any key presses in the event queue
    showStartScreen()
#------------------------------------------------------------------------------------------------------------------------------------------------#
def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)
#------------------------------------------------------------------------------------------------------------------------------------------------#
def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, GREEN, wormInnerSegmentRect)
#------------------------------------------------------------------------------------------------------------------------------------------------#
def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)
#------------------------------------------------------------------------------------------------------------------------------------------------#
def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE):  # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):  # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))
#------------------------------------------------------------------------------------------------------------------------------------------------#
if __name__ == '__main__':
    main()
# ------------------------------------------------------------------------------------------------------------------------------------------------#
# Code Ends Here!
# Thank ypo For watching this code
# By Aishwary