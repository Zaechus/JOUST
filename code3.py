  # JOUST

import sys
import pygame as pg
import time
import math

from pygame.draw import rect as Rect

pg.init()

fps = 60
fpsClock = pg.time.Clock()
width, height = 800, 600
screen = pg.display.set_mode((width, height))
counter = 0
startTime = time.time()
tic = time.time()

STATE = 0
platformColor = (180, 150, 0)
BBuffer = height - 64
whoWins = 0
backgroundColor = (0, 0, 0)
TITLE = "JOUST"
menuTitleFont = pg.font.Font("./resources/ARCADECLASSIC.TTF", 128)
menuFont = pg.font.Font("./resources/ARCADECLASSIC.TTF", 32)
font = pg.font.Font("./resources/unispace.ttf", 16)
g = 1.3

pg.mixer.music.load("./resources/background.mp3")
pg.mixer.music.play(-1)

imageScale = 3
p1left_img = pg.image.load("./resources/p1left.bmp")
p1left_img = pg.transform.scale(p1left_img, (p1left_img.get_size()[0] * imageScale, p1left_img.get_size()[1] * imageScale))
p1right_img = pg.image.load("./resources/p1right.bmp")
p1right_img = pg.transform.scale(p1right_img, (p1right_img.get_size()[0] * imageScale, p1right_img.get_size()[1] * imageScale))
p1lFlap = pg.image.load("./resources/p1lflap.bmp")
p1lFlap = pg.transform.scale(p1lFlap, (p1lFlap.get_size()[0] * imageScale, p1lFlap.get_size()[1] * imageScale))
p1rFlap = pg.image.load("./resources/p1rflap.bmp")
p1rFlap = pg.transform.scale(p1rFlap, (p1rFlap.get_size()[0] * imageScale, p1rFlap.get_size()[1] * imageScale))

p2left_img = pg.image.load("./resources/p2left.bmp")
p2left_img = pg.transform.scale(p2left_img, (p2left_img.get_size()[0] * imageScale, p2left_img.get_size()[1] * imageScale))
p2right_img = pg.image.load("./resources/p2right.bmp")
p2right_img = pg.transform.scale(p2right_img, (p2right_img.get_size()[0] * imageScale, p2right_img.get_size()[1] * imageScale))
p2lFlap = pg.image.load("./resources/p2lflap.bmp")
p2lFlap = pg.transform.scale(p2lFlap, (p2lFlap.get_size()[0] * imageScale, p2lFlap.get_size()[1] * imageScale))
p2rFlap = pg.image.load("./resources/p2rflap.bmp")
p2rFlap = pg.transform.scale(p2rFlap, (p2rFlap.get_size()[0] * imageScale, p2rFlap.get_size()[1] * imageScale))

pA = 1.1
pMaxV = 10
p1Size = [p1left_img.get_size()[0], p1left_img.get_size()[1]]
p2Size = [p2left_img.get_size()[0], p2left_img.get_size()[1]]
p1pos = [150, 100]
p2pos = [650, 100]

class Block(object):

    def __init__(self, pos, size, color):
        self.otype = "block"
        self.pos = pos
        self.size = size
        self.color = color

    def draw(self):
        Rect(screen, self.color, (self.pos[0], self.pos[1], self.size[0], self.size[1]))

class Player(object):

    def __init__(self, i, pos, size, a, maxV, left_img, right_img, lFlap, rFlap):
        self.otype = "player"
        self.i = i
        self.pos = pos
        self.size = size
        self.a = a
        self.maxV = maxV
        self.left_img = left_img
        self.right_img = right_img
        self.lFlap = lFlap
        self.rFlap = rFlap

    direction = 1
    flap = 0

    vx = 0.
    xti = tic
    xt = 0.

    vy = 1.
    yti = tic
    yt = 0.

    def draw(self):
        imgRect = Rect(screen, backgroundColor, (self.pos[0], self.pos[1], self.size[0], self.size[1]))

        if self.direction == 0:
            if self.flap == 0:
                screen.blit(self.left_img, imgRect)
            elif self.flap == 1:
                screen.blit(self.lFlap, imgRect)
                self.flap = 0
        elif self.direction == 1:
            if self.flap == 0:
                screen.blit(self.right_img, imgRect)
            elif self.flap == 1:
                screen.blit(self.rFlap, imgRect)
                self.flap = 0

    def events(self):
        if self.i == 1:
            self.UP = keys[pg.K_x]
            self.LEFT = keys[pg.K_z]
            self.RIGHT = keys[pg.K_c]
        elif self.i == 2:
            self.UP = keys[pg.K_UP]
            self.LEFT = keys[pg.K_LEFT]
            self.RIGHT = keys[pg.K_RIGHT]

        if self.LEFT and not self.RIGHT:
            self.direction = 0
            if self.vx > -self.maxV * 1.3:
                self.xt = tic - self.xti
                self.vx -= (1/2.) * self.a * self.xt
        elif self.RIGHT and not self.LEFT:
            self.direction = 1
            if self.vx < self.maxV * 1.3:
                self.xt = tic - self.xti
                self.vx += self.a * self.xt
        else:
            self.xti = tic
            if self.vx > 0.:
                self.vx -= (0.2) * self.a
            elif self.vx < 0.:
                self.vx += (0.2) * self.a

        if self.UP:
            self.flap = 1
            if self.vy < self.maxV:
                self.yt = tic - self.yti
                self.vy += self.a * self.yt
        else:
            self.yti = tic
            if self.vy > -self.maxV * 1.5:
                self.vy -= (0.2) * g
                self.flap = 0

    def update(self):

        if self.vx != 0:
            self.pos[0] += (1/2.) * self.vx

        self.pos[1] -= (1/2.) * self.vy

    def collisions(self, obstacles):
        self.obstacles = obstacles

        global whoWins

        for block in obstacles:
            if block.otype == "block":
                if (self.pos[0] + self.size[0]) > block.pos[0] and self.pos[0] < (block.pos[0] + block.size[0]):
                    if (self.pos[1] + self.size[1]) > block.pos[1] and (self.pos[1] + self.size[1]) < (block.pos[1] + block.size[1] - 1):
                        self.pos[1] = block.pos[1] - self.size[1]
                        self.vy = -self.vy * (0.2)
                    if self.pos[1] > (block.pos[1] + 1) and self.pos[1] < (block.pos[1] + block.size[1] + 2):
                        self.pos[1] = block.pos[1] + block.size[1] + 2
                        self.vy = -self.vy * (0.2)
            elif block.otype == "player":
                if ((self.pos[0] + self.size[0]) > block.pos[0] and self.pos[0] < (block.pos[0] + block.size[0])):
                    if (self.pos[1] + self.size[1]) > block.pos[1] and self.pos[1] < (block.pos[1] + block.size[1]):
                        if self.pos[1] > block.pos[1]:
                            self.pos = [150, 100]
                            block.pos = [650, 100]
                            self.vx = 0.
                            self.vy = 1.
                            block.vx = 0.
                            block.vy = 1.
                            whoWins = block.i

              # LEFT EDGE --> RIGHT EDGE
            if self.pos[0] < 0:
                self.pos[0] = width - self.size[0]
              # RIGHT EDGE --> LEFT EDGE
            if self.pos[0] > width - self.size[0]:
                self.pos[0] = 0
              # TOP EDGE
            if self.pos[1] < 0:
                self.pos[1] = 0
                self.vy = -self.vy * (0.2)
              # BOTTOM EDGE
            if self.pos[1] > BBuffer - self.size[1]:
                self.pos[1] = BBuffer - self.size[1]
                self.vy = -self.vy * (0.2)

objects = []

plat1 = Block([300, 400], [200, 15], platformColor)
plat2 = Block([50, 200], [200, 20], platformColor)
plat3 = Block([550, 250], [200, 17], platformColor)

p1 = Player(1, p1pos, p1Size, pA, pMaxV, p1left_img, p1right_img, p1lFlap, p1rFlap)
p2 = Player(2, p2pos, p2Size, pA, pMaxV, p2left_img, p2right_img, p2lFlap, p2rFlap)

objects.append(plat1)
objects.append(plat2)
objects.append(plat3)
objects.append(p1)
objects.append(p2)

def drawObjects(objectList):
    for i in objectList:
        i.draw()

def UPDATE_MENU():

    global event, counter, keys, tic, STATE, whoWins

    tic = time.time()
    event = pg.event.wait()
    keys = pg.key.get_pressed()
    counter += 1
    if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
        pg.quit()
        sys.exit()
    if event.type == pg.KEYDOWN and keys[pg.K_RETURN]:
        STATE = 1;
    if counter % 100 == 0:
        pg.event.clear()
    pg.event.post(pg.event.Event(1))

def UPDATE_GAME():

    global event, counter, keys, tic, STATE, whoWins

    tic = time.time()
    event = pg.event.wait()
    keys = pg.key.get_pressed()
    counter += 1
    if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
        pg.quit()
        sys.exit()
    if counter % 100 == 0:
        pg.event.clear()

    p1.collisions(objects)
    p2.collisions(objects)
    p1.events()
    p2.events()
    p1.update()
    p2.update()

    if whoWins > 0:
        STATE = 2

    pg.event.post(pg.event.Event(1))

def UPDATE_WIN():

        global event, counter, keys, tic, STATE, whoWins

        tic = time.time()
        event = pg.event.wait()
        keys = pg.key.get_pressed()
        counter += 1
        if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN and keys[pg.K_RETURN]:
            whoWins = 0
            STATE = 0
        if counter % 100 == 0:
            pg.event.clear()
        pg.event.post(pg.event.Event(1))

def DRAW_MENU():

    imageScale = 4
    mp1left_img = pg.transform.scale(p1left_img, (p1left_img.get_size()[0] * imageScale, p1left_img.get_size()[1] * imageScale))
    mp2rFlap = pg.transform.scale(p2rFlap, (p2rFlap.get_size()[0] * imageScale, p2rFlap.get_size()[1] * imageScale))

    imgRect1 = Rect(screen, backgroundColor, (width - p2rFlap.get_size()[0] * imageScale - 15, height - p2rFlap.get_size()[1] * imageScale - 15, 10, 10))
    imgRect2 = Rect(screen, backgroundColor, (20, 10, 10, 10))

    menuTitle = menuTitleFont.render("JOUST", 1, (255, 255, 0))
    startText = menuFont.render("PRESS   ENTER   TO   START", 1, (255, 255, 0))

    screen.fill(backgroundColor)
    screen.blit(menuTitle, (width / 2 - (menuTitle.get_rect()[2] / 2), height / 5))
    screen.blit(startText, (width / 2 - (startText.get_rect()[2] / 2), height / 1.6))
    screen.blit(mp1left_img, imgRect1)
    screen.blit(mp2rFlap, imgRect2)
    pg.display.flip()

def DRAW_GAME():
    clockTime = math.floor(tic - startTime)
    clock = font.render("Time: " + str(clockTime), 1, (0, 255, 0))

    screen.fill(backgroundColor)
    Rect(screen, platformColor, (0, BBuffer, width, height))
    Rect(screen, backgroundColor, (10, BBuffer + 10, 150, height - BBuffer - 20))
    screen.blit(clock, (20, height - 45))
    drawObjects(objects)
    pg.display.flip()

def DRAW_WIN():
    winText = menuFont.render("Player   " + str(whoWins) + "   wins!", 1, (255, 0, 255))
    screen.fill(backgroundColor)
    screen.blit(winText, (width / 2 - (winText.get_rect()[2] / 2), height / 2 - (winText.get_rect()[3] / 2)))
    pg.display.flip()

if __name__ == "__main__":
    pg.display.set_caption(TITLE)
    pg.mouse.set_visible(0)

    while True:
        if STATE == 0:
            UPDATE_MENU()
            DRAW_MENU()
        elif STATE == 1:
            UPDATE_GAME()
            DRAW_GAME()
        elif STATE == 2:
            UPDATE_WIN()
            DRAW_WIN()

        fpsClock.tick(fps)
