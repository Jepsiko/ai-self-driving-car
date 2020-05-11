import pygame
import math
import numpy as np

class Lidar:

    def __init__(self, width, height):

        self.matrix = np.zeros((height, width), dtype=int)

    def update(self):
        self.matrix[6][2] = 1
         #print(self.matrix)

    def draw(self, screen, pos, rot, width, length, backlenght):
        #width = width * 10
        #length = length * 10

        rot = math.radians(rot)
        cos = math.cos(rot)
        sin = math.sin(rot)
        p1=(pos[0] + cos * length, pos[1] - sin * width)


        hypfrontof = math.sqrt(math.pow(length, 2) + math.pow((width / 2), 2))
        hypbehind = math.sqrt(math.pow(backlenght, 2) + math.pow((width / 2), 2))

        angle = math.atan((width/2) / length)
        anglebehind = math.atan((width / 2) / backlenght)
        anglebehind = anglebehind - rot
        math.pi - rot - anglebehind
        math.pi + rot + anglebehind

        frontofleft = (pos[0] + math.cos(rot + angle) * hypfrontof, pos[1] - math.sin(rot + angle) * hypfrontof)
        behindleft = (pos[0] + math.cos(rot - angle + math.pi) * hypfrontof, pos[1] - math.sin(rot - angle + math.pi) * hypfrontof)
        behindright = (pos[0] + math.cos(rot + angle + math.pi) * hypfrontof, pos[1] - math.sin(rot + angle + math.pi) * hypfrontof)
        frontofright = (pos[0] + math.cos(rot - angle) * hypfrontof, pos[1] - math.sin(rot - angle) * hypfrontof)

        list=[frontofleft, behindleft, behindright, frontofright]
        pygame.draw.lines(screen, (200, 0, 0 ), True, list)



