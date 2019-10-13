import pygame as pg


class Block(object):
    def __init__(self, pos, size, color):
        self.otype = "block"
        self.pos = pos
        self.size = size
        self.color = color

    def draw(self, screen):
        pg.draw.rect(screen, self.color,
             (self.pos[0], self.pos[1], self.size[0], self.size[1]))
