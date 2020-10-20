#!/usr/bin/env python
# -*- coding: utf-8 -*-

# JOUST

import sys
import pygame as pg
import time
import math

from pygame.draw import rect as Rect

from block import Block
from player import Player
from settings import WIDTH, HEIGHT, BOTTOM_MARGIN

pg.init()

fps = 60
fps_clock = pg.time.Clock()

screen = pg.display.set_mode((WIDTH, HEIGHT))

counter = 0
start_time = time.time()
tic = time.time()

state = 0
platform_color = (180, 150, 0)
who_wins = 0
background_color = (0, 0, 0)
menu_title_font = pg.font.Font("./resources/ARCADECLASSIC.TTF", 128)
menu_font = pg.font.Font("./resources/ARCADECLASSIC.TTF", 32)
font = pg.font.Font("./resources/unispace.ttf", 16)
g = 1.3

pg.mixer.music.load("./resources/background.mp3")
pg.mixer.music.play(-1)

image_scale = 3
p1left_img = pg.image.load("./resources/p1left.bmp")
p1left_img = pg.transform.scale(p1left_img,
                                (p1left_img.get_size()[0] * image_scale,
                                 p1left_img.get_size()[1] * image_scale))
p1right_img = pg.image.load("./resources/p1right.bmp")
p1right_img = pg.transform.scale(p1right_img,
                                 (p1right_img.get_size()[0] * image_scale,
                                  p1right_img.get_size()[1] * image_scale))
p1lFlap = pg.image.load("./resources/p1lflap.bmp")
p1lFlap = pg.transform.scale(
    p1lFlap,
    (p1lFlap.get_size()[0] * image_scale, p1lFlap.get_size()[1] * image_scale))
p1rFlap = pg.image.load("./resources/p1rflap.bmp")
p1rFlap = pg.transform.scale(
    p1rFlap,
    (p1rFlap.get_size()[0] * image_scale, p1rFlap.get_size()[1] * image_scale))

p2left_img = pg.image.load("./resources/p2left.bmp")
p2left_img = pg.transform.scale(p2left_img,
                                (p2left_img.get_size()[0] * image_scale,
                                 p2left_img.get_size()[1] * image_scale))
p2right_img = pg.image.load("./resources/p2right.bmp")
p2right_img = pg.transform.scale(p2right_img,
                                 (p2right_img.get_size()[0] * image_scale,
                                  p2right_img.get_size()[1] * image_scale))
p2lFlap = pg.image.load("./resources/p2lflap.bmp")
p2lFlap = pg.transform.scale(
    p2lFlap,
    (p2lFlap.get_size()[0] * image_scale, p2lFlap.get_size()[1] * image_scale))
p2rFlap = pg.image.load("./resources/p2rflap.bmp")
p2rFlap = pg.transform.scale(
    p2rFlap,
    (p2rFlap.get_size()[0] * image_scale, p2rFlap.get_size()[1] * image_scale))

pA = 1.1
pMaxV = 10
p1Size = [p1left_img.get_size()[0], p1left_img.get_size()[1]]
p2Size = [p2left_img.get_size()[0], p2left_img.get_size()[1]]
p1pos = [150, 100]
p2pos = [650, 100]

objects = []

plat1 = Block([300, 400], [200, 15], platform_color)
plat2 = Block([50, 200], [200, 20], platform_color)
plat3 = Block([550, 250], [200, 17], platform_color)

p1 = Player(1, p1pos, p1Size, pA, pMaxV, p1left_img, p1right_img, p1lFlap,
            p1rFlap)
p2 = Player(2, p2pos, p2Size, pA, pMaxV, p2left_img, p2right_img, p2lFlap,
            p2rFlap)

objects.append(plat1)
objects.append(plat2)
objects.append(plat3)
objects.append(p1)
objects.append(p2)


def drawObjects(objectList):
    for i in objectList:
        i.draw(screen)


def UPDATE_MENU():

    global event, counter, keys, tic, state, who_wins

    tic = time.time()
    event = pg.event.wait()
    keys = pg.key.get_pressed()
    counter += 1
    if event.type == pg.QUIT:
        pg.quit()
        sys.exit()
    if event.type == pg.KEYDOWN and keys[pg.K_RETURN]:
        state = 1
    if counter % 100 == 0:
        pg.event.clear()
    pg.event.post(pg.event.Event(1))


def UPDATE_GAME():

    global event, counter, keys, tic, state, who_wins

    tic = time.time()
    event = pg.event.wait()
    keys = pg.key.get_pressed()
    counter += 1
    if event.type == pg.QUIT:
        pg.quit()
        sys.exit()
    if counter % 100 == 0:
        pg.event.clear()

    p1.events(tic, keys)
    p2.events(tic, keys)
    p1.update()
    p2.update()

    who_wins = p1.collisions(objects)
    if who_wins != None:
        state = 2
        return
    who_wins = p2.collisions(objects)
    if who_wins != None:
        state = 2
        return

    pg.event.post(pg.event.Event(1))


def UPDATE_WIN():

    global event, counter, keys, tic, state, who_wins

    tic = time.time()
    event = pg.event.wait()
    keys = pg.key.get_pressed()
    counter += 1
    if event.type == pg.QUIT:
        pg.quit()
        sys.exit()
    if event.type == pg.KEYDOWN and keys[pg.K_RETURN]:
        who_wins = None
        state = 0
    if counter % 100 == 0:
        pg.event.clear()
    pg.event.post(pg.event.Event(1))


def DRAW_MENU():

    image_scale = 4
    mp1left_img = pg.transform.scale(p1left_img,
                                     (p1left_img.get_size()[0] * image_scale,
                                      p1left_img.get_size()[1] * image_scale))
    mp2rFlap = pg.transform.scale(p2rFlap,
                                  (p2rFlap.get_size()[0] * image_scale,
                                   p2rFlap.get_size()[1] * image_scale))

    img_rect1 = Rect(screen, background_color,
                     (WIDTH - p2rFlap.get_size()[0] * image_scale - 15,
                      HEIGHT - p2rFlap.get_size()[1] * image_scale - 15, 10, 10))
    img_rect2 = Rect(screen, background_color, (20, 10, 10, 10))

    menuTitle = menu_title_font.render("JOUST", 1, (255, 255, 0))
    startText = menu_font.render(
        "PRESS   ENTER   TO   START", 1, (255, 255, 0))

    screen.fill(background_color)
    screen.blit(menuTitle,
                (WIDTH / 2 - (menuTitle.get_rect()[2] / 2), HEIGHT / 5))
    screen.blit(startText,
                (WIDTH / 2 - (startText.get_rect()[2] / 2), HEIGHT / 1.6))
    screen.blit(mp1left_img, img_rect1)
    screen.blit(mp2rFlap, img_rect2)
    pg.display.flip()


def DRAW_GAME():
    clockTime = math.floor(tic - start_time)
    clock = font.render("Time: " + str(clockTime), 1, (0, 255, 0))

    screen.fill(background_color)
    Rect(screen, platform_color, (0, BOTTOM_MARGIN, WIDTH, HEIGHT))
    Rect(screen, background_color,
         (10, BOTTOM_MARGIN + 10, 150, HEIGHT - BOTTOM_MARGIN - 20))
    screen.blit(clock, (20, HEIGHT - 45))
    drawObjects(objects)
    pg.display.flip()


def DRAW_WIN():
    winText = menu_font.render("Player   " + str(who_wins) + "   wins!", 1,
                               (255, 0, 255))
    screen.fill(background_color)
    screen.blit(winText, (WIDTH / 2 - (winText.get_rect()[2] / 2),
                          HEIGHT / 2 - (winText.get_rect()[3] / 2)))
    pg.display.flip()


if __name__ == "__main__":
    pg.display.set_caption("JOUST")
    pg.mouse.set_visible(0)

    while True:
        if state == 0:
            UPDATE_MENU()
            DRAW_MENU()
        elif state == 1:
            UPDATE_GAME()
            DRAW_GAME()
        elif state == 2:
            UPDATE_WIN()
            DRAW_WIN()

        fps_clock.tick(fps)
