import pygame
import math
import numpy as np


class Lidar:

    def __init__(self, lin, col, width, length, backlength):

        self.matrix = np.zeros((lin, col), dtype=int)
        self.width = width
        self.length = length
        self.backlength = backlength

    def update(self):
        self.matrix[6][2] = 99
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                print(self.matrix[i][j])

        print(self.matrix)

    def draw(self, screen, pos, rot, backlenght):


        rot = math.radians(rot)
        # p1=(pos[0] + cos * length, pos[1] - sin * width)

        hypfrontof = math.sqrt(math.pow(self.length, 2) + math.pow((self.width / 2), 2))
        hypbehind = math.sqrt(math.pow(backlenght, 2) + math.pow((self.width / 2), 2))

        angle = math.atan((self.width / 2) / self.length)
        anglebehind = math.pi / 2 - (math.atan((self.width / 2) / self.backlength))

        frontleft = (pos[0] + math.cos(rot + angle) * hypfrontof, pos[1] - math.sin(rot + angle) * hypfrontof)
        behindleft = (pos[0] + math.cos(rot + math.pi / 2 + anglebehind) * hypbehind,
                      pos[1] - math.sin(rot + math.pi / 2 + anglebehind) * hypbehind)
        behindright = (pos[0] + math.cos(rot - math.pi / 2 - anglebehind) * hypbehind,
                       pos[1] - math.sin(rot - math.pi / 2 - anglebehind) * hypbehind)
        frontright = (pos[0] + math.cos(rot - angle) * hypfrontof, pos[1] - math.sin(rot - angle) * hypfrontof)

        lidarpoints = [frontleft, behindleft, behindright, frontright]
        pygame.draw.lines(screen, (200, 0, 0), True, lidarpoints)

        self.draw_circle(frontleft, behindleft, frontright, self.width, self.length + self.backlength)

    def draw_circle(self, frontofleft, behindleft, frontofright, width, lenght):
        lin = self.matrix

        pass
