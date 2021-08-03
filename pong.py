#Welcome to THE PONG GAME

import random
import pygame
import tkinter as tk
from tkinter import messagebox

class ball(object):
    l = 750
    w = 500
    radius = 8

    def __init__(self, start, color=(255,255,255)):
        self.pos = start
        self.color = color
        self.dirnx = 1
        self.dirny = 0

    def move_ball(self, dirnx, dirny):
        global x_vector, y_vector
        self.dirnx = dirnx              #dirnx is set equal to inputted x_vector
        self.dirny = dirny              #dirny is set equal to inputted y_vector
        self.pos = [self.pos[0] + self.dirnx, self.pos[1] + self.dirny]

        if self.dirnx > 0 and self.pos[0] >= (self.l-self.radius):  #if ball touches right side of screen
            self.pos[0] = self.l-self.radius-1
            x_vector = -dirnx - random.randint(-5, 5)
        elif self.dirnx < 0 and self.pos[0] <= self.radius:         #if ball touches left side of screen
            self.pos[0] = self.radius + 1
            x_vector = -dirnx - random.randint(-5, 5)
        elif self.dirny < 0 and self.pos[1] <= self.radius:         #if ball touches top of screen
            self.pos[1] = self.radius + 1
            y_vector = -dirny - random.randint(-5, 5)
        elif self.dirny > 0 and self.pos[1] >= (self.w-self.radius):  #if ball touches bottom of screen
            self.pos[1] = self.w-self.radius-1
            y_vector = -dirny - random.randint(-5, 5)

        if x_vector > 25:
            x_vector = 25
        elif y_vector > 25:
            y_vector = 25
        elif x_vector == 0:
            x_vector = random.randint(-2, 2)
        elif y_vector == 0:
            y_vector = random.randint(-1, 1)

    def draw_ball(self, surface):
        dis = self.l // self.w  # integer division between length and width
        i = self.pos[0]  # i represents length
        j = self.pos[1]  # j represents width

        circleCenter = (i*dis, j*dis)
        pygame.draw.circle(surface, (255,255,255), circleCenter, self.radius)

    def collision(self):
        pass

class paddle(object):
    length = ball.l
    width = ball.w

    def __init__(self, start, color = (255,255,255)):
        self.pos = start
        self.color = color
        self.dirny = 0

    def move_paddle(self):
        self.dirny = dirny
        self.pos = [self.pos[0], self.pos[1] + self.dirny]

    def draw_paddle(self):
        dis = self.length // self.width  # integer division between length and width
        i = self.pos[0]  # i represents length
        j = self.pos[1]  # j represents width

def redrawWindow(surface):
    global b
    surface.fill((0, 0, 0))  # creates a background (black in this case)
    b.draw_ball(surface)
    pygame.display.update()

def message_box():
    pass

def main():
    global length, width, b, x_vector, y_vector

    length = 750
    width = 500
    x_vector = random.randint(5, 20)
    y_vector = random.randint(-10, 10)

    flag = True
    b = ball((375, 250))

    pygame.init()
    win = pygame.display.set_mode((length, width))  # create game and background with length x width size
    redrawWindow(win)
    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(50)  # 50 milliseconds (lower value = faster)
        clock.tick(30)  # fps limit (lower value = slower)
        b.move_ball(x_vector, y_vector)

        for event in pygame.event.get(): #creates a list of events
            if event.type == pygame.QUIT: #quit game when the user closes the window
                pygame.quit()

        redrawWindow(win)
main()