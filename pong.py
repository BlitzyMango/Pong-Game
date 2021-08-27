# Welcome to THE PONG GAME
# Made by Eddie Elvira
# Visit www.github.com/blitzymango for project description and a future README file

import random
import pygame
import tkinter as tk
from tkinter import messagebox


class pong(object):
    l = 750
    w = 500
    r = 8

    def __init__(self, color=(0, 0, 255)):
        self.color = color

    @staticmethod
    def event_quit() -> bool:
        for event in pygame.event.get():   # creates a list of events
            if event.type == pygame.QUIT:  # quit game when the user closes the window
                pygame.quit()
                return False
        return True

    @staticmethod
    def redrawWindow(surface):
        global b, p1, p2

        surface.fill((0, 0, 0))  # creates a background (black in this case)
        b.draw_ball(surface)
        p1.draw_paddle(surface)
        p2.draw_paddle(surface)
        pygame.display.update()

    def message_box():
        pass

    def draw():
        pass


class ball(pong):
    length = pong.l
    width = pong.w
    radius = pong.r

    def __init__(self):
        super().__init__()
        self.pos = [length//2, width//2]
        self.dirnx = 3
        self.dirny = 3

    def move_ball(self):
        self.dirnx = ball.speed_limit(self.dirnx)
        self.dirny = ball.speed_limit(self.dirny)

        # if ball touches right side of screen
        if self.pos[0] >= (self.length-self.radius-self.dirnx):
            self.dirnx = -self.dirnx
        # if ball touches left side of screen
        elif self.pos[0] <= (self.radius+self.dirnx):
            self.dirnx = -self.dirnx
        # if ball touches top of screen
        elif self.dirny < 0 and self.pos[1] <= (self.radius+self.dirny):
            self.dirny = -self.dirny - random.randint(-1, 1)
        # if ball touches bottom of screen
        elif self.dirny > 0 and self.pos[1] >= (self.width-self.radius-self.dirny):
            self.dirny = -self.dirny - random.randint(-1, 1)

        self.pos = [self.pos[0] + self.dirnx, self.pos[1] + self.dirny]

    @staticmethod
    def speed_limit(velocity) -> int:
        if velocity > 7:
            velocity = 7
        elif velocity < -7:
            velocity = -7
        elif velocity == 0:
            velocity = random.randint(-1, 1)
        return velocity

    def draw_ball(self, surface):
        circleCenter = (self.pos[0], self.pos[1])
        pygame.draw.circle(surface, self.color, circleCenter, self.radius)

    def collision(self, player1):
        global p1, p2
        if player1:
            pad_inst = p1
        else:
            pad_inst = p2

        x_ball = self.pos[0]
        y_ball = self.pos[1]

        x_front = pad_inst.location()[0]
        y_topleft = pad_inst.location()[1]
        y_bottomleft = y_topleft + pad_inst.length()

        ball_reach_right = x_ball + self.radius + self.dirnx
        ball_reach_left = x_ball - self.radius*2 - self.dirnx

        if (y_ball <= y_bottomleft+self.radius) and (y_ball >= y_topleft-self.radius):
            if player1:
                if (ball_reach_right >= x_front) and (ball_reach_right <= x_front + pad_inst.width()):
                    self.dirnx = -self.dirnx - random.randint(-1, 1)
            else:
                if (ball_reach_left <= x_front + pad_inst.width()) and (ball_reach_left >= x_front):
                    self.dirnx = -self.dirnx - random.randint(-1, 1)

        self.pos = [self.pos[0] + self.dirnx, self.pos[1] + self.dirny]


class paddle(pong):
    length = pong.l
    width = pong.w
    thickness = length // 40             # thickness of paddle
    # amount of vertical space paddle can use to hit the ball
    spread = width // 5

    def __init__(self, player1):
        super().__init__()
        self.player1 = player1

        if self.player1:
            self.pos = (length-self.thickness*3, width//2-self.spread//2)
        else:
            self.pos = (self.thickness*2, width//2-self.spread//2)

    def location(self):
        return self.pos

    def length(self):
        return self.spread

    def width(self):
        return self.thickness

    def move_paddle(self, dirny=0):
        global b
        self.dirny = dirny
        self.pos = [self.pos[0], self.pos[1] + self.dirny]

        b.move_ball()                    # keep ball moving
        # check if the ball collided with paddle first
        b.collision(self.player1)

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

    def draw_paddle(self, surface):
        # x-coordinate of top-left corner of rectangle
        x = self.pos[0]
        # y-coordinate of top-left corner of rectangle
        y = self.pos[1]

        if self.player1:
            pygame.draw.rect(surface, self.color,
                             (x, y, self.thickness, self.spread))
        else:
            pygame.draw.rect(surface, self.color,
                             (x, y, self.thickness, self.spread))


if __name__ == '__main__':
    global length, width, b, p1, p2

    length = 750
    width = 500

    flag = True
    b = ball()
    p1 = paddle(True)
    p2 = paddle(False)

    pygame.init()
    # create game and background with length x width size
    win = pygame.display.set_mode((length, width))
    pong().redrawWindow(win)
    clock = pygame.time.Clock()

    while flag:
        # 50 milliseconds (lower value = faster)
        pygame.time.delay(60)
        clock.tick(60)                  # fps limit (lower value = slower)
        p1.move_paddle()
        p2.move_paddle()

        # did the user close the window? If so, terminate program
        flag = pong().event_quit()
        if not flag:                    # if user closed window, break loop too
            break

        pong().redrawWindow(win)
