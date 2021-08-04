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

    def __init__(self, start=(l//2, w//2), color=(255, 255, 255)):
        self.pos = start
        self.color = color


class ball(pong):
    length = pong.l
    width = pong.w
    radius = pong.r

    def move_ball(self, dirnx, dirny):
        global x_vector, y_vector
        self.dirnx = dirnx  # dirnx is set equal to inputted x_vector
        self.dirny = dirny  # dirny is set equal to inputted y_vector
        self.pos = [self.pos[0] + self.dirnx, self.pos[1] + self.dirny]

        # if ball touches right side of screen
        if self.dirnx > 0 and self.pos[0] >= (self.length-self.radius):
            self.pos[0] = self.length-self.radius-1
            x_vector = -dirnx - random.randint(-5, 5)
        # if ball touches left side of screen
        elif self.dirnx < 0 and self.pos[0] <= self.radius:
            self.pos[0] = self.radius + 1
            x_vector = -dirnx - random.randint(-5, 5)
        # if ball touches top of screen
        elif self.dirny < 0 and self.pos[1] <= self.radius:
            self.pos[1] = self.radius + 1
            y_vector = -dirny - random.randint(-5, 5)
        # if ball touches bottom of screen
        elif self.dirny > 0 and self.pos[1] >= (self.width-self.radius):
            self.pos[1] = self.width-self.radius-1
            y_vector = -dirny - random.randint(-5, 5)

        if x_vector > 25:
            x_vector = 25
        elif y_vector > 25:
            y_vector = 25
        elif x_vector == 0:
            x_vector = random.randint(-5, 5)
        elif y_vector == 0:
            y_vector = random.randint(-1, 1)

    def draw_ball(self, surface):
        dis = self.l // self.w  # integer division between length and width
        i = self.pos[0]  # i represents length
        j = self.pos[1]  # j represents width

        circleCenter = (i*dis, j*dis)
        pygame.draw.circle(surface, self.color, circleCenter, self.radius)

    def collision(self):
        pass


class paddle(pong):
    length = pong.l
    width = pong.w

    def move_paddle(self, dirny):
        self.dirny = dirny
        self.pos = [self.pos[0], self.pos[1] + self.dirny]

    def draw_paddle(self, surface, player1):
        sep = length // 20  # distance paddle is from wall
        thickness = length // 35  # thickness of paddle
        center = width // 3  # initial location of paddle
        spread = center  # amount of space paddle can use to hit the ball

        if player1:
            pygame.draw.rect(surface, self.color, (length -
                             sep - thickness, center, thickness, spread))
        else:
            pygame.draw.rect(surface, self.color,
                             (sep, center, thickness, spread))


def redrawWindow(surface):
    global b, p1, p2

    surface.fill((0, 0, 0))  # creates a background (black in this case)
    b.draw_ball(surface)
    p1.draw_paddle(surface, True)
    p2.draw_paddle(surface, False)
    pygame.display.update()


def message_box():
    pass


def main():
    global length, width, b, x_vector, y_vector, p1, p2

    length = 750
    width = 500
    x_vector = random.randint(10, 20)
    y_vector = random.randint(-10, 10)

    flag = True
    b = ball()
    p1 = paddle()
    p2 = paddle()

    pygame.init()
    # create game and background with length x width size
    win = pygame.display.set_mode((length, width))
    redrawWindow(win)
    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(50)  # 50 milliseconds (lower value = faster)
        clock.tick(30)  # fps limit (lower value = slower)
        b.move_ball(x_vector, y_vector)

        for event in pygame.event.get():  # creates a list of events
            if event.type == pygame.QUIT:  # quit game when the user closes the window
                pygame.quit()
                flag = False
        if not flag:
            break

        redrawWindow(win)


main()
