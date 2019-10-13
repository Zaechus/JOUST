import pygame as pg

from settings import WIDTH, BOTTOM_MARGIN, GRAV


class Player(object):
    def __init__(self, i, pos, size, a, max_v, left_img, right_img, l_flap,
                 r_flap):
        self.otype = "player"
        self.i = i
        self.pos = pos
        self.size = size
        self.a = a
        self.max_v = max_v
        self.left_img = left_img
        self.right_img = right_img
        self.l_flap = l_flap
        self.r_flap = r_flap

    direction = 1
    flap = 0

    vx = 0.
    xti = 0
    xt = 0.

    vy = 1.
    yti = 0
    yt = 0.

    def draw(self, screen, background_color=(0, 0, 0)):
        img_rect = pg.draw.rect(screen, background_color,
                                (self.pos[0], self.pos[1], self.size[0], self.size[1]))

        if self.direction == 0:
            if self.flap == 0:
                screen.blit(self.left_img, img_rect)
            elif self.flap == 1:
                screen.blit(self.l_flap, img_rect)
                self.flap = 0
        elif self.direction == 1:
            if self.flap == 0:
                screen.blit(self.right_img, img_rect)
            elif self.flap == 1:
                screen.blit(self.r_flap, img_rect)
                self.flap = 0

    def events(self, tic, keys):
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
            if self.vx > -self.max_v * 1.3:
                self.xt = tic - self.xti
                self.vx -= (1 / 2.) * self.a * self.xt
        elif self.RIGHT and not self.LEFT:
            self.direction = 1
            if self.vx < self.max_v * 1.3:
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
            if self.vy < self.max_v:
                self.yt = tic - self.yti
                self.vy += self.a * self.yt
        else:
            self.yti = tic
            if self.vy > -self.max_v * 1.5:
                self.vy -= (0.2) * GRAV
                self.flap = 0

    def update(self):

        if self.vx != 0:
            self.pos[0] += (1 / 2.) * self.vx

        self.pos[1] -= (1 / 2.) * self.vy

    def collisions(self, obstacles):
        self.obstacles = obstacles

        for block in obstacles:
            if block.otype == "block":
                if (self.pos[0] +
                        self.size[0]) > block.pos[0] and self.pos[0] < (
                            block.pos[0] + block.size[0]):
                    if (self.pos[1] + self.size[1]) > block.pos[1] and (
                            self.pos[1] + self.size[1]) < (
                                block.pos[1] + block.size[1] - 1):
                        self.pos[1] = block.pos[1] - self.size[1]
                        self.vy = -self.vy * (0.2)
                    if self.pos[1] > (block.pos[1] + 1) and self.pos[1] < (
                            block.pos[1] + block.size[1] + 2):
                        self.pos[1] = block.pos[1] + block.size[1] + 2
                        self.vy = -self.vy * (0.2)
            elif block.otype == "player":
                if ((self.pos[0] + self.size[0]) > block.pos[0]
                        and self.pos[0] < (block.pos[0] + block.size[0])):
                    if (self.pos[1] +
                            self.size[1]) > block.pos[1] and self.pos[1] < (
                                block.pos[1] + block.size[1]):
                        if self.pos[1] > block.pos[1]:
                            self.pos = [150, 100]
                            block.pos = [650, 100]
                            self.vx = 0.
                            self.vy = 1.
                            block.vx = 0.
                            block.vy = 1.
                            return block.i

            # LEFT EDGE --> RIGHT EDGE
            if self.pos[0] < 0:
                self.pos[0] = WIDTH - self.size[0]
            # RIGHT EDGE --> LEFT EDGE
            if self.pos[0] > WIDTH - self.size[0]:
                self.pos[0] = 0
            # TOP EDGE
            if self.pos[1] < 0:
                self.pos[1] = 0
                self.vy = -self.vy * (0.2)
            # BOTTOM EDGE
            if self.pos[1] > BOTTOM_MARGIN - self.size[1]:
                self.pos[1] = BOTTOM_MARGIN - self.size[1]
                self.vy = -self.vy * (0.2)
