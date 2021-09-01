# Welcome to THE PONG GAME
# Made by Eddie Elvira
# Visit www.github.com/blitzymango for project description and a future README file

import random
from tkinter.constants import VERTICAL
import pygame
import tkinter as tk
from tkinter import messagebox
import asyncio


class pong(object):
    l = 750
    w = 500
    r = 8

    def __init__(self, color1=(0, 0, 255), color2=(255,255,255)):
        self.color1 = color1
        self.color2 = color2

    @staticmethod
    def event_quit() -> bool:
        for event in pygame.event.get():   # creates a list of events
            if event.type == pygame.QUIT:  # quit game when the user closes the window
                pygame.quit()
                return False
        return True

    @staticmethod
    async def redrawWindow(surface):
        surface.fill((0, 0, 0))  # creates a background (black in this case)
        asyncio.create_task(game.draw(surface))
        pygame.display.update()
    
    @staticmethod
    async def move():
        global p1, p2, b
        p1.move()
        p2.move()
        await b.move()

    def message_box():
        pass

    @staticmethod
    async def draw(surface):
        b.draw_ball(surface)
        p1.draw_paddle(surface)
        p2.draw_paddle(surface)
        pygame.display.update()
        await asyncio.sleep(0.01)


class ball(pong):
    length = pong.l
    width = pong.w
    radius = pong.r

    def __init__(self):
        super().__init__()
        self.pos = [length//2, width//2]
        self.dirnx = length//100
        self.dirny = width//100

    async def horizontal_collision(self):
        asyncio.create_task(b.vertical_collision())
         # If ball is moving right
        if self.dirnx > 0:
            if self.pos[0] + self.radius >= p1.location()[0]:
                y_top1 = p1.location()[1]
                y_bottom1 = y_top1 + p1.length()
                b.paddle_collision(p1, self.pos[1], y_top1, y_bottom1)
            if self.pos[0] + self.radius > length:
                self.dirnx = -self.dirnx

        # If ball is moving left
        if self.dirnx < 0:
            if self.pos[0] - self.radius <= p2.location()[0]+p2.width():
                y_top2 = p2.location()[1]
                y_bottom2 = y_top2 + p2.length()
                b.paddle_collision(p2, self.pos[1], y_top2, y_bottom2)
            if self.pos[0] + self.radius <= 0:
                self.dirnx = -self.dirnx

    async def vertical_collision(self):
        # If ball is moving up
        if self.dirny < 0:
            # if ball touches top of screen
            if self.pos[1] <= (self.radius):
                self.dirny = -self.dirny

        # If ball is moving down
        if self.dirny > 0:
            # if ball touches bottom of screen
            if self.pos[1] >= (self.width-self.radius):
                self.dirny = -self.dirny
        await asyncio.sleep(0)

    def paddle_collision(self, paddle, yball, ytop, ybottom):
        if (yball <= ybottom) and (yball >= ytop):
            self.dirnx = -self.dirnx
            if paddle.velocity() != 0:
                self.dirny = paddle.velocity() // 2
                

    async def move(self):
        self.pos = [self.pos[0] + self.dirnx, self.pos[1] + self.dirny]
        await b.horizontal_collision()

    def draw_ball(self, surface):
        circleCenter = (self.pos[0], self.pos[1])
        pygame.draw.circle(surface, self.color2, circleCenter, self.radius)


class paddle(pong):
    length = pong.l
    width = pong.w
    pad_width = length // 40        # width of paddle
    pad_length = width // 5         # length of paddle
    center = width//2-pad_length//2 # y-coordinate used to center paddle
    p1_space = length - pad_width*3 # space between wall and paddle1
    p2_space = pad_width*2          # space between wall and paddle2

    def __init__(self, player1):
        super().__init__()
        self.player1 = player1

        if self.player1:
            self.pos = (self.p1_space, self.center)
        else:
            self.pos = (self.p2_space, self.center)

    def location(self):
        return self.pos

    def length(self):
        return self.pad_length

    def width(self):
        return self.pad_width

    def velocity(self):
        return self.dirny

    def move(self, dirny=0):
        self.dirny = dirny
        self.pos = [self.pos[0], self.pos[1] + self.dirny]

        keys = pygame.key.get_pressed()  # records that a key was pressed
        if self.player1:
            if keys[pygame.K_UP]:
                self.dirny = -width // 40
            elif keys[pygame.K_DOWN]:
                self.dirny = width // 40
                
        else:
            if keys[pygame.K_w]:
                self.dirny = -width // 40
            elif keys[pygame.K_s]:
                self.dirny = width // 40
                
        self.pos[1] += self.dirny
        # if self.pos[1]-self.pad_length//2-self.dirny < 0:
        #     self.dirny = 0
        # elif self.pos[1]+self.pad_length+self.dirny >= width:
        #     self.dirny = 0
        # else:
        #     self.pos[1] += self.dirny



    def draw_paddle(self, surface):
        # x-coordinate of top-left corner of rectangle
        x = self.pos[0]
        # y-coordinate of top-left corner of rectangle
        y = self.pos[1]

        if self.player1:
            pygame.draw.rect(surface, self.color1,
                             (x, y, self.pad_width, self.pad_length))
        else:
            pygame.draw.rect(surface, self.color1,
                             (x, y, self.pad_width, self.pad_length))


if __name__ == '__main__':
    global length, width, b, p1, p2, game

    length = 750
    width = 500

    flag = True
    b = ball()
    p1 = paddle(True)
    p2 = paddle(False)
    game = pong()

    pygame.init()
    # create game and background with length x width size
    win = pygame.display.set_mode((length, width))
    asyncio.run(game.redrawWindow(win))
    clock = pygame.time.Clock()

    while flag:
        # 50 milliseconds (lower value = faster)
        pygame.time.delay(30)
        clock.tick(60)                  # fps limit (lower value = slower)
        asyncio.run(pong.move())

        # did the user close the window? If so, terminate program
        flag = game.event_quit()
        if not flag:                    # if user closed window, break loop too
            break

        asyncio.run(game.redrawWindow(win))
